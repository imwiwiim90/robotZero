import socket
import sys
import time
import RPi.GPIO as GPIO
import json


GPIO.setmode(GPIO.BCM)
out_pins = [i for i in range(12,16)]
"""
12 -> left - front
13 -> left - back
14 -> right - front
15 -> right - back
"""

for pin in out_pins:
    GPIO.setup(pin,GPIO.OUT)

pwms = [GPIO.PWM(pin,15) for pin in out_pins]
for pwm in pwms:
    pwm.start(0)
    pwm.ChangeFrequency(15)

try: 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
HOST = ""
PORT = 8000
current_dutyCycle = 20
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
        	pwm.ChangeDutyCycle(current_dutyCycle)
	GPIO.output(tuple(out_pins),tuple(key_list))
	

prev_keylist = None
while True:
    msg, addr = s.recvfrom(2048)
    keys = json.loads(msg)
    keys = {u'arrows':keys[u'arrows'],
    u'buttons':keys[u'buttons']}
    y_arrow = keys[u'arrows'][1]
    x_arrow = keys[u'arrows'][0]
    pins = [0,0,0,0]

    if keys[u'buttons'][u'R1'] == True:
        current_dutyCycle += 1
    if keys[u'buttons'][u'L1'] == True:
        current_dutyCycle -= 1
    if current_dutyCycle <= 0:
        current_dutyCycle = 1
    if current_dutyCycle >= 100:
        current_dutyCycle = 100

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
    print pins
    change_todo = False
    if prev_keylist == None:
    	prev_keylist = keys
    	change_todo = True
    else:
    	for k in keys:
    		if keys[k] != prev_keylist[k]:
    			change_todo = True
    prev_keylist = keys
    if change_todo:
    	key_actuator(pins)

