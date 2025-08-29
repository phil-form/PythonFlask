from flask import jsonify

from app import app


@app.get('/')
def index():
    return jsonify({'error': 'invalid credentials'}), 401