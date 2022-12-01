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
from models import db, User, Planet, People, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# users = [
#     {"id": 1,
#     "email": "bob@dylan2.com",
#     "password": "asda",
#     "is_active": "True"},
#     {"id": 2,
#     "email": "paul@dylan2.com",
#     "password": "bcbc",
#     "is_active": "True"},
# ]

# favorites = [
#     {"id": 1,
#     "id_user": 1,
#     "id_planet": 1,
#     "id_people": 1},
#     {"id": 2,
#     "id_user": 2,
#     "id_planet": 1,
#     "id_people": 1}
# ]

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Get, Post and Delete User
@app.route('/user', methods=['GET'])
def handle_hello():
    users = User.query.all()
    response_user = [user.serialize() for user in users]
    response_body = {
        "msg": "Users list"
    }

    return jsonify(response_user), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def select_user(user_id):
    # user = list(filter(lambda element: element['id'] == user_id, users))
    user = User.query.get(user_id)
    user = user.serialize()
    return jsonify(user), 200

# Get, Post and Delete People
@app.route('/people', methods=['GET'])
def handle_people():
    peoples = People.query.all()
    result_people = [people.serialize() for people in peoples]
    return jsonify(result_people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def select_people(people_id):
    person = People.query.get(people_id)
    person = person.serialize()
    return jsonify(person), 200

@app.route('/people', methods=['POST'])
def create_people():
    data = request.data
    data = json.loads(data)

    person = People(name = data['name'], mass = data['mass'])
    db.session.add(person)
    db.session.commit()
    response_body = {
        "msg": "Todo Ok! "
    }
    return jsonify(response_body), 200

@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_person(people_id):
    person_delete = People.query.get(people_id)
    db.session.delete(person_delete)
    db.session.commit()

    response_body = {
        "msg": "Borrado! "
    }
    return jsonify(response_body), 200

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

# Get, post and delete Favorites
@app.route('/favorite', methods=['GET'])
def handle_fav():
    # favorites = Favorites.query.filter_by(id == user_id)
    favorites = Favorites.query.all()
    fav = [favorite.serialize() for favorite in favorites]

    return jsonify(fav), 200

@app.route('/favorite/<int:id>', methods=['GET'])
def select_fav(id):
    # user_id = request.json.get('user_id', None)
    # fav = Favorites.query.filter_by(id)
    # list_fav = Favorites.query.all()
    # favorites = [fav.serialize() for fav in list_fav]
    # x = fav[user_id]

    # favorites = Favorites.query.all()
    # fav = [favorite.serialize() for favorite in favorites]
    # x = fav.filter_by(id == fav.user_id)

    fav = Favorites.query.filter_by(user_id = id).all()
    # fav = fav.serialize()
    favorite_user = [favorite.serialize() for favorite in fav]
    print(fav)
    return jsonify(favorite_user), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
