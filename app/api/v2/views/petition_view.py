from flask import Flask, make_response, abort, jsonify, Blueprint,request
from app.api.v2.models import petition_model
from app.api.v2 import database
import datetime

petition = petition_model.Petition()

petition_route = Blueprint('petition',__name__,url_prefix='/api/v2/petition')
@petition_route.route('/add',methods=['POST'])
def save():

    try:
        data = request.get_json(force=True)
    except:
        return make_response(jsonify({
            "status":400,
            "message":"ensure your content type is application/json"
        })),400  
    createdOn = datetime.datetime.utcnow()
    createdBy = data["createdBy"] #voter
    office = data["office"]
    body = data["body"] 

    petition.save(createdOn, createdBy, office,body)

    return make_response(jsonify({
            "message": "Your candidature was accepted successfully",
            "petition": {
                "office":office,
                "body": body,
                "user":createdBy
            }
        }), 201)

@petition_route.route('',methods=['GET'])
def get_votes():

    petitions = petition.fetch_all_petitions()

    if not petitions:

        return make_response(jsonify({
            'status':404,
            'msg':'there are no filed petitions yet'
        }),404)
    
    response = jsonify({
            'message': "Successfully fetched all the offices",
            'products': petitions
            })

    response.status_code = 200
    return response


