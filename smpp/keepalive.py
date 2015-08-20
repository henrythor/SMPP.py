import threading
from time import sleep

class SMPPKeepAlive(threading.Thread):
        def __init__(self, obj):
                self.obj = obj
                threading.Thread.__init__(self)
		self.daemon = True
        def run(self):
                while 1:
                        self.obj._keepalive()
                        sleep(30)

