from threading import Thread
from .. import client


class MQTTThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.stop = False

    def run(self):
        while not self.stop and client.loop_forever() == 0:
            pass
