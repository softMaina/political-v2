from flask import Flask, make_response, abort, jsonify, Blueprint,request
from app.api.v2.models import office_model
from app.api.v2 import database
from app.api.v2.utils.validator import validate_office_json_keys, return_error, validate_string,validate_office_types
office = office_model.Office()


office_route = Blueprint('office',__name__,url_prefix='/api/v2/')
@office_route.route('offices',methods=['POST'])
def save():
    """ Add a new political office to the database """

    json_key_errors = validate_office_json_keys(request)

    if json_key_errors:
        return return_error(400, "Missing keys {}".format(json_key_errors))


    try:
        data = request.get_json(force=True)
    except:
        return make_response(jsonify({
            "status":400,
            "error":"Ensure your content type is application/json"
        })),400  
    name = data["name"]
    office_type = data["office_type"]

    name = name.strip()
    office_type = office_type.strip()


    if(validate_office_types(office_type.lower()) == False):
        return return_error(400,"Office must be of either of the following State, Legistlative, Local, Federal")

    if(validate_string(name) == False):
        return return_error(400, "Name must be of type string")
    
    if(validate_string(office_type) == False):
        return return_error(400, "Office_type must be of type string")

    if(name == ""):
        return return_error(400,"name cannot be empty")
    if(office_type == ""):
        return return_error(400,"Office_type cannot be empty")


    office.save(name, office_type)

    return make_response(jsonify({
            "status": 201,
            "office": {
                "name":name,
                "office_type": office_type
            }
        }), 201)

@office_route.route('offices',methods=['GET'])
def get_offices():
    """
        get all registered offices
    """


    offices = office_model.Office()

    all_offices = offices.fetch_all_offices()

    if not all_offices:

        return make_response(jsonify({
            'status':404,
            'error':'There are no registered offices yet'
        }),404)
    
    response = jsonify({
            'status': 200,
            'data': all_offices
            })

    response.status_code = 200
    return response

@office_route.route('offices/<int:office_id>',methods=['GET'])
def get_specific_office(office_id):
    """  
        get an office by id
    """
    query = """SELECT * FROM offices WHERE office_id = '{}'""".format(office_id)
    office = office_model.Office()

    office = database.select_from_db(query)
    if not office:
        return make_response(jsonify({
        "status":404,
        "message": "Office with id {} is not available".format(office_id),
        }), 404)
    
    return make_response(jsonify({
        "status":200,
        "office": office
        }), 200)
@office_route.route('offices/<int:office_id>',methods=['PUT'])
def update(office_id): 
    """
        edit a political office
    """
    json_key_errors = validate_office_json_keys(request)

    if json_key_errors:
        return return_error(400, "Missing keys {}".format(json_key_errors))



    try:
        data = request.get_json(force=True)
    except:
        return make_response(jsonify({
            'status':400,
            'error':'Data should be in json format'
        }),400)  
    id=office_id
    name = data["name"]
    office_type = data["office_type"]

    if(validate_string(name) == False):
        return return_error(400, "Name must be of type string")
    
    if(validate_string(office_type) == False):
        return return_error(400, "Office_type must be of type string")

    if(name == ""):
        return return_error(400,"Name cannot be empty")
    if(office_type == ""):
        return return_error(400,"Office_type cannot be empty")

    office = office_model.Office()
    office.update(id, name, office_type )

    return make_response(jsonify({
            "status": 201,
            "office": {
                "name":name,
                "hqaddress": office_type
            }
        }), 201)

@office_route.route('offices/<int:office_id>',methods=['DELETE'])
def delete(office_id):
    """
        delete a political office
    """
    query = """SELECT * FROM offices WHERE office_id = {} """.format(office_id)
    office = database.select_from_db(query)
        
    if not office:
        return make_response(jsonify({
        "status":404,
        "error": "Office with id {} does not exist".format(office_id)
        }), 404)

    office = office_model.Office()
    office.delete(office_id)

    return make_response(jsonify({
        "status":200,
        "message": "Office deleted successfully"
    }), 200)