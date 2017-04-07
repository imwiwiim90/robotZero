import socket
import sys

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
a = ""
while a != "exit":
	a = raw_input("send message: ")
	s.sendto(a, ("127.0.0.1",8000))
