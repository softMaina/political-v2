from flask import Flask, make_response, abort, jsonify, Blueprint,request
from app.api.v2.models import vote_model
from app.api.v2 import database
from app.api.v2.utils.verify import verify_tokens
from app.api.v2.utils.validator import validate_ints, return_error
import datetime
vote = vote_model.Vote()

vote_route = Blueprint('vote',__name__,url_prefix='/api/v2/vote')
@vote_route.route('/add',methods=['POST'])
def save():
    """ save user vote """
    # user_email, user_id = verify_tokens()

   
    try:
        data = request.get_json(force=True)
    except:
        return make_response(jsonify({
            "status":400,
            "message":"ensure your content type is application/json"
        })),400  
    createdOn = datetime.datetime.utcnow()
    createdBy = data["createdBy"] #voter
    candidate = data["candidate"] 

    if(validate_ints(candidate) == False):
        return return_error(400, "candidate data must be of type integer")

    vote.save(createdOn, createdBy, candidate)

    return make_response(jsonify({
            "status":201,
            "message": "Your vote was accepted successfully",
            "data": {
                "party": candidate,
                "user":createdBy
            }
        }), 201)

@vote_route.route('',methods=['GET'])
def get_votes():
    """
        get all the votes
    """

    votes = vote_model.Vote()

    all_votes = votes.fetch_all_votes()

    if not all_votes:

        return make_response(jsonify({
            'status':404,
            'msg':'there are no registered aspirants yet'
        }),404)
    
    response = jsonify({
            'message': "Successfully fetched all the offices",
            'products': all_votes
            })

    response.status_code = 200
    return response

