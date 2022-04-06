from flask import jsonify, request, make_response
from config.config import secret_key
from models.user import User
from jwt import decode, exceptions
from functools import wraps

def validate_token(f):
    @wraps(f)
    def get_token():
        token = None

        if 'auth-token' in request.headers:
            token = request.headers['auth-token']

        if not token:
            return make_response(jsonify({'msg': 'No token access'}), 404)

        try:
            data = decode(token, secret_key, algorithms=["HS256"])
            user = User.query.filter_by(public_id = data['public_id']).first()
        except exceptions.DecodeError:
            return make_response(jsonify({'msg': 'Invalid token'}), 401)
        except exceptions.ExpiredSignatureError:
            return make_response(jsonify({'msg': 'Token expired'}), 401)
        
        return f(user)
    return get_token