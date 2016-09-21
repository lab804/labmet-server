#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'testing'
    MQTT_BROKER_URL = "0.0.0.0"
    MQTT_PORT = 1883
    MQTT_KEEP_ALIVE = 60
    MQTT_TOPIC = "weather_data"
    MQTT_QOS = 0

    @staticmethod
    def init_app(app):
        pass

config = {'default': Config}
