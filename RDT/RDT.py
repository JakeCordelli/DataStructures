from FaultySocket import *
from threading import *
from struct import Struct
import binascii
from time import sleep

Channel_Drop_Rate = 0.250
Channel_Bit_Error_Rate = 0.250

class RDT(object):
	def __init__(self,destination_address=None,source_address=None):
		self.__fo = open("Random10K.txt")
		self.__faulty_socket = faulty_socket.random_file_object(AF_INET, SOCK_DGRAM,self.__fo)

		if source_address:
			self.__faulty_socket.bind(source_address)

		#Here are the simulation variables
		self.__faulty_socket.settimeout(2)
		self.__faulty_socket.set_drop_prob(Channel_Drop_Rate)
		self.__faulty_socket.set_bit_error_prob(Channel_Bit_Error_Rate)

		print "The RDT Object uses 8081 as the back channel."
		print "TCP would use the first free (higher) one "
		self.__open = False
		self.sending_thread = None
		self.receiving_thread = None
		self.destination_address = destination_address
		self.__sender_state = 0
		self.__receiver_state = 0
		self.sender_current_seqnum = 0
		self.sender_expected_seqnum = 0
		self.receiver_current_seqnum = 0
		self.receiver_expected_seqnum = 0
		self.__msgqueue = deque()
		self.__pktqueue = deque()
		pass

	@classmethod
	def Sender(cls,destination_address):
	## This class factory method binds the senders return port to a known address
	## \param destination_address is the address of the server
		return cls(destination_address,('localhost',8081))

	@classmethod
	def Receiver(cls,destination_address):
	## This class factory method binds the receiver to the specified interface
	## \param destination_address is the address of the server
		return cls(None,destination_address)

	def send(self,message):
		## Simply place the message in the outgoing queue
		# \param message:   Message to Send
		self.__msgqueue.appendleft(message)
		pass

	def receive(self):
		message = None
		while message is None:
			try:
				message=self.__msgqueue.pop()
			except IndexError:
				sleep(4)  # let it fill
		return message

	def accept(self):
		self.__open = True
		self.receiving_thread = Thread(target=RDT.stop_and_wait_receiver_thread,args=(self,))
		self.receiving_thread.start()
		print "[TRANSPORT] Starting the Receiver"

	def open(self):
		self.__open = True
		print "[TRANSPORT] Sender Opening a Reliable Channel to:",self.destination_address
		self.sending_thread = Thread(target=RDT.stop_and_wait_sender_thread,args=(self,))
		self.sending_thread.start()
		pass

	def close(self):
		self.__open = False
		self.sending_thread.join()
		print "[TRANSPORT] Sender Reliable Channel to:",self.destination_address," is now closed"
		pass

	def make_pkt(self,seqnum,message):
		packet_format = '! I'+ str(len(message))+'s'
		s = Struct(packet_format)
		packed_data = s.pack(seqnum,message)
		return packed_data

	def is_ack(self,packet):
		packet_format = '! I'+ str(len(packet)-4)+'s'
		s = Struct(packet_format)
		(seqnum,message) = s.unpack(packet)
		return seqnum

	def extract(self,packet):
		packet_format = '! I'+ str(len(packet)-4)+'s'
		s = Struct(packet_format)
		(seqnum,message) = s.unpack(packet)
		return seqnum,message

	def stop_and_wait_sender_thread(self):
		print "[TRANSPORT] Sender Stop And Wait Sender Thread Starts \n"
		while self.__open:
			#print "Sender in State 0"
			if self.__sender_state == 0:
				try:
					msg = self.__msgqueue.pop()
					# Got something, need to make packet and send and go to state 1
					self.sender_expected_seqnum = self.sender_current_seqnum
					pkt =self.make_pkt(self.sender_current_seqnum,msg)
					self.__faulty_socket.sendto(pkt,self.destination_address)

					self.__sender_state = 1
				except IndexError:
					#print "Nothing to send Strip Channel"
					try:
						dump=self.__faulty_socket.recvfrom(1024)
						pass
					except timeout:
						pass
					continue
			elif self.__sender_state == 1:
				print "[TRANSPORT] Sender in State 1"
				try:
					# Remember to start the receiver, or this will fail
					# the failure is [Errno 10054]
					(ack_pack,responsefrom)=self.__faulty_socket.recvfrom(1024)
					# check the sequence number of ack and see if we can continue
					print "[TRANSPORT] Sender got an ack with Number",self.is_ack(ack_pack)
					if self.is_ack(ack_pack)==self.sender_expected_seqnum:
						print "[TRANSPORT] Got The ACK I Want"
						self.__sender_state = 0
						self.sender_current_seqnum = (self.sender_current_seqnum+1)%2
				except timeout:
					print "[TRANSPORT] Sender Ack Time Out"
					self.__faulty_socket.sendto(pkt,self.destination_address)
				except BadCheckSum:
					print "[TRANSPORT] Sender Bad Checksum: Ignoring Packet"
					pass
				continue

			else:
				print "[TRANSPORT] Sender in Bad State: Hanging Up In Loop!!"
				while True:
					pass
			pass

		pass

	def stop_and_wait_receiver_thread(self):
		## This is the reciever thread as on page 214 of Kurose Ross
		# \details{ Initial state is zero, with expected packet zero, when a packet arrives if it is expected
		#  it is acked.  And the expected packet is updated and the data is delivered to the waiting application
		# If it is unexpected the last a duplicate ack of the last expected packet is sent
		# If the packet is corrupted, the last expected packet is send a duplicate ack, last good thing we got
		#         }
		print "[TRANSPORT] Receiver Thread Starts"
		while(True):
			if self.__receiver_state == 0:
				try:
					print "[TRANSPORT] Receiver Waiting for Message",self.receiver_expected_seqnum
					(packet,message_from)=self.__faulty_socket.recvfrom(1024)
					self.receiver_current_seqnum,message=self.extract(packet)
					print "[TRANSPORT] Receiver Got Packet ",self.receiver_current_seqnum,message
					if self.receiver_current_seqnum == self.receiver_expected_seqnum:
						print "[TRANSPORT] Receiver Acking Packet ",self.receiver_current_seqnum
						self.__faulty_socket.sendto(packet,message_from)
						self.__msgqueue.appendleft(message)
						self.receiver_expected_seqnum = (self.receiver_current_seqnum+1)%2
					else:  # Send a duplicate Ack, since it may have been lost
						packet=self.make_pkt(self.receiver_current_seqnum,"DUPLICATE ACK")
						self.__faulty_socket.sendto(packet,message_from)
				except timeout:
						print "[TRANSPORT] Receiver Time Out: No Messages Yet, take a nap"
						sleep(1)
				except BadCheckSum:
						if self.receiver_expected_seqnum == 0:
							ack_seq = 1
						else:
							ack_seq = 0

						packet=self.make_pkt(ack_seq,"DUPLICATE ACK")
						self.__faulty_socket.sendto(packet,message_from)
						print "[TRANSPORT] Receiver Bad Checksum: Ignoring Packet"
				pass
			else:
				print "[TRANSPORT] Receiver in Bad State: Hanging Up In Loop!!"
				while True:
					pass
			pass
