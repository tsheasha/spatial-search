# -*- coding: utf-8 -*-

import os
from extensions import db
from flask import Flask
from flask.ext.cors import CORS, cross_origin
from server.api import api
from server.models import *

from load_db_from_csv import load_shops, load_products, load_tags, load_taggings

def create_app(settings_overrides=None):
    app = Flask(__name__)

    # Using Cross-origin resource sharing to allow
    # the ajax call from another domain since
    # SimpleHTTPServer runs on port 8000 and this
    # application runs on port 5000
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    configure_settings(app, settings_overrides)

    # Initialise database
    db.init_app(app)

    configure_blueprints(app)

    with app.app_context():
        db.create_all()
        # Initialising the data in the database
        # this should not be needed in a real system
        # since the data would be fed in as a result or
        # real events taking place.
        # However for the sake of this task we need data to work with
        # so will keeo this here.
        if not Shop.query.count():
            load_shops('shops.csv')
        if not app.config['TESTING'] and not Product.query.count():
            load_products('products.csv')
        if not Tag.query.count():
            load_tags('tags.csv')
        if not Tagging.query.count():
            load_taggings('taggings.csv')
    return app


def configure_settings(app, settings_override):
    parent = os.path.dirname(__file__)
    data_path = os.path.join(parent, '..', 'data')
    app.config.update({
        'DEBUG': True,
        'TESTING': False,
        'DATA_PATH': data_path
    })
    if settings_override:
        app.config.update(settings_override)


def configure_blueprints(app):
    app.register_blueprint(api)
