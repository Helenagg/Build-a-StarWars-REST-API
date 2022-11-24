"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People
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

users = [
    {"id": 1,
    "email": "bob@dylan2.com",
    "password": "asda",
    "is_active": "True"},
    {"id": 2,
    "email": "paul@dylan2.com",
    "password": "bcbc",
    "is_active": "True"},
]

favorites = [
    {"id": 1,
    "id_user": 1,
    "id_planet": 1,
    "id_people": 1},
    {"id": 2,
    "id_user": 2,
    "id_planet": 1,
    "id_people": 1}
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
    response_user = users
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_user), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def select_user(user_id):
    user = list(filter(lambda element: element['id'] == user_id, users))
    return jsonify(user), 200

# Get, Post and Delete People
@app.route('/people', methods=['GET'])
def handle_people():
    response_people = people
    return jsonify(response_people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def select_people(people_id):
    person = list(filter(lambda element: element['id'] == people_id, people))
    return jsonify(person), 200

# Get, Post and Delete Planets
@app.route('/planet', methods=['GET'])
def handle_planet():
    planets = Planet.query.all()
    # result = []
    # for planet in planets:
    #     result.append(planet.serialize())
    result = [planet.serialize() for planet in planets]
    return jsonify(result), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def select_planet(planet_id):
    planet = Planet.query.get(planet_id)
    planet = planet.serialize()
    return jsonify(planet), 200

@app.route('/planet', methods=['POST'])
def create_planet():  
    data = request.data
    data = json.loads(data)

    planet = Planet(name = data['name'], rotation_period = data['rotation_period'])
    db.session.add(planet)
    db.session.commit()
    response_body = {
        "msg": "Todo Ok! "
    }
    return jsonify(response_body), 200

@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id): 
    planet_delete = Planet.query.get(planet_id)
    db.session.delete(planet_delete)
    db.session.commit()
    
    response_body = {
        "msg": "Borrado! "
    }
    return jsonify(response_body), 200    

@app.route('/favorite', methods=['GET'])
def handle_fav():
    response_fav = favorites
    return jsonify(response_fav), 200

@app.route('/favorite/<int:fav_id>', methods=['GET'])
def select_fav(fav_id):
    favorite = list(filter(lambda element: element['id'] == fav_id, favorites))
    return jsonify(favorite), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
