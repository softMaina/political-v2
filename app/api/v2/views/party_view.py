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
