
import json
from flask import current_app
from app.api.v2.tests import base_tests
from . import helper_functions
from app.api.v2.tests.helper_functions import convert_response_to_json

class TestCandidates(base_tests.TestBaseClass):
    """
    A class to test candidate's endpoints
    :param: object of the TestBaseClass
    """


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

        token = convert_response_to_json(response)['token']
        return token

        

    def test_candidate(self):
        """
        Method to test candidate registration
        """
        add_party = self.app_test_client.post('api/v2/parties',json=self.PARTY, headers=dict(Authorization = self.log_user()))
        add_office = self.app_test_client.post('api/v2/offices',json=self.OFFICE, headers=dict(Authorization = self.log_user()))
        response = self.app_test_client.post('api/v2/candidates',json=self.Candidate, headers=dict(Authorization = self.log_user()), content_type='application/json')

        self.assertEqual(response.status_code, 201)

    def test_candidate_no_token(self):
        """
        Method to test candidate registration with no auth token
        """
        add_party = self.app_test_client.post('api/v2/parties',json=self.PARTY)
        add_office = self.app_test_client.post('api/v2/offices',json=self.OFFICE)
        response = self.app_test_client.post('api/v2/candidates',json=self.Candidate, headers=dict(Authorization = ""), content_type='application/json')

        self.assertEqual(response.status_code,401)
    
    def test_candidate_invalid_token(self):
        """
        Method to test candidate registration with invalid token
        """
        add_party = self.app_test_client.post('api/v2/parties',json=self.PARTY)
        add_office = self.app_test_client.post('api/v2/offices',json=self.OFFICE)
        response = self.app_test_client.post('api/v2/candidates',json=self.Candidate, headers=dict(Authorization = "invalid_token"), content_type='application/json')

        self.assertEqual(response.status_code,403)
    
    def test_candidate_with_no_office(self):
        """
        Method to test candidate registration without existing offices
        """
        add_party = self.app_test_client.post('api/v2/parties',json=self.PARTY)
        response = self.app_test_client.post('api/v2/candidates',json=self.Candidate, headers=dict(Authorization = self.log_user()), content_type='application/json')

        self.assertEqual(response.status_code,400)
            
    def test_candidate_with_no_party(self):
        """
        Method to test candidate registration with no existing parties
        """
        add_office = self.app_test_client.post('api/v2/offices',json=self.OFFICE)
        response = self.app_test_client.post('api/v2/candidates',json=self.Candidate, headers=dict(Authorization = self.log_user()), content_type='application/json')

        self.assertEqual(response.status_code,400)