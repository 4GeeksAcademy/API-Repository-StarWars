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
from models import db, User, Planet, Character, Favourites
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

    users=User.query.all()
    if users == []:
        return jsonify({"MSG": "NO EXISTEN USUARIOS"}), 404
    response_body=[item.serialize() for item in users]

    return jsonify(response_body), 200;

@app.route('/planet', methods=['GET'])
def handle_planet():

    planet=Planet.query.all()
    if planet == []:
        return jsonify({"MSG": "NO EXISTEN PLANETAS"}), 404
    response_body=[item.serialize() for item in planet]

    return jsonify(response_body), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def handle_planetbyid(planet_id):

    planet=Planet.query.get(planet_id)
    if planet == None:
        return jsonify({"MSG": "NO EXISTEN PLANETAS FAVORITOS"}), 404
    return jsonify(planet.serialize()), 200

@app.route('/character', methods=['GET'])
def handle_character():

    character=Character.query.all()
    if character == []:
        return jsonify({"MSG": "NO EXISTEN PERSONAJES"}), 404
    response_body=[item.serialize() for item in character]

    return jsonify(response_body), 200;

@app.route('/character/<int:character_id>', methods=['GET'])
def handle_characterbyid(character_id):

    character=Character.query.get(character_id)
    if character == None:
        return jsonify({"MSG": "NO EXISTEN PERSONAJES FAVORITOS"}), 404
    return jsonify(character.serialize()), 200

@app.route('/favourites/character/<int:character_id>', methods=['POST'])
def handle_postcharacter(character_id):
    user=User.query.get(1)
    new_favourite=Favourites()
    character=Character.query.get(character_id)

    new_favourite.user = user
    new_favourite.character = character

    db.session.add(new_favourite)
    db.session.commit()

    return jsonify(new_favourite.serialize()), 200

@app.route('/favourites/character/<int:character_id>', methods=['DELETE'])
def handle_deletecharacter(character_id):
    favourite=Favourites.query.filter_by(user_id=1, character_id=character_id).first()
    db.session.delete(favourite)
    db.session.commit()

    return jsonify({"MSG": "ELIMINADO CON EXITO"}),200








@app.route('/user/favourites', methods=['GET'])
def handle_favourites():

    favourites=Favourites.query.all()
    if favourites == []:
        return jsonify({"MSG": "NO EXISTEN FAVORITOS"}), 404
    response_body=[item.serialize() for item in favourites]

    return jsonify(response_body), 200;




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
