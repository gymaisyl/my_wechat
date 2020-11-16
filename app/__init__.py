from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from config import config


def create_app(config_name):
    """config_name
    Create an application through the factory mode, and initialize the corresponding application instance by passing in different configurations

    :param config_name: str Project configuration corresponding to different environments：development，production，test
    """
    app = Flask(__name__)
    # app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    db.app = app  # Solve the problem of context (operate the database outside the view)

    "------ Here is the blueprint for registration -------"
    from app.ifw import ifwsend_blu, ifwrecv_blu
    app.register_blueprint(ifwsend_blu)
    app.register_blueprint(ifwrecv_blu)

    from app.wxpub import verify_blu
    app.register_blueprint(verify_blu)

    return app
