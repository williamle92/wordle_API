from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from config import Config
from db import db

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


# temporary view
@app.route('/')
def home():
    return "Hello World!"