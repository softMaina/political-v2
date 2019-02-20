import json

from flask import current_app

from app.api.v2.tests import base_tests

class TestParties(base_tests.TestBaseClass):
    # class contains tests for party endpoints
    
    """
     Class to test party endpoints
    """
    
    def test_get_parties(self):
      
        response1 = self.app_test_client.post('/api/v2/parties',json=self.PARTY)

        response = self.app_test_client.get('/api/v2/parties',json=self.PARTY)


        self.assertEqual(response.status_code,200)

        
    def test_add_party(self):
        response = self.app_test_client.post('/api/v2/parties',json=self.PARTY)

        self.assertEqual(response.status_code, 201)
   
    def test_get_specific_office(self):

        response1 = self.app_test_client.post('/api/v2/parties',json=self.PARTY)

        response = self.app_test_client.get('/api/v2/parties/1')

        self.assertEqual(response.status_code, 200)
    
    def test_update_office(self):
        response1 = self.app_test_client.post('/api/v2/parties',json=self.PARTY)

        response = self.app_test_client.put('/api/v2/parties/1',json=self.PARTY)

        self.assertEqual(response.status_code, 201)
        
    def test_delete_office(self):
        response1 = self.app_test_client.post('/api/v2/parties',json=self.PARTY)
        response = self.app_test_client.delete('/api/v2/parties/1')

        self.assertEqual(response.status_code, 200)