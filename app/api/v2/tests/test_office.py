""" office tests """
import json

from flask import current_app

from app.api.v2.tests import base_tests
from . import helper_functions

class TestOffices(base_tests.TestBaseClass):


    def test_get_offices(self):
        response1 = self.app_test_client.post('/api/v2/offices',json=self.OFFICE)

        response = self.app_test_client.get('/api/v2/offices')

        self.assertEqual(response.status_code,200)
    
    def test_add_office(self):

        response = self.app_test_client.post('/api/v2/offices',json=self.OFFICE)

        self.assertEqual(response.status_code, 201)
    
    def test_get_specific_office(self):

        response1 = self.app_test_client.post('/api/v2/offices',json=self.OFFICE)

        response = self.app_test_client.get('/api/v2/offices/1')

        self.assertEqual(response.status_code, 200)
    
    def test_update_office(self):
        response1 = self.app_test_client.post('/api/v2/offices',json=self.OFFICE)

        response = self.app_test_client.put('/api/v2/offices/1',json=self.OFFICE)

        self.assertEqual(response.status_code, 201)
        
    def test_delete_office(self):
        response1 = self.app_test_client.post('/api/v2/offices',json=self.OFFICE)
        response = self.app_test_client.delete('/api/v2/offices/1')

        self.assertEqual(response.status_code, 200)
