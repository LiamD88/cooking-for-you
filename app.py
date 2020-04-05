import os 
from flask import Flask, render_template
from flask_pymongo import PyMongo
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__) 

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
DBS_NAME = "NewRecipes"
COLLECTION_NAME = "Recipes"

mongo = PyMongo(app)


@app.route('/index')
def home_page():
    return render_template("index.html")


@app.route('/recipe')
def recipe_page():
    return render_template("recipes.html")



@app.route('/login')
def login_page():
    return render_template("login.html")


@app.route('/')
@app.route('/ingredients')
def ingredients_page():
    return render_template("ingredients.html")




if __name__ == '__main__':
    app.run(host=os.environ.get('IP', "0.0.0.0"),
    port=int(os.environ.get('PORT', "5000")),
    debug=True)
