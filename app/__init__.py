#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey
from flask import Flask
from flask_socketio import SocketIO
from config import config
import paho.mqtt.client as mqtt

monkey.patch_all()

socketio = SocketIO()
client = mqtt.Client()


def create_app(config_stage):
    app = Flask(__name__)
    app.config.from_object(config[config_stage])

    from .main import main as main_blueprint
    from .main import on_mesage

    app.register_blueprint(main_blueprint)

    config[config_stage].init_app(app)
    client.username_pw_set(username=config[config_stage].MQTT_USERNAME,
                           password=config[config_stage].MQTT_PASSWORD)
    client.connect(config[config_stage].MQTT_BROKER_URL,
                   config[config_stage].MQTT_PORT,
                   config[config_stage].MQTT_KEEP_ALIVE)
    client.subscribe(config[config_stage].MQTT_TOPIC, config[config_stage].MQTT_QOS)
    client.on_message = on_mesage

    socketio.init_app(app)

    return app