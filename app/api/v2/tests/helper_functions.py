import json 

def convert_response_to_json(response):
    """ converts the response to json type"""

    json_response = json.loads(response.data.decode('utf-8'))

    return json_response