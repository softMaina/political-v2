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
