import json
from flask import current_app
from app.api.v2.tests import base_tests
from . import helper_functions

class TestCandidates(base_tests.TestBaseClass):

    def register_user(self):

        response = self.app_test_client.post('api/v2/auth/register', json=self.User)
        
        return response.status_code

    def login_user(self):
        response1 = self.register_user()
        response = self.app_test_client.post('api/v2/auth/login',json=self.login_user)

        token = response.json["data"]["token"]

        return {
            "Authorization":token
        }
    

