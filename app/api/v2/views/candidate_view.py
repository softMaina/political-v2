from flask import Flask, make_response, abort, jsonify, Blueprint,request
from app.api.v2.models import candidate_model
from app.api.v2 import database
from app.api.v2.utils.verify import verify_tokens

CANDIDATE = candidate_model.Candidate()

candidate_route = Blueprint('candidate',__name__,url_prefix='/api/v2/')
@candidate_route.route('candidates',methods=['POST'])
def save():

    user_email, user_id = verify_tokens()

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

    CANDIDATE.save(office, party, user)

    return make_response(jsonify({
            "message": "Your candidature was accepted successfully",
            "office": {
                "office":office,
                "party": party,
                "user":user
            }
        }), 201)


@candidate_route.route('/update/<int:candidate_id>',methods=['PUT'])
def update(candidate_id): 
    try:
        data = request.get_json(force=True)
    except:
        return make_response(jsonify({
            'status':400,
            'msg':'data should be in json format'
        }),400)  
    id=candidate_id
    office = data["office"]
    party = data["party"]
    user = data["user"]

    
    CANDIDATE.update(id, office, party, user)

    return make_response(jsonify({
            "message": "office updated successfully",
            "office": {
                "office":office,
                "party": party,
                "user":user
            }
        }), 201)

@candidate_route.route('',methods=['GET'])
def get_candidates():

    candidates = candidate_model.Candidate()

    aspirants= candidates.fetch_all_candidates()
    if not aspirants:

        return make_response(jsonify({
            'status':404,
            'msg':'there are no registered aspirants yet'
        }),404)
    
    response = jsonify({
            'message': "Successfully fetched all the offices",
            'products': aspirants
            })

    response.status_code = 200
    return response

@candidate_route.route('delete/<int:candidate_id>',methods=['DELETE'])
def delete(candidate_id):
    query = """SELECT * FROM candidates WHERE candidate_id = {} """.format(candidate_id)
    office = database.select_from_db(query)
        
    if not office:
        return make_response(jsonify({
        "message": "Candidate with id {} does not exist".format(candidate_id)
        }), 404)


    CANDIDATE.delete(candidate_id)

    return make_response(jsonify({
        "message": "Product deleted successfully"
    }), 200)

@candidate_route.route('getcandidate/<int:candidate_id>',methods=['GET'])
def get_specific_candidate(candidate_id):
    query = """SELECT * FROM candidates WHERE candidate_id = '{}'""".format(candidate_id)

    candidate = database.select_from_db(query)
    if not candidate:
        return make_response(jsonify({
        "message": "Candidate with id {} is not available".format(candidate_id),
        }), 404)
    
    return make_response(jsonify({
        "message": "{} retrieved successfully".format(candidate[0]['office']),
        "candidate": candidate
        }), 200)