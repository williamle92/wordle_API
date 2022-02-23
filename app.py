from flask import Flask, request, make_response, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restful import Api
from config import Config
from db import db
from resources.game import GameResource, Games
from resources.user import UserRegister, UserResource







# create flask app
app = Flask(__name__)

# Get configs from Config object
app.config.from_object(Config)

# instantiating migrate object
migrate = Migrate(app,db)


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

app.route("/login")
def login():
    return "hello world"
    

api.add_resource(UserRegister, '/register')
api.add_resource(UserResource, "/user/<id>")
api.add_resource(GameResource, '/game/<id>', '/game')
api.add_resource(Games, '/games')



if __name__ == "__main__":
    app.run(debug=True)