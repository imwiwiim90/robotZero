import socket
import sys
import time
import RPi.GPIO as GPIO
import json


GPIO.setmode(GPIO.BCM)
out_pins = [i for i in range(12,14)]
"""
12 -> left - front
13 -> left - back
14 -> right - front
15 -> right - back
"""

for pin in out_pins:
    GPIO.setup(pin,GPIO.OUT)

pwms = [GPIO.PWM(pin) for pin in out_pins]
for pwm in pwms:
    pwm.start(0)
    p.ChangeFrequency(15)

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
    for pwm,key in zip(pwms,key_list):
        if key == 0:
            pwm.ChangeDutyCycle(0)
        else:
            pwm.ChangeDutyCycle(50)
    GPIO.output(tuple(out_pins),tuple(key_list))
	


while True:
	msg, addr = s.recvfrom(2048)
    keys = json.loads(msg)
    y_arrow = keys["hat"]["0"][1]
    x_arrow = keys["hat"]["0"][0]
    pins = [0,0,0,0]
    if y_arrow == 1:
        pins = [1,0,1,0]
    elif y_arrow == -1:
        pins = [0,1,0,1]
    elif x_arrow == 1:
        pins = [1,0,0,1]
    elif x_arrow == -1:
        pins = [0,1,1,0]
    else:
        pins = [0,0,0,0]
        # everything zero
	key_actuator(pins)

