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
users = mongo.db.users   
recipes = mongo.db.recipes

# Main Pages

@app.route('/') #This is routing for the home page
@app.route('/index')
def home_page():
    return render_template("index.html")


@app.route('/recipe', methods=['GET', 'POST'])   #Routing for recipe page 
def recipe_page():   
    """this function allows the user to insert the recipe into the mongodb database
        and will flash a message when succesful"""

    create_recipe = {                       
        'category' : request.form.get('category'),
        'name' : request.form.get('name'),
        'ingredients' : request.form.get('ingredients'),
        'how_to_cook' : request.form.get('how_to_cook'),
        'additional_notes' : request.form.get('additional_notes')
    }
    recipes.insert_one(create_recipe)
    return render_template("recipes.html")



@app.route('/login', methods=['GET', 'POST'])  #routing for the log in page 
def login_page():
    """ This function allows a user to log into the site with a username and unhashing of the password 
        If corrrect they are redirected to the home page, if incorrect a message will flash and redirect
        to the login page """    

    LoginForm()

    if request.method == 'POST':
    
        login_users = users.find_one({'username' : request.form['username']})

        if login_users:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_users['password']) == login_users['password']:
                session['username'] = request.form['username']
                return redirect(url_for("home_page"))

        flash('Login Details Incorrect')
        return redirect(url_for("login_page"))

    return render_template("login.html")



@app.route('/register', methods=['GET', 'POST']) # Routing for register page
def register_page():
    """ This function allows the user to register details and they will get saved to the mongodb database
        the password they enter will be hashed to offer more security, when succesful a session is logged 
        and returned to the home page. If unsuccesful they will be flashed a message and redirected to the register page"""

    register_form = RegisterForm()

    if request.method == 'POST':
        current_user = users.find_one({'username' : request.form['username']})
        
        if current_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'name' : register_form.name.data, 'username' : register_form.username.data, 'email' : register_form.email.data, 'password' : hashpass})
            session['username'] = request.form['username']
            flash('You are now registered!', 'success')
            return redirect(url_for('register_page'))
        else:
            flash('This Username Already Exists!', 'error')
            return redirect(url_for("register_page"))
    
    return render_template("register.html", form=register_form)


#  Recipe pages 

@app.route('/meat-recipes', methods=['GET', 'POST']) # Routing for the meat recipes page
def meat_recipes():
    """ This function will search for the meat category in my mongodb database and render the results to be 
        displayed in my html page"""

    meats = recipes.find({'category': 'meat'})

    return render_template("meat-recipes.html", meats=meats, recipe=recipes.find())


@app.route('/pasta-recipes', methods=['GET', 'POST']) # Routing for the pasta recipes page
def pasta_recipes():
    """ This function will search for the pasta category in my mongodb database and render the results to be 
        displayed in my html page"""

    pastas = recipes.find({'category': 'pasta'})

    return render_template("pasta-recipes.html", pastas=pastas, recipe=recipes.find())


@app.route('/poultry-recipes', methods=['GET', 'POST']) # Routing for the poultry recipes page
def poultry_recipes():
    """ This function will search for the poultry category in my mongodb database and render the results to be 
        displayed in my html page"""
    poultrys = recipes.find({'category': "poultry"})

    return render_template("poultry-recipes.html", poultrys=poultrys, recipe=recipes.find())


@app.route('/vegetarian-recipes', methods=['GET', 'POST']) # Routing for the vegatarian recipes page
def vegetarian_recipes():
    """ This function will search for the vegetarian category in my mongodb database and render the results to be 
        displayed in my html page"""
    vegetarians = recipes.find({'category': 'vegetarian'})

    return render_template("vegetarian-recipes.html", vegetarians=vegetarians, recipe=recipes.find())



# Ingredients Pages 

@app.route('/meat-ingredients/<meat_id>') # Routing for my meat ingredients page
def meat_ingredients(meat_id):

    recipe = recipes.find_one({'_id': ObjectId(meat_id)})

    meat = ({'_id': ObjectId(meat_id)})

    return render_template("meat-ingredients.html", recipes=recipe, recipe=recipes, meat=meat)

@app.route('/poultry-ingredients/<poultry_id>') # routing for my poultry ingredients page
def poultry_ingredients(poultry_id):

    recipe = recipes.find_one({'_id': ObjectId(poultry_id)})

    poultry = ({'_id': ObjectId(poultry_id)})

    return render_template("poultry-ingredients.html", recipes=recipe, poultry=poultry)

@app.route('/pasta-ingredients/<pasta_id>') # Routing for my pasta ingredients page
def pasta_ingredients(pasta_id):

    recipe = recipes.find_one({'_id': ObjectId(pasta_id)})

    pasta = ({'_id': ObjectId(pasta_id)})

    return render_template("pasta-ingredients.html", recipes=recipe, pasta=pasta)

@app.route('/vegetarian-ingredients/<vegetarian_id>') # Routing for my vegetarian ingredients page
def vegetarian_ingredients(vegetarian_id):

    recipe = recipes.find_one({'_id': ObjectId(vegetarian_id)})

    vegetarian = ({'_id': ObjectId(vegetarian_id)})

    return render_template("vegetarian-ingredients.html", recipes=recipe, vegetarian=vegetarian)


# Edit Pages

@app.route('/edit-recipe/<meat_id>', methods=['GET', 'POST']) # routing to edit meat recipes
def edit_recipe_meat(meat_id):
    

    if request.method == "POST":
        recipes.find_one_and_update({'_id': ObjectId(meat_id)},
        {'$set':
        {                       
        'category' : request.form.get('category'),
        'name' : request.form.get('name'),
        'ingredients' : request.form.get('ingredients'),
        'how_to_cook' : request.form.get('how_to_cook'),
        'additional_notes' : request.form.get('additional_notes')
        }
        })

    meat = ({'_id': ObjectId(meat_id)})

    return render_template("edit-recipe-meat.html", meat=meat)

@app.route('/edit-recipe/<poultry_id>', methods=['GET', 'POST']) # routing to edit poultry recipes
def edit_recipe_poultry(poultry_id):
    

    if request.method == "POST":
        recipes.find_one_and_update({'_id': ObjectId(poultry_id)},
        {'$set':
        {                       
        'category' : request.form.get('category'),
        'name' : request.form.get('name'),
        'ingredients' : request.form.get('ingredients'),
        'how_to_cook' : request.form.get('how_to_cook'),
        'additional_notes' : request.form.get('additional_notes')
        }
        })

    poultry = ({'_id': ObjectId(poultry_id)})

    return render_template("edit-recipe-poultry.html", poultry=poultry)

@app.route('/edit-recipe/<pasta_id>', methods=['GET', 'POST']) # routing to edit pasta recipes
def edit_recipe_pasta(pasta_id):
    

    if request.method == "POST":
        recipes.find_one_and_update({'_id': ObjectId(pasta_id)},
        {'$set':
        {                       
        'category' : request.form.get('category'),
        'name' : request.form.get('name'),
        'ingredients' : request.form.get('ingredients'),
        'how_to_cook' : request.form.get('how_to_cook'),
        'additional_notes' : request.form.get('additional_notes')
        }
        })

    pasta = ({'_id': ObjectId(pasta_id)})

    return render_template("edit-recipe-pasta.html", pasta=pasta)


@app.route('/edit-recipe/<vegetarian_id>', methods=['GET', 'POST']) # routing to edit vegetarian recipes
def edit_recipe_vegetarian(vegetarian_id):
    

    if request.method == "POST":
        recipes.find_one_and_update({'_id': ObjectId(vegetarian_id)},
        {'$set':
        {                       
        'category' : request.form.get('category'),
        'name' : request.form.get('name'),
        'ingredients' : request.form.get('ingredients'),
        'how_to_cook' : request.form.get('how_to_cook'),
        'additional_notes' : request.form.get('additional_notes')
        }
        })

    vegetarian = ({'_id': ObjectId(vegetarian_id)})

    return render_template("edit-recipe-vegetarian.html", vegetarian=vegetarian)



# Delete Pages

@app.route('/delete-recipe/<meat_id>', methods=['GET', 'POST']) # Routing for delete meat recipes
def delete_recipe_meat(meat_id):

    if request.method == "POST":
        recipes.delete_one({'_id': ObjectId(meat_id)})
        redirect(url_for("recipe_page"))

    meat = ({'_id': ObjectId(meat_id)})
    
    return render_template("delete-recipe-meat.html", meat=meat, recipes=recipes)
    
@app.route('/delete-recipe/<poultry_id>', methods=['GET', 'POST']) # Routing for delete poultry recipes
def delete_recipe_poultry(poultry_id):

    if request.method == "POST":
        recipes.delete_one({'_id': ObjectId(poultry_id)})
        redirect(url_for("recipe_page"))

    poultry = ({'_id': ObjectId(poultry_id)})
    
    return render_template("delete-recipe-meat.html", poultry=poultry, recipes=recipes)

@app.route('/delete-recipe/<pasta_id>', methods=['GET', 'POST']) # Routing for delete pasta recipes
def delete_recipe_pasta(pasta_id):

    if request.method == "POST":
        recipes.delete_one({'_id': ObjectId(pasta_id)})
        redirect(url_for("recipe_page"))

    pasta = ({'_id': ObjectId(pasta_id)})
    
    return render_template("delete-recipe-meat.html", pasta=pasta, recipes=recipes)

@app.route('/delete-recipe/<vegetarian_id>', methods=['GET', 'POST']) # Routing for delete vegetarian recipes
def delete_recipe_vegetarian(vegetarian_id):

    if request.method == "POST":
        recipes.delete_one({'_id': ObjectId(vegetarian_id)})
        redirect(url_for("recipe_page"))

    vegetarian = ({'_id': ObjectId(vegetarian_id)})
    
    return render_template("delete-recipe-meat.html", vegetarian=vegetarian, recipes=recipes)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP', "0.0.0.0"),
    port=int(os.environ.get('PORT', "5000")),
    debug=True)