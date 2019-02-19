import os
import datetime
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from flask import Flask, jsonify, request, make_response, abort, Blueprint
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity
)
from instance import config
from app.api.v2.utils.validator import format_response, check_duplication,validate_credentials
from app.api.v2.models import user_model


auth_route = Blueprint('auth',__name__,url_prefix='/api/v2/auth')

user = user_model.User()

@auth_route.route('/register',methods=['POST'])
def register():

    data = request.get_json()

    if not data:
        return format_response(400,"missing credentials")

    
    try:
        email = data["email"]
    except KeyError:
        return make_response(jsonify({
                    "message": "Please supply an email to be able to register an attendant"
                    }), 400)

    try:
        request_password = data["password"]
    except KeyError:
        return make_response(jsonify({
                    "message": "Please supply a password to be able to register an attendant"
                    }), 400)  
    if not isinstance(data["email"], str):
        return make_response(jsonify({
                    "message": "Email should be a string"
                    }), 400)   
    if not isinstance(data["password"], str):
        return make_response(jsonify({
                    "message": "Password should be a string"
                    }), 400)
    firstname = data["firstname"]
    lastname = data["lastname"]
    othername = data["othername"]
    phoneNumber = data["phoneNumber"]
    passportUrl = data["passportUrl"]

    # validate_credentials(self,data)
    check_duplication("email", "users", email)
    # hash the user password
    hashed_password = generate_password_hash(request_password, method='sha256')

    user.save_user(firstname,lastname,othername,email,phoneNumber,passportUrl,hashed_password, False)

    return make_response(jsonify({
        "status":201,
        "message":"user successfully created"
    }),201)
    
@auth_route.route('/login',methods=['POST'])
def login():

    data = request.get_json()          
    if not data:
        return make_response(jsonify({
            "message": "Kindly provide an email and a password to login"
        }
        ), 400)

    try:
        request_mail = data["email"]
    except:
        return make_response(jsonify({
            "message": "Kindly provide an email address to log in"
            }), 400)

    try:
        request_password = data["password"]
    except:
        return make_response(jsonify({
            "message": "Kindly provide a password to log in"
            }), 400)

    if not isinstance(data['email'], str):
            return make_response(jsonify({
            "message": "E-mail should be a string"
        }
        ), 406)

    if not isinstance(data['password'], str):
            return make_response(jsonify({
            "message": "Password should be a string"
        }
        ), 406)

    request_email = request_mail.strip()                   
    user = user_model.User.fetch_user(request_email)
    
    if user:
        token = jwt.encode({
            "email": request_email,
            "user_id": user[0]['user_id'],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=3000)
        }, os.getenv('JWT_SECRET_KEY', default='SdaHv342nx!jknr837bjwd?c,lsajjjhw673hdsbgeh'))
        return make_response(jsonify({
                        "message": "Login successful",
                        "token": token.decode("UTF-8")}), 200)

    return make_response(jsonify({
        "message": "Try again. E-mail or password is incorrect!"
    }
    ), 403)
