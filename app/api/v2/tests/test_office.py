""" office tests """
import json

from flask import current_app

from app.api.v2.tests import base_tests
from . import helper_functions


class TestOffices(base_tests.TestBaseClass):


    def register_user(self):
        """
        user registration
        :Response: status 201, data, user_data
        """
        response = self.app_test_client.post('api/v2/auth/register', json=self.Admin)
        
        return response.status_code


    def log_user(self):
        """
        Method to login
        :Response: auth_token
        """
        response1 = self.app_test_client.post('/api/v2/auth/signup',json=self.Admin)
        response = self.app_test_client.post('/api/v2/auth/login',json=self.admin_login)

        token = helper_functions.convert_response_to_json(response)['token']
        return token

    def test_get_offices(self):
        response1 = self.app_test_client.post('/api/v2/offices',json=self.OFFICE,headers=dict(Authorization = self.log_user()))

        response = self.app_test_client.get('/api/v2/offices')

        self.assertEqual(response.status_code,200)
    
    def test_add_office(self):

        response = self.app_test_client.post('/api/v2/offices',json=self.OFFICE,headers=dict(Authorization = self.log_user()))

        self.assertEqual(response.status_code, 201)
    
    def test_get_specific_office(self):

        response1 = self.app_test_client.post('/api/v2/offices',json=self.OFFICE,headers=dict(Authorization = self.log_user()))

        response = self.app_test_client.get('/api/v2/offices/1')

        self.assertEqual(response.status_code, 200)
    
    def test_update_office(self):
        response1 = self.app_test_client.post('/api/v2/offices',json=self.OFFICE,headers=dict(Authorization = self.log_user()))

        response = self.app_test_client.put('/api/v2/offices/1',json=self.update_office,headers=dict(Authorization = self.log_user()))

        self.assertEqual(response.status_code, 200)
        
    def test_delete_office(self):
        response1 = self.app_test_client.post('/api/v2/offices',json=self.OFFICE,headers=dict(Authorization = self.log_user()))
        response = self.app_test_client.delete('/api/v2/offices/1',headers=dict(Authorization = self.log_user()))

        self.assertEqual(response.status_code, 200)

    def test_add_office_wrong_type(self):

        response = self.app_test_client.post('/api/v2/offices',json=self.Wrong_office_type,headers=dict(Authorization = self.log_user()))

        self.assertEqual(response.status_code, 400)