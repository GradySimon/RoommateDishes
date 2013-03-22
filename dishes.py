import random
from datetime import timedelta, datetime, date
import pytz
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

timezone = pytz.timezone('US/Eastern')
dish_days_of_the_week = (1, 3, 5)  # ISO week days for Mon, Wed, Fri

app = Flask(__name__)
app.config.from_pyfile('dishes.cfg')
db = SQLAlchemy(app)


class Dish_Doer(db.Model):
    __tablename__ = 'dish_doer'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    dish_days = db.relationship('Dish_Day', backref='dish_doer', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Dish_Doer: name='%s'>" % self.name


class Dish_Day(db.Model):
    __tablename__ = 'dish_day'
    id = db.Column('id', db.Integer, primary_key=True)
    date = db.Column('date', db.Date)
    dish_doer_id = db.Column(db.Integer, db.ForeignKey('dish_doer.id'))

    def __init__(self, date, dish_doer):
        self.date = date
        self.dish_doer = dish_doer
    
    def __repr__(self):
        return "<Dish_Day: date='%s' | dish_doer=%s>" % (self.date, self.dish_doer)


@app.route('/')
def front_page():
    dish_doer = get_proper_dish_doer()
    return render_template("index.html", dish_doer=dish_doer.name)


def get_proper_dish_doer():
    update_dish_days_if_necessary()
    return get_current_dish_doer()


def is_necessary_to_update_dish_days():
    return current_date() >= get_following_dish_date(get_most_recent_dish_day())


def update_dish_days_if_necessary():
    while is_necessary_to_update_dish_days():
        next_dish_date = get_following_dish_date(get_most_recent_dish_day())
        db.session.add(Dish_Day(next_dish_date, select_next_dish_doer()))
        db.session.commit()


def select_next_dish_doer():
    return random.choice(get_dish_doer_candidates())


def get_dish_doer_candidates():
    return Dish_Doer.query.all()


def get_current_dish_doer():
    return get_most_recent_dish_day().dish_doer


def current_date():
    now = datetime.now(timezone)
    return date(now.year, now.month, now.day)


def is_a_dish_date(date):
    return date.isoweekday() in dish_days_of_the_week


def get_following_dish_date(last_dish_day):
    one_day = timedelta(days=1)
    if last_dish_day is None:
        next_dish_date = current_date()
    else:
        next_dish_date = last_dish_day.date + one_day
    while not is_a_dish_date(next_dish_date):
        next_dish_date += one_day
    return next_dish_date


def get_most_recent_dish_day():
    return Dish_Day.query.order_by(Dish_Day.date.desc()).first()


if __name__ == '__main__':
    app.run()
