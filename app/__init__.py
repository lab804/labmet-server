#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

from flask import Flask
from flask_socketio import SocketIO
from config import config

socketio = SocketIO()

def create_app(config_stage):
    app = Flask(__name__)
    app.config.from_object(config[config_stage])
    config[config_stage].init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)

    return app