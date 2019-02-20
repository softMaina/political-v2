import re
from flask import jsonify, make_response,abort
from validate_email import validate_email
from app.api.v2 import database

def format_response(status_code, msg, data=list()):

    response = {
        "status":status_code,
        "message": msg,
        "data":data
    }
    return make_response(jsonify(response),status_code)

def check_duplication(column, table, value):
    """Checks for a value duplication

    Aborts if there is a duplication
    """
    
    query = """
    SELECT {} FROM {} WHERE LOWER({}) = LOWER('{}')
    """.format(column, table, column, value)

    duplicated = database.select_from_db(query)

    if duplicated:
        abort(make_response(jsonify(
            message="Record already exists in the database"), 400))

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
    """ check if input is of alphanumeric characters """
    if input_data.isalpha() == False:
        return False
def validate_ints(data):
    """ensures that data is of integer data type"""
    if not isinstance(data, int):
        return False
    return True

def validate_string(data):
    """ Ensure data is of a string data type """
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
    request_keys = ["name", "hqaddress", "logoUrl"]
    errors = []
    for key in request_keys:
        if not key in request.json:
            errors.append(key)
    return errors

def validate_office_json_keys(request):
    request_keys = ["name","office_type"]

    errors = []
    for key in request_keys:
        if not key in request.json:
            errors.append(key)
    return errors

def validate_phone_number(phone_number):
    if len(phone_number) != 10:
        return False 
    if not phone_number.isdigit():
        return False
    return True

def return_error(status_code, message):
    """ function to format response """
    response = {
        "status":status_code,
        "error": message
    }
    return make_response(jsonify(response),status_code)
def validate_alphabets(user_input):
    if not user_input.isalpha():
        return False
    return True

def validate_office_types(office_type):
    office_types = ["local","federal","state", "legistlative"]
    if office_type not in office_types:
        return False
    return True
