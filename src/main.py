"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

people = [{"id": 1,
        "name": "Luke Skywalker", 
        "height": "172", 
        "mass": "77", 
        "hair_color": "blond", 
        "skin_color": "fair", 
        "eye_color": "blue", 
        "birth_year": "19BBY"},

    {"id": 2,
    "name": "C-3PO", 
    "height": "167", 
    "mass": "75", 
    "hair_color": "n/a", 
    "skin_color": "gold", 
    "eye_color": "yellow", 
    "birth_year": "112BBY"}]

planets = [
    {"id":0,
    "name": "Tatooine", 
    "rotation_period": "23", 
    "orbital_period": "304", 
    "diameter": "10465", 
    "climate": "arid", 
    "gravity": "1 standard", 
    "terrain": "desert", 
    "surface_water": "1", 
    "population": "200000"},
    {"id":1,
    "name": "Alderaan", 
    "rotation_period": "24", 
    "orbital_period": "364", 
    "diameter": "12500", 
    "climate": "temperate", 
    "gravity": "1 standard", 
    "terrain": "grasslands, mountains", 
    "surface_water": "40", 
    "population": "2000000000"}
]

users = [
    {"id": 1,
  "first_name": "Bob",
  "last_name": "Dylan",
  "email": "bob@dylan2.com",
  "password": "asda"},
  {"id": 2,
  "first_name": "Paul",
  "last_name": "McCartney",
  "email": "paul@dmccartney.com",
  "password": "bcbc"}
]

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def handle_people():
    response_people = people
    return jsonify(response_people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def select_people(people_id):
    person = list(filter(lambda element: element['id'] == people_id, people))
    return jsonify(person), 200

@app.route('/planet', methods=['GET'])
def handle_planet():
    response_planet = planets
    return jsonify(response_planet), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def select_planet(planet_id):
    planet = list(filter(lambda element: element['id'] == planet_id, planets))
    return jsonify(planet), 200

@app.route('/users', methods=['GET'])
def handle_user():
    response_user = users
    return jsonify(response_user), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
