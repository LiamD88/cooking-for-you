import os 
from flask import Flask
from flask_pymongo import PyMongo
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__) 

MONGODB_URI = os.getenv("MONGO_URI")
DBS_NAME = "NewRecipes"
COLLECTION_NAME = "Recipes"

mongo = PyMongo(app)



if __name__ == '__main__':
    app.run(host=os.environ.get('IP', "0.0.0.0"),
    port=int(os.environ.get('PORT', "5000")),
    debug=True)
