import os

from flask import Flask
from instance.config import config
from app.api.v2.database import init_db
from app.api.v2.utils.validator import return_error

# handle 405 errors
def handle_405_error(err):
    return return_error(405,"method not allowed")

# handle 404 errors
def handle_404_error(err):
    return return_error(404,"Not found")

def handle_500_error(err):
    return return_error(500,'Internal Server error')

def handle_400_error(err):
    return return_error(400,'Bad Request')

def handle_401_error(err):
    return return_error(401,'Unauthorised')

def handle_502_error(err):
    return return_error(502,"Bad Gateway")

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    

    from app.api.v2.views import office_view
    from app.api.v2.views import user_view
    from app.api.v2.views import party_view
    from app.api.v2.views import candidate_view
    from app.api.v2.views import vote_view
    

    app.register_blueprint(party_view.party_route)
    app.register_blueprint(user_view.auth_route)
    app.register_blueprint(office_view.office_route)
    app.register_blueprint(candidate_view.candidate_route)
    app.register_blueprint(vote_view.vote_route)

    app.register_error_handler(405,handle_405_error)
    app.register_error_handler(404,handle_404_error)
    app.register_error_handler(400,handle_400_error)
    app.register_error_handler(502,handle_502_error)
    app.register_error_handler(500,handle_500_error)
    app.register_error_handler(400,handle_400_error)
    app.register_error_handler(401,handle_401_error)

    return app