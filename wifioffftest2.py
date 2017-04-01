import socket
import sys


try: 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
msg = ""
while msg != "exit":
	try:
		msg = raw_input('msg: ')
		s.sendto(msg,('192.168.0.17',5000))
	except socket.error, (no,msg):
		if no == socket.errno.ENETUNREACH:
			print msg
