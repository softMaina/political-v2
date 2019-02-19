import os
import jwt
from functools import wraps

from flask import request, make_response, jsonify,abort

def verify_tokens():
    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
    if not token:
        abort(make_response(jsonify({"Message": "You need to login"}), 401))
    
    try:
        data = jwt.decode(token, os.getenv('JWT_SECRET_KEY', default='SdaHv342nx!jknr837bjwd?c,lsajjjhw673hdsbgeh'))
        return data["email"], data["user_id"]
    
    except:
        abort(make_response(jsonify({
            "Message":"The token is invalid"
        }), 403))