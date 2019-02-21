from flask import Flask, make_response, abort, jsonify, Blueprint,request
from app.api.v2.models import vote_model
from app.api.v2 import database
import json
from app.api.v2.utils.validator import return_error 
from app.api.v2.utils.verify import verify_tokens
from app.api.v2.utils.validator import validate_ints, return_error
import datetime

vote = vote_model.Vote()
# vote = json.loads(vote)

vote_route = Blueprint('vote',__name__,url_prefix='/api/v2/')
@vote_route.route('/votes',methods=['POST'])
def save():
    """ save user vote """
    user_email, user_id = verify_tokens()
   
    try:
        data = request.get_json(force=True)
    except:
        return make_response(jsonify({
            "status":400,
            "message":"ensure your content type is application/json"
        })),400  
    createdOn = datetime.datetime.utcnow()
    createdBy = user_id
    candidate = data["candidate"]



    if(validate_ints(candidate) == False):
        return return_error(400, "candidate data must be of type integer")

    candidate_office = """SELECT office FROM candidates WHERE candidate_id = '{}'""".format(candidate)

    office = database.select_from_db(candidate_office)

    if not office:
        return return_error(400,"Wrong candidate data")

    office_id = office[0]['office']


    # user cannot vote for same office twice 
    # check that the database does not have more that one column with same office and candidate by the same user
    vote_once_query = """SELECT createdby, office, candidate FROM votes WHERE createdBy = '{}' AND office = '{}' AND candidate = '{}' """.format(createdBy,office_id,candidate)
    
    vote_results = database.select_from_db(vote_once_query)

    vote_results_len = len(vote_results)

    if vote_results_len > 1:
        return return_error(400,"You cannot vote more than once for the same office")
  
    vote.save(createdOn, createdBy, office_id, candidate)

    return make_response(jsonify({
            "status":201,
            "data": {
                "time voted":createdOn,
                "to office": office_id,
                "party": candidate,
                "voting user":createdBy
            }
        }), 201)

@vote_route.route('votes',methods=['GET'])
def get_votes():
    """
        get all the votes
    """

    votes = vote_model.Vote()

    all_votes = votes.fetch_all_votes()

    if not all_votes:

        return make_response(jsonify({
            'status':404,
            'msg':'Voting hasnt begun'
        }),404)
    
    return make_response(jsonify({
        'status':200,
        'data':all_votes
    }))

