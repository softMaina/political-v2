import os

from flask import Flask
from instance.config import config
from app.api.v2.database import init_db

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    init_db()

    return app