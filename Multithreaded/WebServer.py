__author__ = 'rosienej'

import threading
from socket import *
import ProcessRequest

class WebServer(threading.Thread):
    def __init__(self, serverPort):
        threading.Thread.__init__(self)
        self.serverPort = serverPort

    def run(self):
        serverSocket = socket(AF_INET,SOCK_STREAM)
        serverSocket.bind(('localhost',self.serverPort))
        serverSocket.listen(0) # number of backlogged connections
        print ('server ready')
        while 1:
            try:
                connectionSocket,_ = serverSocket.accept()
            except IOError:
                print ("Server Socket Accept Error")

      # We will kick off a handle request object here!! and that's it.
            thread1 = ProcessRequest.ProcessRequest( connectionSocket )
            thread1.start()
