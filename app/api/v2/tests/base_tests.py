import os
import unittest

from app.api.v2.tests.helper_functions import convert_response_to_json
from app import create_app
from app.api.v2.database import init_db
from instance.config import config

class TestBaseClass(unittest.TestCase):
    """ Base test class """

    
    def setUp(self):
        self.app = create_app(os.getenv('FLASK_ENV'))
        self.BASE_URL = 'api/v2'
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app_test_client = self.app.test_client()
        self.app.testing = True

        with self.app.app_context():
            self.db_url  = config['test_db_url']
            init_db(self.db_url)

        self.Candidate = {
            "office":7,
	        "party":5
        }

        self.User = {
            "firstname":"dffewf",
            "lastname" :"Fdfdsa",
            "othername":"asfdfdsa",
            "email":"www@gmail.com",
            "phoneNumber":"4444478043",
            "password":"password",
            "passportUrl":"www.img.com/passport"
        }
        self.User_wrong_name = {
            "firstname":"dff2wf",
            "lastname" :"Fdfdsa",
            "othername":"asfdfdsa",
            "email":"www@gmail.com",
            "phoneNumber":"4444478043",
            "password":"password",
            "passportUrl":"www.img.com/passport"
        }
        self.user_login = {
            "email":"www@gmail.com",
            "password":"password"
        }
        self.user_login_wrong = {
            "email":"wrong@gmail.com",
            "password":"password"
        }

        self.PARTY = {
            'id':1,
            'name':'Jubilee',
            'hqaddress':'Tuko Pamoja',
            'logoUrl':'www.youtube.com'
        }
        self.OFFICE = {
            'name':'ward',
            'office_type':'state'
        }
        self.wrong_office_name = {
            'id':1,
            'name':2,
            'office_type':'federal'
        }
        self.wrong_party_name = {
            'id':1,
            'name':2,
            'hqaddress':'Tuko pamoja',
            'logoUrl':'www.youtube.com'
        }
        self.wrong_office_type = {
            'id':1,
            'name':'urp',
            'office_type':3
        }
        self.invalid_keys = {
            'id':1,
            'names':'urp',
            'office_type':'neeat'
        }

    

    def tearDown(self):
        self.app_context.pop()

    
    

if __name__ == '__main__':
    unittest.main()