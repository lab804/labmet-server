#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from datetime import datetime
from .. import socketio
from notification import Notification

from config import Config

notification = Notification(Config.NOTIFICATIONKEY) # o.0

ERROR = False
NIGHT = 5

CULTURE = {
    'POTATO': {
        'BEST_PERFOMACE': {
            'ILLUMINACE': 3,
            'TEMPMAX': 30.5,
            'TEMPMIN': 9.3,
        },
        'MSGS': {
            'LESS_ILLUMINACE': 'missing light'
        }
    }
}


def on_mesage(mosq, obj, msg):
    global ERROR  # crazy o.0
    json_msg = json.loads(msg.payload)
    json_msg['id'] = 123
    json_msg['status'] = 1

    socketio.emit('my response', {'topic': msg.topic, 'payload': json_msg},
                  namespace='/weather_data')

    if ERROR is False and json_msg['bh1750_illuminance'] < CULTURE['POTATO']['BEST_PERFOMACE']['ILLUMINACE']:
        # is night?
        now = datetime.now()
        if now.hour > NIGHT:
            msg = CULTURE['POTATO']['MSGS']['LESS_ILLUMINACE']
            notification.send_push_all(msg)
            ERROR = True
