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
    
    @staticmethod
    def fetch_user(email):
        select_user_by_email = """
        SELECT * FROM users
        WHERE email = '{}'""".format(email)

        return database.select_from_db(select_user_by_email)
    
    @staticmethod
    def check_candidature(candidate):
        #candidate should not be registered to more than one office and with more than one party
        query = """SELECT * FROM candidates WHERE candidate = '{}'""".format(candidate)

        number_of_rows = database.select_from_db(query)

        if number_of_rows > 1:
            return False
        
        return True
    @staticmethod
    def check_if_admin(user_id):

        query = """SELECT * FROM users WHERE user_id = '{}'""".format(user_id)

        user_data = database.select_from_db(query)
        
        isAdmin = user_data[0]['isadmin']

        if(isAdmin == True):
            return True
        
        return False