import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BCM)

TRIG = (5,19)
ECHO = (6,26)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

time_start = (time.time(),time.time())

def my_callback_one(channel):
    print "d1:" + str((time.time() - time_start[0])*17150) 

def my_callback_two(channel):
    print "d2:" + str((time.time() - time_start[1])*17150) 

GPIO.add_event_detect(ECHO[1], GPIO.FALLING)
GPIO.add_event_detect(ECHO[0], GPIO.FALLING)
GPIO.add_event_callback(ECHO[0], my_callback_one)
GPIO.add_event_callback(ECHO[1], my_callback_two)


while True:
	try:
		print "sending"
		GPIO.output(TRIG,1)
		time.sleep(0.000001)
		GPIO.output(TRIG,0)
		time.sleep(0.1)
	except KeyboardInterrupt:
		GPIO.cleanup()
		break


