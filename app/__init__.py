# Author: Jaehoon Lim

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
import os

from config import DevConfig

db = SQLAlchemy()
bcrypt = Bcrypt()
photos = UploadSet('photos', IMAGES)

def create_app(config_class=DevConfig):
    """
    Creates an application instance to run using settings from config.py
    :return: A Flask object
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    configure_uploads(app, photos)
    patch_request_class(app)

    from populate_db import populate_db
    from app.models import User, Item, ShippingInfo

    with app.app_context():
        db.create_all()
        populate_db()

    from app.main import bp
    app.register_blueprint(bp)

    return app
