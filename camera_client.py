import numpy as np
import cv2
import socket   #for sockets
import sys  #for exit
import camera
import time
import random
import threading
from thread import *

CHUNK_SIZE = 4096

# tr   5 1
# echo 6 1

# tr     19 2
# echo   26 2

# servos
# 21
# 20
# 18

cam = camera.VideoCamera()
if cam.video.isOpened():
	print "camera connected successfully"
else:
	print "error while accesing to camera"
	sys.exit(0)


# LSB -> MSB
def int_to_byte3(number):
	byte = ''
	for i in range(3):
		byte += chr(number%256)
		number = number/256
	return byte

# LSB -> MSB
def byte3_to_int(string):
	number = 0
	exp = 0
	for s in string:
		number += ord(s) * (256**exp)
		exp+=1
	return number

# six first bytes -> from,to
def image_to_chunks(img):
	chunks = []
	chunks.append(img)
	return chunks

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error:
    print 'Failed to create socket'
    sys.exit()
'''
host = 'ec2-35-163-207-7.us-west-2.compute.amazonaws.com'
 
try:
    remote_ip = socket.gethostbyname( host )
 
except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()
'''
#def receiver_thread(subs):

PORT = 8000
HOST = ''

# Bind socket to local host and port
subscribers = []

try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
print 'Socket bind complete'


class SocketListener(threading.Thread):
	def __init__(self,_socket,lock,limit=10):
		threading.Thread.__init__(self)
		self.sckt = _socket
		self.ips = {}
		self.limit = limit


	def run(self):
		while True:
			msg, addr = self.sckt.recvfrom(CHUNK_SIZE)
			ip = str(addr[0]) + ":" + str(addr[1])
			print msg
			if not (ip in self.ips.keys()):
				lock.acquire()
				print "new subscriber: " + ip
				if len(self.ips) == self.limit:
					self.ips.pop(ip,None)
				self.ips[ip] = addr
				lock.release()



#print 'Ip address of ' + host + ' is ' + remote_ip
host = ''
#host = '190.27.88.19'
#port = 5000
#start_new_thread(receiver_thread,(subcribers,) )
lock = threading.Lock()
skt_manager = SocketListener(s,lock,limit=2)
skt_manager.start()
while True:
	time.sleep(1.0/30.0)
	chunks = cam.get_image_slides() # video
	random.shuffle(chunks)
	lock.acquire()
	ips = skt_manager.ips
	for chunk in chunks:
		for ip in ips.keys():
			s.sendto(chr(0)+chr(0)+chunk , ips[ip]) #video type
	lock.release()




