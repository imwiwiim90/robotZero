import RPi.GPIO as GPIO
import time
#190.14.232.243
GPIO.setmode(GPIO.BCM)
TRIG = 5
ECHO = 6

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(TRIG,0)
time.sleep(2)
while True:
	

	GPIO.output(TRIG,1)
	time.sleep(0.00001)
	GPIO.output(TRIG,False)

	time_flag = time.time()
	pulse_start = time.time()
	timeout = GPIO.wait_for_edge(ECHO, GPIO.RISING, timeout=500)
	pulse_start = time.time()
	"""
	while GPIO.input(ECHO) == 0:
		pulse_start = time.time()
		if pulse_start - time_flag > 2:
			break
	"""
	if timeout == None:
		print "first timeout"
	distance = 0

	timeout = GPIO.wait_for_edge(ECHO, GPIO.FALLING, timeout=int(100*1000/(17150)))
	pulse = time.time() - pulse_start
	distance = pulse*17150

	"""
	while GPIO.input(ECHO) == 1:
		pulse_end = time.time()
		pulse = pulse_end - pulse_start
		distance = pulse*17150
		if distance > 100:
			break
	"""
	print distance

