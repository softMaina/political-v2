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
    elif len(self.password) < 6 or len(self.password) > 12:
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