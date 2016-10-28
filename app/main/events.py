#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from config import Config
from app.external import socketio
from app.main.notification import Notification


notification = Notification(Config.NOTIFICATIONKEY)  # o.0


@socketio.on('stations')
def station_receive(json_data):
    socketio.emit('station_data', json.loads(json_data),
                  namespace='/weather_data')
