from flask import Flask

from config import config


def register_blueprints(app_instance):
    from routes import app_bp
    app_instance.register_blueprint(app_bp)


def register_extensions(app_instance):
    from extensions import db
    db.init_app(app_instance)
    from model import create_all
    create_all(app_instance)


def create_app():
    app_instance = Flask(__name__, static_folder='static')
    app_instance.config.from_object(config)
    register_extensions(app_instance)
    register_blueprints(app_instance)
    return app_instance


app = create_app()
