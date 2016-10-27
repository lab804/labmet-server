import os
import sys
import signal


from app import create_app, external
from app.resources import MQTTThread

app = create_app(os.environ.get('PROD') or 'default')

mqtt_thread = MQTTThread()
mqtt_thread.start()

# 
# def signal_handler(signal, frame):
#     mqtt_thread.stop = True
#     sys.exit(0)
#
# signal.signal(signal.SIGINT, signal_handler)


def main():

    external.socketio.run(app,
                          host=os.environ.get('HOST') or '0.0.0.0',
                          port=int(os.environ.get('PORT')) or 80)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        mqtt_thread.stop = True
        sys.exit(0)
