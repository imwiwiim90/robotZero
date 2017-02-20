import socket   #for sockets
import sys  #for exit
import numpy as np
import cv2
import threading
import time

HEIGHT = 720
WIDTH = 1280

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 5000 # Arbitrary non-privileged port

CHUNK_SIZE = 4096

# LSB -> MSB
def byte3_to_int(string):
	number = 0
	exp = 0
	for s in string:
		number += ord(s) * (256**exp)
		exp+=1
	return number

class ImageManager(threading.Thread):
	def __init__(self,stream,lock):
		threading.Thread.__init__(self)
		self.image = np.zeros((HEIGHT,WIDTH))
		self.stream = stream
		self.lock = lock

	def run(self):
		while True:
			chunks = self.stream.retrieve()
			if len(chunks) == 0:
				continue
			for c in chunks:
				y = byte3_to_int(c[:3])
				x = byte3_to_int(c[3:6])
				msg = c[6:]
				np_arr = np.fromstring(msg, np.uint8)
				data = cv2.imdecode(np_arr,cv2.COLOR_BGR2GRAY)
				if data == None:
					continue
				self.lock.acquire()
				self.set_image(x,y,data)
				self.lock.release()


	def get_image(self):
		return self.image

	def set_image(self,x,y,data):
		y_n,x_n = data.shape 
		self.image[y:y + y_n,x:x + x_n] = data

class UDPreceiver(threading.Thread):
	def __init__(self,_socket,lock):
		threading.Thread.__init__(self)
		self.socket = _socket
		self.lock = lock
		self.chunks = []

	def run(self):
		while True:
			msg , addr = self.socket.recvfrom(CHUNK_SIZE)
			self.lock.acquire()
			self.chunks.append(msg)
			self.lock.release()

	def retrieve(self):
		self.lock.acquire()
		retrieval = list(self.chunks)
		self.chunks = []
		self.lock.release()
		return retrieval



class FrameUpdater(threading.Thread):
	def __init__(self,lock,img):
		threading.Thread.__init__(self)
		self.lock = lock
		self.image = img

	def run(self):
		while True:
			self.lock.acquire()
			img = np.copy(self.image.get_image())
			self.lock.release()
			self.frame = img
			time.sleep(1.0/30)
	def get_frame(self):
		self.lock.acquire()
		ans = np.copy(self.frame)
		self.lock.release()
		cv2.imwrite('test.jpg',ans)
		return ans

 
# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error:
    print 'Failed to create socket'
    sys.exit()
'''
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
'''
#print 'Socket bind complete'

'''
host = 'ec2-35-163-207-7.us-west-2.compute.amazonaws.com'
 
try:
    remote_ip = socket.gethostbyname( host )
 
except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()

print 'Ip address of ' + host + ' is ' + remote_ip
'''
remote_ip = '192.168.0.15'
s.sendto('subscribe', (remote_ip, PORT))



lock = threading.Lock()
u  = UDPreceiver(s,lock)
img_manager = ImageManager(u,lock)
f = FrameUpdater(lock,img_manager)
threads = [ u , f , img_manager]

for t in threads:
	t.start()

while True:
	time.sleep(1.0/30)
	f.get_frame()
	img = cv2.imread('test.jpg')
	cv2.imshow('stream',img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

for t in threads:
	t.join()


    