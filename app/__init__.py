from flask import Flask
from lib.extensions import db, migrate
from config.config import database_uri, secret_key
from routes.home import home
from routes.auth import auth
from routes.contacts import contacts

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secret_key

    #Base de Datos
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)
    #Rutas
    app.register_blueprint(home)
    app.register_blueprint(auth)
    app.register_blueprint(contacts)
    return app