""" office tests """
import json

from flask import current_app

from app.api.v2.tests import base_tests
from . import helper_functions

class TestOffices(base_tests.TestBaseClass):


    def test_get_offices(self):
        response1 = self.app_test_client.post('/api/v2/office/add',json=self.OFFICE)

        response = self.app_test_client.get('/api/v2/office')

        self.assertEqual(response.status_code,200)
    
    def test_add_office(self):

        response = self.app_test_client.post('/api/v2/office/add',json=self.OFFICE)

        self.assertEqual(response.status_code, 201)
        
   