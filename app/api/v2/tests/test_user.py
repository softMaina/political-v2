import json
from flask import current_app
from app.api.v2.tests import base_tests
from . import helper_functions

class TestUsers(base_tests.TestBaseClass):


    def test_signup(self):
        """
        Test adding a candidate
        """
        response = self.app_test_client.post('/api/v2/auth/signup',json=self.User)

        self.assertEqual(response.status_code,201)

    def test_signup_empty_name(self):

        response = self.app_test_client.post('/api/v2/auth/signup',json=self.User_wrong_name)

        self.assertEqual(response.status_code,400)

    
    def test_login(self):
        response1 = self.app_test_client.post('/api/v2/auth/signup',json=self.User)
        response = self.app_test_client.post('/api/v2/auth/login',json=self.user_login)

        self.assertEqual(response.status_code,200)
    
    def test_login_wrong_user(self):
        response1 = self.app_test_client.post('/api/v2/auth/signup',json=self.User)
        response = self.app_test_client.post('/api/v2/auth/login',json=self.user_login_wrong)

        self.assertEqual(response.status_code,401)
    
    def test_missing_keys(self):
        response = self.app_test_client.post('/api/v2/auth/signup',json=self.user_missing_Key)

        self.assertEqual(response.status_code,400)
    def test_missing_data(self):
        response = self.app_test_client.post('/api/v2/auth/signup',json={})

        self.assertEqual(response.status_code,400)
    def test_int_email(self):
        response = self.app_test_client.post('/api/v2/auth/signup',json={
            "firstname":"dffewf",
            "lastname" :"Fdfdsa",
            "othername":"asfdfdsa",
            "email":1,
            "phoneNumber":"4444478043",
            "password":"password",
            "passportUrl":"www.img.com/passport"
        })

        self.assertEqual(response.status_code,400)

    def test_int_password(self):
        response = self.app_test_client.post('/api/v2/auth/signup',json={
            "firstname":"dffewf",
            "lastname" :"Fdfdsa",
            "othername":"asfdfdsa",
            "email":"email",
            "phoneNumber":"4444478043",
            "password":1,
            "passportUrl":"www.img.com/passport"
        })

        self.assertEqual(response.status_code,400)