#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .. import socketio


def on_mesage(mosq, obj, msg):
    socketio.emit('my response', {'topic': msg.topic, 'payload': msg.payload}, namespace='/weather_data')
