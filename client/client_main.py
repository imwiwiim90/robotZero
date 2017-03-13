from controller import PS4Controller
from MessageUDP import MessageUDP
import json
import threading
import time

lock = threading.Lock()


ctrl = PS4Controller(lock,1/6.0)
mailer = MessageUDP()
mailer.set_destination('192.168.0.15',8000)

ctrl.start()

while True:
	time.sleep(1/60.0)
	message = ctrl.getKeys()
	#print message
	mailer.send(json.dumps(message))


