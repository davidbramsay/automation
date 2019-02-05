PORT = 12345

import time

class StateMaintainer():

    i=0

    def iterate_i(self):
        i = self.i
        self.i = i + 1
        return i

# rpyc servic definition
import rpyc

class MyService(rpyc.Service):
    def exposed_i(self):
        return main.iterate_i()

# start the rpyc server
from rpyc.utils.server import ThreadedServer
from threading import Thread
server = ThreadedServer(MyService, port = PORT)
t = Thread(target = server.start)
t.daemon = True
t.start()

#start
main = StateMaintainer()

print 'running on port ' + str(PORT) + ' ...\n'

while True:
    time.sleep(5)
