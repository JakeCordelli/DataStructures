__author__ = 'rosienej'

from socket import *
from collections import *
from MyExceptions import *
## \mainpage The faulty (Fawlty) Socket class documentation
#  \section Introduction
#  Since sending packets from localhost:source_port to localhost:destination_port has
#  very low error rate (bit arror and dropped packets) this class allows for the injection'
#  of errors at a prescribed rate.
#
#  \section Discussion
#
class faulty_socket(object):
	## Construct a faulty socket given a network transport pair, the file object is None
	def __init__(self, net,trans,fo=None):
		self.__sock = socket(net,trans)
		self.__packet_drop_prob =0.0
		self.__bit_error_prob =0.0
		self.__file_object=fo
		self.__rvs = deque()

	@classmethod
	## This is a class factory method, which sets the file from which to pull the random varaiables
	# \param net   The network to use
	# \param trans The transport to use, in this case UDP
	# \param fo    The file object
	#
	def random_file_object(cls,net,trans,fo):
		return cls(net,trans,fo)

	def __getattr__(self, name):
		return getattr(self.__sock, name)

	def set_drop_prob(self,prob):
		self.__packet_drop_prob = prob

	def set_bit_error_prob(self,prob):
		self.__bit_error_prob = prob

	def sendto(self, MESSAGE, (UDP_IP, UDP_PORT)):
		"""
		sendto:
			Behaves like a normal socket unless a file of random numbers has been used to create the class
			When a file is specified the elements are queued up and used to
		Args:
			Message: a message to send send out the socket
			(UDP_IP, UDP_PORT) : The network protocol and port tuple

		"""
		if self.__file_object:
			try:
				rv = self.__rvs.pop()
			except IndexError:
				self.__rvs.extend(map(float,self.__file_object.readline().split()))
				rv = self.__rvs.pop()

			if rv >= self.__packet_drop_prob:
				print "sending to",(UDP_IP, UDP_PORT)
				self.__sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
			else:
				print "Sender: Packet Lost",self.__packet_drop_prob,rv
		else:
			self.__sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

	def settimeout(self,value):
		self.__sock.settimeout(value)

	def bind(self,*p):
		print p
		self.__sock.bind(*p)

	def recvfrom(self,max_size):
		"""

		"""
		# to do: Need to receive from the socket and periodically raise a bad checksum exception to
		# be handled by the calling function

		data,client=self.__sock.recvfrom(max_size)

		if self.__file_object:
			try:
				rv = self.__rvs.pop()
			except IndexError:
				self.__rvs.extend(map(float,self.__file_object.readline().split()))
				rv = self.__rvs.pop()

			if rv <= self.__bit_error_prob:
				raise BadCheckSum("Simulated Bad Checksum In Received Packet")
			else:
				return (data,client)
		else:
			return (data,client)
