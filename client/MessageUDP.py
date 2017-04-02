import socket
import sys


class MessageUDP(object):
	def __init__(self):
		try:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		except socket.error:
		    print 'Failed to create socket'
		    sys.exit()


	def set_destination(self,ip,port):
		self.host = ip
		self.port = port


	def send(self,string):
		print "sending"
		self.socket.sendto(string, (self.host,self.port))