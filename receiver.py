import socket
import sys
CHUNK_SIZE = 4096

PORT = 8000
try: 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
try:
    s.bind(("", PORT)) # as server
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
print 'Socket bind complete'
msg = ""
while str(msg) != "exit":
    msg, addr = s.recvfrom(CHUNK_SIZE)
    print msg