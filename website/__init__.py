from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "database.db"


#Create Flask app
def create_app():
    app = Flask(__name__)

    #Config Data 
    app.config['SECRET_KEY'] = "asdf"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    



    from .views import views
    from .auth import auth


    #We will be able to go to these urls

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')


    #check if database is created and create database if it has not been created yet

    from .models import User, Note

    create_database(app)

    #where should flask redirect us if the user is not login and login is requred => auth.login endpoint
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    #telling flask how we load a user, what user we are looking for, just an essential thing for loading a user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('websote/' +DB_NAME):
        db.create_all(app=app)
        print("Created Database!")
    