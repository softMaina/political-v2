"""
Implement data validations
"""

import re
from flask import jsonify, make_response,abort
from validate_email import validate_email
from app.api.v2 import database

def format_response(status_code, msg, data=list()):
    """
    Method to format responses in a json format
    :params: status_code, message, data
    :response: json object
    """
    response = {
        "status":status_code,
        "message": msg,
        "data":data
    }
    return make_response(jsonify(response),status_code)

def check_duplication(column, table, value):
    """
    Method to check for a value duplication
    :params: table column, table and variable value
    Aborts if there is a duplication
    """
    
    query = """
    SELECT {} FROM {} WHERE LOWER({}) = LOWER('{}')
    """.format(column, table, column, value)

    duplicated = database.select_from_db(query)

    if duplicated:
        abort(make_response(jsonify({
            "status":400,
            "error":"Record already exists in the database"}), 400))

def validate_credentials(self, data):
    """Validate email, password and role fields"""

    self.email = data["email"].strip()
    self.password = data["password"].strip()
    valid_email = validate_email(self.email)

    if not valid_email:
        Message = "Please supply a valid email"
        abort(400, Message)
    elif len(self.password) < 6 or len(self.password) > 6:
        Message = "Password must be long than 6 characters or less than 12"
        abort(400, Message)
    elif not any(char.isdigit() for char in self.password):
        Message = "Password must have a digit"
        abort(400, Message)
    elif not any(char.isupper() for char in self.password):
        Message = "Password must have an upper case character"
        abort(400, Message)
    elif not any(char.islower() for char in self.password):
        Message = "Password must have a lower case character"
        abort(400, Message)
    elif not re.search("^.*(?=.*[@#$%^&+=]).*$", self.password):
        Message = "Password must have a special charater"
        abort(400, Message)

def sanitize_input(input_data):
    """ 
    Method to sanitize data input
    :params: user_data
    Check if it is alphanumeric
    :response: True, False 
    """
    if input_data.isalpha() == False:
        return False

def validate_ints(data):
    """
    Method to validate data of type integer
    :params: data
    :response: True, False
    """
    if not isinstance(data, int):
        return False
    return True

def validate_string(data):
    """
    Method to validate data of type string
    :params: user input
    :response: True, False 
    """
    if not isinstance(data, str):
        return False
    return True

def check_field_is_not_empty(input_data):

    if input_data == "":
        return False

def strip_whitespace(input_data):
    input_data = input_data.strip()
    return input_data

def check_is_valid_url(url):
    """check if the url provided is valid"""
    if re.match(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)",
               url):
       return True
    return False

def validate_party_json_keys(request):
    """
    Method to validate request keys
    :params: request
    :response: error array
    """
    request_keys = ["name", "hqaddress", "logoUrl"]
    errors = []
    for key in request_keys:
        if not key in request.json:
            errors.append(key)
    return errors

def validate_office_json_keys(request):
    """
    Method to validate request keys
    :params: request
    :response: error array
    """
    request_keys = ["name","office_type"]

    errors = []
    for key in request_keys:
        if not key in request.json:
            errors.append(key)
    return errors

def validate_phone_number(phone_number):
    """
    Method to validate phone number
    :params: phone number 
    :response: boolean
    """
    if len(phone_number) != 10:
        return False 
    if not phone_number.isdigit():
        return False
    return True

def return_error(status_code, message):
    """
    Method to format error message
    :params: status_code, error message
    :response: json object
    """
    response = {
        "status":status_code,
        "error": message
    }
    return make_response(jsonify(response),status_code)

def validate_alphabets(user_input):
    """
    Method to validate that a string contains letters only
    :response:boolean
    :params: user data, string
    """
    if not user_input.isalpha():
        return False
    return True

def validate_office_types(office_type):
    """
    Method to validate office types
    :params: office type
    :response: boolean
    """
    office_types = ["local","federal","state", "legistlative"]
    if office_type not in office_types:
        return False
    return True
def validate_user_json_keys(request):

    request_keys = ["firstname", "lastname", "othername","email","phoneNumber","password","passportUrl"]
    errors = []

    for key in request_keys:
        if not key in request.json:
            errors.append(key)
    return errors
def check_if_admin_key(request):
    admin_key = ["isAdmin","isAdmin","isAdmin","isAdmin","isAdmin","isAdmin","isAdmin","isAdmin","isAdmin"]
    
    for key in admin_key:
        if not key in request.json:
            return False
    return True

def validate_candidate_json_keys(request):
    """
    Method to validate request keys
    :params: request
    :response: error array
    """
    request_keys = ["office","party"]

    errors = []
    for key in request_keys:
        if not key in request.json:
            errors.append(key)
    return errors

def sanitize_data(data):
    errors=[]
    for item in data:
        if item == "":
            errors.append(item)
    return errors
