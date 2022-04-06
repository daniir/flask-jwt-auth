import email
from flask import Blueprint
from middleware.validateToken import validate_token

home = Blueprint('home', __name__, url_prefix='/')

@home.route("/", methods=['GET'])
@validate_token
def index(user):
    return {
        "msg": "Hello World",
        "username": user.name,
        "email": user.email
    }

@home.route("/about", methods=['GET'])
def about():
    return {
        'msg': 'Basic authentication example using JWT and SQLite'
    }