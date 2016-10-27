#!/usr/bin/env python3
"""
Do you have station? This file simulate a
weather station.
"""

import sys
import json
import argparse
import paho.mqtt.client as mqtt
from socketIO_client import SocketIO, LoggingNamespace


# Arguments
ap = argparse.ArgumentParser()
ap.add_argument("-host", "--host", type=str, default="0.0.0.0",
                help="broker host")
ap.add_argument("-shost", "--sockethost", type=str, default="localhost",
                help="socket host default: localhost")
ap.add_argument("-port", "--port", type=int, default=1883,
                help="port")
ap.add_argument("-sport", "--sport", type=int, default=8080,
                help="socket port, default: 8080")
ap.add_argument("-k", "--keepalive", type=int, default=60,
                help="keepalive")
ap.add_argument("-u", "--user", type=str, default="server_listener",
                help="user")
ap.add_argument("-p", "--password", type=str, default="l4b804",
                help="password")
ap.add_argument("-t", "--topic", type=str, default="weather_data",
                help="topic")
ap.add_argument("-q", "--qqos", type=int, default=0,
                help="qqos default: 0")
ap.add_argument("-w", "--wait", type=float, default=1.0,
                help="socket wait")
args = vars(ap.parse_args())

# SocketIO
socketIO = SocketIO(args['sockethost'], args['sport'])


def on_connect(client, userdata, flags, rc):
    print("Connected MQTT [%s:%s] topic [%s]" % (args['host'], args['port'],
                                                 args['topic']))


def on_message(client, userdata, msg):
    """this function send to"""
    payload = msg.payload.decode('utf-8')  # py3
    socketIO.emit('stations', payload)
    socketIO.wait(seconds=args['wait'])


# client mqtt
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Set username and password
client.username_pw_set(username=args['user'],
                       password=args['password'])

# connect
client.connect(args['host'],
               args['port'],
               args['keepalive'])

# Subscrive
client.subscribe(args['topic'], args['qqos'])

# public
try:
    print("Press CTRL+C to exit.")
    client.loop_forever(timeout=1.0, max_packets=1,
                        retry_first_connection=False)
except (KeyboardInterrupt, SystemExit):
    sys.exit()
