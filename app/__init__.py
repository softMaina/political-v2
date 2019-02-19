import os

from flask import Flask
from instance.config import config
from app.api.v2.database import init_db

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

    return app