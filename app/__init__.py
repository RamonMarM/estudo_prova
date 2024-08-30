# app/__init__.py
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
