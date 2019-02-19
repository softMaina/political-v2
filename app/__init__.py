import os

from flask import Flask
from instance.config import config

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    


    return app