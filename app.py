from flask import Flask, request, make_response, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restful import Api
from config import Config
from db import db
import random

def load_dict(file_name):
    file = open(file_name)
    words = file.readlines()
    file.close()
    return [word[:5].upper() for word in words]

possible_wordle_words = load_dict("dict_wordle.txt")
english_5_letter_words = load_dict("english_5_words.txt")
answer = random.choice(possible_wordle_words)

print(possible_wordle_words)
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
    return "Hello World!"

app.route("/login")
def login():
    return "hello world"
    

if __name__ == "__main__":
    app.run(debug=True)