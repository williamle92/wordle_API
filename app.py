from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token
from werkzeug.security import check_password_hash, generate_password_hash
from flask_migrate import Migrate
from flask_restful import Api
from config import Config
from db import db
from models.user import User
from models.guess import Guess
from models.guess import Game
from resources.game import GameResource, Games
from resources.guess import GuessResource
from resources.user import UserRegister, UserResource


# create flask app
app = Flask(__name__)

# Get configs from Config object
app.config.from_object(Config)

# instantiating migrate object
migrate = Migrate(app, db)


# instantiate db
db.init_app(app)

# instantiate API object
api = Api(app)

# instantiate jwt object
jwt = JWTManager(app)

# temporary view


@app.route('/')
def home():
    return "Wordle!"


@app.post("/login")
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(username=username).first()
    print(user)
    print(username, password)
    if user:
        # Create a password hash
        pwhash = generate_password_hash(password)
        # Compares the password hash against password
        is_pass_correct = check_password_hash(pwhash, password)

        if is_pass_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return jsonify(
                {"user": {
                    "refresh": refresh, "access": access, "data" : {"username": user.username, "email": user.email}
                }
                }), 200
    return jsonify({"Message": "Error! The credentials you entered are incorrect, please try again."}), 401


api.add_resource(UserRegister, '/register')
api.add_resource(UserResource, "/user/<id>")
api.add_resource(GameResource, '/game/<id>', '/game')
api.add_resource(Games, '/games')
api.add_resource(GuessResource, "/guess")


if __name__ == "__main__":
    app.run(debug=True)
