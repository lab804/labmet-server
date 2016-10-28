#!/usr/bin/env python3
"""
Do you have station? This file simulate a
weather station.
"""

import sys
import time
import json
import random
import argparse
from datetime import datetime
import paho.mqtt.client as mqtt
from datetime import datetime
from app.external import aqua_crop_model


def random_data(_id=1):
    """ random data to publish """

    data = {
        "id": _id,
        "collected_at": datetime.now().strftime("%m/%d/%YT%H:%M:%S"),
        "bmp180_temp": random.uniform(10.0, 50.0),
        "bmp180_alt": random.uniform(100.0, 3000.0),
        "bmp180_press": random.uniform(1.5, 1.9),
        "ds18b20_temp": random.uniform(-10.0, 50.0),
        "dht22_temp": random.uniform(10.0, 50.0),
        "dht22_humid": random.uniform(1.0, 95.0),
        "bh1750_illuminance": random.randint(0, 1000),
        "analog_soil_moisture": random.uniform(1.0, 50.0)
    }

    productivity_values_data = {"soil_moisture": data["analog_soil_moisture"],
                                "temperature": data["ds18b20_temp"],
                                "illuminance": data["bh1750_illuminance"],
                                "date": datetime.now()
                                }

    productivity_values = aqua_crop_model.aqua_crop(**productivity_values_data)

    data.update(productivity_values)

    return json.dumps(data)

# Arguments
ap = argparse.ArgumentParser()
ap.add_argument("-host", "--host", type=str, default="0.0.0.0",
                help="brokerurl")
ap.add_argument("-port", "--port", type=int, default=1883,
                help="port")
ap.add_argument("-k", "--keepalive", type=int, default=60,
                help="keepalive")
ap.add_argument("-u", "--user", type=str, default="server_listener",
                help="user")
ap.add_argument("-p", "--password", type=str, default="l4b804",
                help="password")
ap.add_argument("-t", "--topic", type=str, default="weather_data",
                help="topic")
ap.add_argument("-d", "--delay", type=float, default=1.0,
                help="delay")
ap.add_argument("-i", "--id", type=int, default=1,
                help="id simulate")
args = vars(ap.parse_args())


# clinent mqtt
client = mqtt.Client()


# Set username and password
client.username_pw_set(username=args['user'],
                       password=args['password'])

# connect
client.connect(args['host'],
               args['port'],
               args['keepalive'])

# public
try:
    while True:
        try:
            payload = json.dumps(random_data(args['id']))
            client.publish(args['topic'], payload)
            time.sleep(args['delay'])
        except ZeroDivisionError:
            pass
except (KeyboardInterrupt, SystemExit):
    sys.exit()
