from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from config import Config
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    #ORM - Object Relational Mapper - flask-sqlalchemy
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    login_manager.init_app(app)

    # Register the blueprints
    from app.blueprints.home import bp as home
    app.register_blueprint(home)
    from app.blueprints.authentication import bp as authentication
    app.register_blueprint(authentication)
    
    return app