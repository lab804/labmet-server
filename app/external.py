import paho.mqtt.client as mqtt
from flask_socketio import SocketIO

socketio = SocketIO()
client = mqtt.Client()
