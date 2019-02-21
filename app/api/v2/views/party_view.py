"""
    Party endpoints
"""
from flask import Flask, make_response, abort, jsonify, Blueprint,request
from app.api.v2.models import party_model
from app.api.v2.models import user_model
from app.api.v2 import database
from app.api.v2.utils.verify import verify_tokens
from app.api.v2.utils.validator import validate_party_json_keys, return_error, validate_string, strip_whitespace, check_duplication, validate_ints

PARTY = party_model.Party()
USER = user_model.User()
party_route = Blueprint('party',__name__,url_prefix='/api/v2')

@party_route.route('/parties',methods=['POST'])
def save():
    """
    Save a party into the database
    method: POST
    """
    # check if is admin
    user_email, user_id = verify_tokens()

    if(USER.check_if_admin(user_id) == False):
        return return_error(401,"Must be an admin to add party")
    #validate json keys
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

    name = name.replace("","")
    hqaddress = hqaddress.strip()
    logoUrl = logoUrl.strip()

    if(name == ""):
        return return_error(400,"Name cannot be empty")

    if(hqaddress == ""):
        return return_error(400,"Hqaddress cannot be empty")

    if(logoUrl == ""):
        return return_error(400,"LogoUrl cannot be empty")

  

    name = strip_whitespace(name)
    hqaddress = strip_whitespace(hqaddress)
    logoUrl = strip_whitespace(logoUrl)

    #check if party with same name exists, if true, abort
    check_duplication("name","parties", name)


    PARTY.save(name, hqaddress,logoUrl)

    return make_response(jsonify({
            "status": 201,
            "party": {
                "name":name,
                "hqaddress": hqaddress,
                "logoUrl": logoUrl
            }
        }), 201)


@party_route.route('parties/<int:party_id>',methods=['DELETE'])
def delete(party_id):
    """
    Delete a political party
    :params: party id
    """

     # check if is admin
    user_email, user_id = verify_tokens()

    if(USER.check_if_admin(user_id) == False):
        return return_error(401,"Must be an admin to delete party")
    if(validate_ints(party_id) == False):
        return return_error(400, "Wrong parameters party id {}").format(party_id)

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

@party_route.route('parties',methods=['GET'])
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

@party_route.route('parties/<int:party_id>',methods=['GET'])
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
@party_route.route('parties/<int:party_id>',methods=['PUT'])
def update(party_id): 
    """ candidate can update a party """

     # check if is admin
    user_email, user_id = verify_tokens()

    if(USER.check_if_admin(user_id) == False):
        return return_error(401,"Must be an admin to update party")
    #validate json keys

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

    name = strip_whitespace(name)
    hqaddress = strip_whitespace(hqaddress)
    logoUrl = strip_whitespace(logoUrl)

    #check if party with same name exists, if true, abort
    check_duplication("name","parties", name)
    check_duplication("logoUrl","parties", logoUrl)
    check_duplication("hqaddress","parties", hqaddress)

    PARTY.update(id, name, hqaddress, logoUrl)

    return make_response(jsonify({
            "status": 200,
             "data": {
                "name":name,
                "hqaddress": hqaddress,
                "logoUrl": logoUrl
            }
        }), 200)