import numpy as np
import cv2
import socket   #for sockets
import sys  #for exit
import camera
import time
import random
from thread import *

CHUNK_SIZE = 4096


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

PORT = 5000
HOST = ''

# Bind socket to local host and port
subscribers = []

try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
print 'Socket bind complete'

msg, addr = s.recvfrom(CHUNK_SIZE)
print 'ip: ' + addr[0] + " : " + str(addr[1])
if (msg == 'subscribe'):
	subscribers.append(addr)



     

#print 'Ip address of ' + host + ' is ' + remote_ip
host = ''
#host = '190.27.88.19'
#port = 5000
#start_new_thread(receiver_thread,(subcribers,) )
while True:
	time.sleep(1.0/30)
	chunks = cam.get_image_slides()
	random.shuffle(chunks)
	for chunk in chunks:
		for subs in subscribers:
			s.sendto(chunk , subs)




