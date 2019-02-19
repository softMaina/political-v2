from flask import Flask, make_response, abort, jsonify, Blueprint,request
from app.api.v2.models import office_model
from app.api.v2 import database
office = office_model.Office()


office_route = Blueprint('office',__name__,url_prefix='/api/v2/office')
@office_route.route('/add',methods=['POST'])
def save():
    """ Add a new political office to the database """
    try:
        data = request.get_json(force=True)
    except:
        return make_response(jsonify({
            "status":400,
            "message":"ensure your content type is application/json"
        })),400  
    name = data["name"]
    office_type = data["office_type"]

    office.save(name, office_type)

    return make_response(jsonify({
            "message": "office added successfully",
            "office": {
                "name":name,
                "hqaddress": office_type
            }
        }), 201)

@office_route.route('',methods=['GET'])
def get_offices():
    """
        get all registered offices
    """


    offices = office_model.Office()

    all_offices = offices.fetch_all_offices()

    if not all_offices:

        return make_response(jsonify({
            'status':404,
            'msg':'there are no registered offices yer'
        }),404)
    
    response = jsonify({
            'message': "Successfully fetched all the offices",
            'products': all_offices
            })

    response.status_code = 200
    return response
