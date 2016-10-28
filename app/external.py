# import paho.mqtt.client as mqtt
from flask_socketio import SocketIO
from labmet.fao_aquacrop_model.prodfao import AquaCropModel

aquacrop_data = {"culture_name": "potato",
                 "ky": 1.1,
                 "lat": 51.5044968,
                 "eto_culture": 0.8,
                 "avg_year_temp": 19,
                 "n_days": 130,
                 "peak_l_a_index": 3,
                 "awc": 35}

aqua_crop_model = AquaCropModel(**aquacrop_data)
socketio = SocketIO()
# client = mqtt.Client()
