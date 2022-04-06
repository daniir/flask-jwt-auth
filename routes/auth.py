from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request, make_response
from lib.extensions import db
from models.user import User
import uuid
from config.config import secret_key
import jwt
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route("/signup", methods=['POST'])
def signup():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if not username or not email or not password:
        return make_response("All fields are required")

    user = User.query.filter_by(email = email).first()
    if user:
        return make_response("User already registered", 202)
    else:
        hash_passwd = generate_password_hash(password)
        new_user = User(
            public_id= str(uuid.uuid1()),
            name= username,
            email= str(email).lower(),
            password= hash_passwd
        )

        db.session.add(new_user)
        db.session.commit()
        return make_response("Successfully registered", 201)

@auth.route("/login", methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']

    if not email or not password:
        return make_response("All fields are required")
    
    user = User.query.filter_by(email=email).first()

    if not user:
        return make_response("User not registered, please sign up", 404)
    
    check_user_passwd = check_password_hash(user.password, password)

    if check_user_passwd:
        token = jwt.encode({
            'public_id': user.public_id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, secret_key, algorithm="HS256")

        token.encode('UTF-8')
        return make_response(jsonify({'token': token}), 200)
    else:
        return make_response("email or password incorrect", 404)
