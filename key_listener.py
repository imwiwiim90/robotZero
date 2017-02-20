import socket
import sys
import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
out_pins = [i for i in range(12,16)]
for pin in out_pins:
    GPIO.setup(pin,GPIO.OUT)

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
    GPIO.output(tuple(out_pins),tuple(key_list))
	


while True:
	msg, addr = s.recvfrom(2048)
	keys = [0 if k == "0" else 1 for k in msg[:4]]
	key_actuator(keys)

