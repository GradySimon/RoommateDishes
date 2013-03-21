from flask import Flask

app = Flask(__name__)

@app.route('/')
def front_page():
	dish_doer = get_proper_dish_doer()
	return render_template("index.html", dish_doer=dish_doer)

def get_proper_dish_doer():
	if is_necessary_to_update_dish_doer():
		update_dish_doer(select_next_dish_doer())
	return get_dish_doer()

def is_necessary_to_update_dish_doer():
	

def update_dish_doer():
	

def select_next_dish_doer():
	

def get_dish_doer():
	
