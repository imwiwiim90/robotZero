import socket
import sys
import time
import threading


try: 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

#HOST = "192.168.0.15"
HOST = "127.0.0.1"
PORT = 8000


class KeyManager(threading.Thread):
	def __init__(self,lock):
		threading.Thread.__init__(self)
		self.keys = list("0000")
		self.lock = lock

	def run(self):
		while True:
			time.sleep(0.2)
			s.sendto(self.getKeyState(), (HOST,PORT))

	def setKeyState(self,key,state):
		self.lock.acquire()
		self.keys[key] = ("1" if state else "0")
		self.lock.release()


	def getKeyState(self):
		lock.acquire()
		s = ''.join(self.keys)
		lock.release()
		return s

from pynput.keyboard import Key, Listener

lock = threading.Lock()
keyM = KeyManager(lock)
keyM.start()
key_map = {
	Key.shift_r: 0,
	Key.shift: 1,
	Key.alt_r: 2,
	Key.alt_l: 3,
}
def on_press(key):
    if key in key_map.keys():
    	keyM.setKeyState(key_map[key],True)

def on_release(key):
    if key in key_map.keys():
    	keyM.setKeyState(key_map[key],False)

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

