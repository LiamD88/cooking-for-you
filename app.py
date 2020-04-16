import os 
from flask import Flask, render_template, url_for, redirect, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__) 

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["SECRET_KEY"] = os.environ.get["SECRET KEY"]

mongo = PyMongo(app)

@app.route('/')
@app.route('/index')
def home_page():
    return render_template("index.html")


@app.route('/recipe')
def recipe_page():
    return render_template("recipes.html", )



@app.route('/login')
def login_page():
    return render_template("login.html")



@app.route('/meat-ingredients')
def meat_ingredients():
    return render_template("meat-ingredients.html")

@app.route('/poultry-ingredients')
def poultry_ingredients():
    return render_template("poultry-ingredients.html")

@app.route('/pasta-ingredients')
def pasta_ingredients():
    return render_template("pasta-ingredients.html")

@app.route('/vegetarian-ingredients')
def vegetarian_ingredients():
    return render_template("vegetarian-ingredients.html")



if __name__ == '__main__':
    app.run(host=os.environ.get('IP', "0.0.0.0"),
    port=int(os.environ.get('PORT', "5000")),
    debug=True)
