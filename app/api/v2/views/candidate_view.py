from flask import Flask, make_response, abort, jsonify, Blueprint,request
from app.api.v2.models import candidate_model
from app.api.v2 import database
from app.api.v2.utils.validator import return_error, validate_candidate_json_keys
from app.api.v2.utils.verify import verify_tokens


CANDIDATE = candidate_model.Candidate()

candidate_route = Blueprint('candidate',__name__,url_prefix='/api/v2/')
@candidate_route.route('candidates',methods=['POST'])
def save():
    """"
     add a candidate
    """


    user_email, user_id = verify_tokens()

    json_keys =validate_candidate_json_keys(request)

    if json_keys:
        return return_error(400, "Missing keys {}".format(json_keys))

    try:
        data = request.get_json(force=True)
    except:
        return make_response(jsonify({
            "status":400,
            "message":"ensure your content type is application/json"
        })),400  
    office = data["office"]
    party = data["party"] 
    user = user_id

    if not isinstance(office, int):
        return return_error(400,"Office must be an integer value")

    if not isinstance(party, int):
        return return_error(400, "Party must be an integer value")

    #check candidate registrations
    candidate_data = CANDIDATE.check_candidature(user_id)

    office_data = CANDIDATE.check_office(office)

    party_data = CANDIDATE.check_party(party)

    if len(office_data) < 1:
        return return_error(400,"Office doesn't not exist")

    if len(party_data) < 1:
        return return_error(400,"Party doesn't not exist")
    
    
    candidate_len = len(candidate_data)

    if candidate_len > 1:
        return return_error(400,"You have already registered as a candidate")

    CANDIDATE.save(office, party, user)

    return make_response(jsonify({
            "message": "Your candidature was accepted successfully",
            "office": {
                "office":office,
                "party": party,
                "user":user
            }
        }), 201)

