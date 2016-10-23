#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from datetime import datetime, timedelta
from .. import socketio

from config import Config
from notification import Notification

notification = Notification(Config.NOTIFICATIONKEY)  # o.0

NIGHT = 5  # Hour (supposedly)
SECONDS_DELAY = 10 # Delay send push just example massive.
DELAY = datetime.now() + timedelta(seconds=SECONDS_DELAY)

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
    global DELAY
    json_msg = json.loads(msg.payload)
    json_msg['id'] = 123
    json_msg['status'] = 1

    socketio.emit('my response', {'topic': msg.topic, 'payload': json_msg},
                  namespace='/weather_data')

    if json_msg['bh1750_illuminance'] < CULTURE['POTATO']['BEST_PERFOMACE']['ILLUMINACE']:
        # is night?
        now = datetime.now()

        if now.hour > NIGHT and now > DELAY:
            msg = CULTURE['POTATO']['MSGS']['LESS_ILLUMINACE']
            notification.send_push_all(msg)
            ERROR = True
            DELAY = now + timedelta(seconds=SECONDS_DELAY)
