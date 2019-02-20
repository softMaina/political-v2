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
from app.api.v2.utils.validator import format_response, check_duplication,validate_credentials, validate_phone_number
from app.api.v2.utils.validator import return_error, validate_string, validate_alphabets, check_is_valid_url
from app.api.v2.models import user_model
from validate_email import validate_email


auth_route = Blueprint('auth',__name__,url_prefix='/api/v2/auth')

user = user_model.User()

@auth_route.route('/signup',methods=['POST'])
def register():

    """
    method to register user and add them into the database
    """

    data = request.get_json()

    if not data:
        return format_response(400,"Missing credentials")

    
    try:
        email = data["email"]
    except KeyError:
        return make_response(jsonify({
                    "error": "Please supply an email to be able to register an attendant"
                    }), 400)

    try:
        request_password = data["password"]
    except KeyError:
        return make_response(jsonify({
                    "error": "Please supply a password to be able to register an attendant"
                    }), 400)

    if not isinstance(data["email"], str):
        return make_response(jsonify({
                    "error": "Email should be a string"
                    }), 400)

    if not isinstance(data["password"], str):
        return make_response(jsonify({
                    "error": "Password should be a string"
                    }), 400)
    firstname = data["firstname"]
    lastname = data["lastname"]
    othername = data["othername"]
    phoneNumber = data["phoneNumber"]
    passportUrl = data["passportUrl"]


    if(validate_phone_number(phoneNumber) == False):
        return return_error(400, "Phone number must be atleast 10 digits register and contain only digits")

    if(validate_string(firstname) == False):
        return return_error(400,"Firstname must be a string")
    if(validate_string(lastname) == False):
        return return_error(400,"Lastname must be a string")
    if(validate_string(firstname) == False):
        return return_error(400,"Othername must be a string")

    if(firstname == ""):
        return return_error(400,"Firstname cannot be empty")
    if(lastname == ""):
        return return_error(400,"Lastname cannot be empty")
    if(othername == ""):
        return return_error(400,"Othername cannot be empty")
    if(passportUrl == ""):
        return return_error(400,"passportUrl cannot be empty")

    if(validate_alphabets(firstname) == False):
        return return_error(400,"firstname can only contain letters") 
    if(validate_alphabets(lastname) == False):
        return return_error(400,"lastname can only contain letters") 
    if(validate_alphabets(othername) == False):
        return return_error(400,"othername can only contain letters")

    # validate_credentials(self,data)
    check_duplication("email", "users", email)
    # hash the user password
    hashed_password = generate_password_hash(request_password, method='sha256')

    user.save_user(firstname,lastname,othername,email,phoneNumber,passportUrl,hashed_password, False)

    return make_response(jsonify({
        "status":201,
        "error":"user successfully created"
    }),201)
    
@auth_route.route('/login',methods=['POST'])
def login():

    data = request.get_json()          
    if not data:
        return make_response(jsonify({
            "status":400,
            "error": "Kindly provide an email and a password to login"
        }
        ), 400)

    try:
        request_mail = data["email"]
    except:
        return make_response(jsonify({
            "status":400,
            "error": "Kindly provide an email address to log in"
            }), 400)

    try:
        request_password = data["password"]
    except:
        return make_response(jsonify({
            "status":400,
            "error": "Kindly provide a password to log in"
            }), 400)

    if not isinstance(data['email'], str):
            return make_response(jsonify({
            "status":400,
            "error": "E-mail should be a string"
        }
        ), 406)

    if not isinstance(data['password'], str):
            return make_response(jsonify({
            "error": "Password should be a string"
        }
        ), 406)

    request_email = request_mail.strip()                   
    user = user_model.User.fetch_user(request_email)
    
    if user and request_email == user[0]['email'] and check_password_hash(user[0]['password'], request_password):
        token = jwt.encode({
            "email": request_email,
            "user_id": user[0]['user_id'],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, os.getenv('JWT_SECRET_KEY', default='SdaHv342nx!jknr837bjwd?c,lsajjjhw673hdsbgeh'))
        return make_response(jsonify({
                        "status": 200,
                        "token": token.decode("UTF-8")}), 200)

    return make_response(jsonify({
        "error": "Try again. E-mail or password is incorrect!",
        "status":403
    }
    ), 403)
