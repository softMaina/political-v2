from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from app.api.v2 import database

USERS = []
class User():
    """
    The v2 user model.
    """

    def __init__(self):
        """
            Constructor of the user class
            New user objects are created with this method
        """
        self.user = USERS

    def save_user(self,firstname,lastname, othername, email, phoneNumber,passportUrl,password,isAdmin):
        """
        Add a new user to the users table
        """
        users =  {
            'firstname': firstname,
            'lastname':lastname,
            'othername':othername,
            'email':email,
            'phoneNumber':phoneNumber,
            'passporturl': passportUrl,
            'password':password,
            'isAdmin': isAdmin
        }
        save_user_query = """
        INSERT INTO users(firstname, lastname, othername, email,phonenumber, passporturl, password,  isadmin) VALUES(
            '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'
        )""".format(firstname,lastname,othername,email,phoneNumber,passportUrl,password,isAdmin)

        database.insert_to_db(save_user_query)

        return users