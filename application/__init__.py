#__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from .api import api

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] ='DUHYFUWEGH'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['DEBUG'] = True
    
    db.init_app(app)
    app.register_blueprint(api)

    from .routes import routes
    from .auth import auth
    from .models import User
 
    app.register_blueprint(auth,url_prefix='')
    app.register_blueprint(routes,url_prefix='/')
    
    create_db(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_db(app):
    with app.app_context():
        if not path.exists('templates/'+ DB_NAME):
            db.create_all()
            print('Created Database!')