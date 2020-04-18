import os 
from flask import Flask, render_template, url_for, redirect, request, session, logging, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import RegisterForm, LoginForm
import bcrypt
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__) 

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route('/')
@app.route('/index')
def home_page():
    return render_template("index.html")


@app.route('/recipe')
def recipe_page():
    return render_template("recipes.html", )



@app.route('/login', methods=['POST'])
def login_page():
    
    LoginForm()

    if request.method == 'POST':
        users = mongo.db.users
    
        login_users = users.find_one({'username' : request.form['username']})

        if login_users:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_users['password'].encode('utf-8')) == login_users['password'].encode('utf-8'):
                session['username'] = request.form['username']
                return redirect(url_for("home_page"))

        flash('Login Details Incorrect')
        return redirect(url_for("login_page"))

    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    
    register_form = RegisterForm()

    if request.method == 'POST':
        users = mongo.db.users
        current_user = users.find_one({'username' : request.form['username']})
        
        if current_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'name' : register_form.name.data, 'password' : hashpass})
            users.insert_one({'username' : register_form.username.data, 'password' : hashpass})
            users.insert_one({'email' : register_form.email.data, 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('home_page'))
        else:
            flash('This Username Already Exists!')
            return redirect(url_for("register_page"))

    return render_template("register.html")




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
