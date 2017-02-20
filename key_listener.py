import socket
import sys
import time

try: 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
HOST = ""
PORT = 8000

try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
print 'Socket bind complete'


def key_actuator(key_list):
	print keys


while True:
	msg, addr = s.recvfrom(2048)
	keys = [0 if k == "0" else 1 for k in msg[:4]]
	key_actuator(keys)

