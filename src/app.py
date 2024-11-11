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

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

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
def get_people():
   all_people = People.query.all()
   people = list(map(lambda x: x.to_dict(), all_people))
   return jsonify(people), 200

@app.route('/people/<int:id_people>', methods=['GET'])   
def get_people_by_id(id_people):
   id_people = People.query.filter_by(id=id_people)
   people = list(map(lambda x: x.to_dict(), id_people))
   return jsonify(people.to_dict()), 200

@app.route('/planets', methods=['GET'])
def get_planets():
   all_planets = Planet.query.all()
   planets = list(map(lambda x: x.to_dict(), all_planets))
   return jsonify(planets), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])   
def get_planets_by_id(planet_id):
   planet_id = Planet.query.filter_by(id=planet_id)
   planets = list(map(lambda x: x.to_dict(), planet_id))
   return jsonify(planets.to_dict()), 200

@app.route('/users', methods=['GET'])
def get_users():    
   all_users = User.query.all()
   users = list(map(lambda x: x.to_dict(), all_users))
   return jsonify(users), 200   

@app.route('/users/<int:id>/favorites', methods=['GET'])
def get_users_favorites():
   all_favorites = Favorites.query.filter_by(id_user=id)
   favorites = list(map(lambda x: x.to_dict(), all_favorites))
   return jsonify(favorites), 200


@app.route('/users/<int:id_user>/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
   id_user = request.json.get("id_user")
   favorite_planet = Favorites(id_user=id_user, planet_id=planet_id)
   db.session.add(favorite_planet)
   db.session.commit()
   return jsonify(favorite_planet.to_dict()), 200

@app.route('/users/<int:id_user>/favorite/people/<int:id_people>', methods=['POST'])
def add_favorite_people(id_people):
   id_user = request.json.get("id_user")
   favorite_people = Favorites(id_user=id_user, id_people=id_people)
   db.session.add(favorite_people)
   db.session.commit()
   return jsonify(favorite_people.to_dict()), 200


@app.route('/users/<int:id_user>/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
   id_user = request.json.get("id_user")
   favorite_planet = Favorites.query.filter_by(id_user=id_user, planet_id=planet_id)
   db.session.delete(favorite_planet)
   db.session.commit()
   return jsonify(favorite_planet.to_dict()), 200


@app.route('/users/<int:id_user>/favorite/people/<int:id_people>', methods=['DELETE'])   
def delete_favorite_people(id_people):       
   id_user = request.json.get("id_user")
   favorite_people = Favorites.query.filter_by(id_user=id_user, id_people=id_people)
   db.session.delete(favorite_people)
   db.session.commit()
   return jsonify(favorite_people.to_dict()), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
