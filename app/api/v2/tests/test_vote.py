import json
from flask import current_app
from app.api.v2.tests import base_tests
from . import helper_functions
from app.api.v2.tests.helper_functions import convert_response_to_json

class TestVotes(base_tests.TestBaseClass):
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

    def add_candidate(self):
        add_party = self.app_test_client.post('api/v2/parties',json=self.PARTY, headers=dict(Authorization = self.log_user()))
        add_office = self.app_test_client.post('api/v2/offices',json=self.OFFICE,headers=dict(Authorization = self.log_user()))
        response = self.app_test_client.post('api/v2/candidates',json=self.Candidate, headers=dict(Authorization = self.log_user()), content_type='application/json')

        return response

    def test_vote(self):
        post_candidate = self.add_candidate()
        response = self.app_test_client.post('api/v2/votes',json={
            "candidate":1
        }, headers=dict(Authorization = self.log_user()))

        self.assertEqual(response.status_code, 201)
    
    def test_vote_no_token(self):
        post_candidate = self.add_candidate()
        response = self.app_test_client.post('api/v2/votes',json={
            "candidate":1
        }, headers=dict(Authorization = ""))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(convert_response_to_json(response)['Message'], "You need to login")

    def test_vote_no_office(self):
        response = self.app_test_client.post('api/v2/votes',json={
            "candidate":1
        }, headers=dict(Authorization = self.log_user()))

        self.assertEqual(response.status_code,400)
    def test_vote_twice(self):
        post_candidate = self.add_candidate()
        response = self.app_test_client.post('api/v2/votes',json={
            "candidate":1
        }, headers=dict(Authorization = self.log_user()))
        #second vote
        response1 = self.app_test_client.post('api/v2/votes',json={
            "candidate":1
        }, headers=dict(Authorization = self.log_user()))

        self.assertEqual(response1.status_code, 201)
    
    def test_vote_empty_data(self):
        response = self.app_test_client.post('api/v2/votes',json={
            "candidate":1
        }, headers=dict(Authorization = self.log_user()),content_type="text")

        self.assertEqual(response.status_code, 400)

    def test_vote_string_data(self):
        response = self.app_test_client.post('api/v2/votes',json={
            "candidate":"one"
        }, headers=dict(Authorization = self.log_user()),content_type="text")

        self.assertEqual(response.status_code, 400)

