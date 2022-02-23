from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from config import Config

# create flask app
app = Flask(__name__)

# Get configs from Config object
app.config.from_object(Config)


migrate = Migrate(app,db)