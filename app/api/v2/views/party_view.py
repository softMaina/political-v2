from flask import Flask, make_response, abort, jsonify, Blueprint,request
from app.api.v2.models import party_model
from app.api.v2 import database
from app.api.v2.utils.validator import validate_party_json_keys, return_error, validate_string, strip_whitespace

PARTY = party_model.Party()

party_route = Blueprint('party',__name__,url_prefix='/api/v2/party')
@party_route.route('/add',methods=['POST'])
def save():
    """
        get a political party and save it to the database
    """

    json_key_errors = validate_party_json_keys(request)

    if json_key_errors:
        return return_error(400, "missing keys {}".format(json_key_errors))

    try:
        data = request.get_json(force=True)
    except:
        return make_response(jsonify({
            "status":400,
            "error":"Ensure your content type is application/json"
        })),400  
    name = data["name"]
    hqaddress = data["hqaddress"]
    logoUrl = data["logoUrl"]

    name = name.replace("","")
    hqaddress = hqaddress.strip()
    logoUrl = logoUrl.strip()

    if(validate_string(name) == False):
        return return_error(400, "Name must be of type string")
    
    if(validate_string(hqaddress) == False):
        return return_error(400, "Hqaddress must be of type string")

    if(validate_string(logoUrl) == False):
        return return_error(400, "LogoUrl must be of type string")
    if(name == ""):
        return return_error(400,"Name cannot be empty")
    if(hqaddress == ""):
        return return_error(400,"Hqaddress cannot be empty")
    if(logoUrl == ""):
        return return_error(400,"LogoUrl cannot be empty")

    name = strip_whitespace(name)
    hqaddress = strip_whitespace(hqaddress)
    logoUrl = strip_whitespace(logoUrl)


    PARTY.save(name, hqaddress,logoUrl)

    return make_response(jsonify({
            "status": 201,
            "party": {
                "name":name,
                "hqaddress": hqaddress,
                "logoUrl": logoUrl
            }
        }), 201)

@party_route.route('delete/<int:party_id>',methods=['DELETE'])
def delete(party_id):
    """
        Delete a political party
    """
    query = """SELECT * FROM parties WHERE party_id = {} """.format(party_id)
    party = database.select_from_db(query)
        
    if not party:
        return make_response(jsonify({
        "message": "Party with id {} does not exist".format(party_id)
        }), 404)

    PARTY.delete(party_id)

    return make_response(jsonify({
        "status":200,
        "message": "Party deleted successfully"
    }), 200)
@party_route.route('',methods=['GET'])
def get_parties():
    """
        return all registered parties
    """
    parties = party_model.Party()

    all_parties = parties.fetch_all_parties()

    if not all_parties:
        return make_response(jsonify({
            'status':404,
            'error':'There are no registered parties yet'
        }),404)
    
    response = jsonify({
            'status': 200,
            'data': all_parties
            })

    response.status_code = 200
    return response

@party_route.route('getparty/<int:party_id>',methods=['GET'])
def get_specific_party(party_id):
    """
        Get a specific political party by id
    """
    query = """SELECT * FROM parties WHERE party_id = '{}'""".format(party_id)

    party = database.select_from_db(query)
    if not party:
        return make_response(jsonify({
        "status": 404,
        "error": "Party with id {} is not available".format(party_id),
        }), 404)
    
    return make_response(jsonify({
        "status": 200,
        "data": party
        }), 200)
@party_route.route('/update/<int:party_id>',methods=['PUT'])
def update(party_id): 
    """ candidate can update a party """

    json_key_errors = validate_party_json_keys(request)

    if json_key_errors:
        return return_error(400, "Missing keys {}".format(json_key_errors))


    try:
        data = request.get_json(force=True)
    except:
        return make_response(jsonify({
            'status':400,
            'error':'Data should be in json format'
        }),400)  
    id=party_id
    name = data["name"]
    hqaddress = data["hqaddress"]
    logoUrl = data["logoUrl"]


    if(validate_string(name) == False):
        return return_error(400, "Name must be of type string")
    
    if(validate_string(hqaddress) == False):
        return return_error(400, "Hqaddress must be of type string")

    if(validate_string(logoUrl) == False):
        return return_error(400, "LogoUrl must be of type string")
    if(name == ""):
        return return_error(400,"Name cannot be empty")
    if(hqaddress == ""):
        return return_error(400,"Hqaddress cannot be empty")
    if(logoUrl == ""):
        return return_error(400,"LogoUrl cannot be empty")

    PARTY.update(id, name, hqaddress, logoUrl)

    return make_response(jsonify({
            "status": 201,
             "data": {
                "name":name,
                "hqaddress": hqaddress,
                "logoUrl": logoUrl
            }
        }), 201)