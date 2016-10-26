#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_script import Manager, Shell
from app import create_app, socketio
from app.resources import MQTTThread

import signal
import sys


app = create_app('default')
manager = Manager(app)
mqtt_thread = None


def signal_handler(signal, frame):
    mqtt_thread.stop = True
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


def make_shell_context():
    return dict(app=app)
manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def runserver():
    socketio.run(app,
                 host='0.0.0.0',
                 port=80)

if __name__ == '__main__':
    mqtt_thread = MQTTThread()
    mqtt_thread.start()

    manager.run()
