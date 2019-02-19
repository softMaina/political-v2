from flask import Flask, make_response, abort, jsonify, Blueprint,request
from app.api.v2.models import party_model
from app.api.v2 import database

PARTY = party_model.Party()

party_route = Blueprint('party',__name__,url_prefix='/api/v2/party')
@party_route.route('/add',methods=['POST'])
def save():
    """
        get a political party and save it to the database
    """
    try:
        data = request.get_json(force=True)
    except:
        return make_response(jsonify({
            "status":400,
            "message":"ensure your content type is application/json"
        })),400  
    name = data["name"]
    hqaddress = data["hqaddress"]
    logoUrl = data["logoUrl"]

        

    PARTY.save(name, hqaddress,logoUrl)

    return make_response(jsonify({
            "message": "Party added successfully",
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
        "message": "Product deleted successfully"
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
            'msg':'there are no registered parties yer'
        }),404)
    
    response = jsonify({
            'message': "Successfully fetched all the products",
            'products': all_parties
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
        "message": "party with id {} is not available".format(party_id),
        }), 404)
    
    return make_response(jsonify({
        "message": "{} retrieved successfully".format(party[0]['name']),
        "product": party
        }), 200)