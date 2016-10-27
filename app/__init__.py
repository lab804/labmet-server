from flask import Flask

from config import config
from external import client, socketio


def create_app(config_stage='default'):
    app = Flask(__name__)

    # read config
    app.config.from_object(config[config_stage])

    # blueprints of app
    blueprints(app)

    # external libs
    external_lib(app)

    return app


def blueprints(app):
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)


def external_lib(app):
    """load external lib"""

    from .main import on_mesage

    # MQTT
    # set username and password
    client.username_pw_set(username=app.config['MQTT_USERNAME'],
                           password=app.config['MQTT_PASSWORD'])

    # connecting...
    client.connect(app.config['MQTT_BROKER_URL'],
                   app.config['MQTT_PORT'],
                   app.config['MQTT_KEEP_ALIVE'])

    # sub
    client.subscribe(app.config['MQTT_TOPIC'],
                     app.config['MQTT_QOS'])

    client.on_message = on_mesage

    # socketio
    socketio.init_app(app)
