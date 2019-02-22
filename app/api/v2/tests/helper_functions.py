"""
Helper functions
"""
import json 

def convert_response_to_json(response):
    """
    A method to convert server responses to json format
    :param: the response object """

    json_response = json.loads(response.data.decode('utf-8'))

    return json_response