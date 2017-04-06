from controller_alt import PS4Controller
from MessageUDP import MessageUDP
from videoStream import Video
import cv2
import json
import threading
import time

lock = threading.Lock()

ip_dir = '192.168.0.4'
#ip_dir = '127.0.0.1'
#ip_dir = '186.28.50.10'
ctrl = PS4Controller()
mailer = MessageUDP()

mailer.set_destination(ip_dir,8000)
video = Video(mailer.socket,ip_dir,8000)
udpReceiver = video.u
video.start()



while True:
	time.sleep(1/30.0)
	message = ctrl.getKeys()
	#print message
	if udpReceiver.in_routine == True:
		print message["buttons"]['T']
		if message["buttons"]['T'] == False:
			continue
	mailer.send(json.dumps(message))
	img = video.getFrame()
	cv2.imshow('stream',img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

