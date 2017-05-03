__author__ = 'rosienej'

from RDT import *
from time import sleep

server_address = ('localhost', 8080)

def main():
    print 'Sender Starts'
    rdt_channel = RDT.Sender(server_address)
    rdt_channel.open()
    for message in ('lemon', 'salad', 'hippo', 'lettuce'):
        rdt_channel.send(message)

    sleep(60)
    rdt_channel.close()

    pass

if __name__ == '__main__':
    main()
