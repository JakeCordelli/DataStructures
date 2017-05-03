__author__ = 'rosienej'
from RDT import *

server_address = ('localhost', 8080)

def main():
	print '[Application Layer] receiver starts'
	rdt_channel = RDT.Receiver(server_address)
	rdt_channel.accept()

	while(True):
		data = rdt_channel.receive()
		print "[Application Layer]",data

	pass

if __name__ == '__main__':
	main()

