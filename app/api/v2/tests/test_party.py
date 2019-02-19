import json

from flask import current_app

from app.api.v2.tests import base_tests

class TestParties(base_tests.TestBaseClass):
    # class contains tests for party endpoints

    
    def test_get_parties(self):
      
        response1 = self.app_test_client.post('/api/v2/party/add',json=self.PARTY)

        response = self.app_test_client.get('/api/v2/party',json=self.PARTY)


        self.assertEqual(response.status_code,200)

        
    def test_add_party(self):
        response = self.app_test_client.post('/api/v2/party/add',json=self.PARTY)

        self.assertEqual(response.status_code, 201)
   