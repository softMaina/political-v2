import os
from flask import Flask, request, jsonify
from app import create_app
app = create_app(os.getenv('FLASK_ENV'))

@app.errorhandler(Exception)
def handle_error(e):
    if request.mimetype != 'application/json':
        return jsonify({
            "status":406,
            "message":"data must be of mimetype application/json"
        }),406

if __name__ == '__main__':
    app.run(debug=True)