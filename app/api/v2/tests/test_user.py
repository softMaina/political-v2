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
