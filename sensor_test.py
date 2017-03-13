import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
TRIG = 0
ECHO = 0

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG,0)
time.sleep(2)
while True:
	

	GPIO.output(TRIG,1)
	time.sleep(0.00001)
	GPIO.output(TRIG,False)

	while GPIO.input(ECHO) == 0:
		pulse_start = time.time()

	while GPIO.input(ECHO) == 1:
		pulse_end = time.time()
		pulse = pulse_end - pulse_start
		distance = pulse*17150
		if distance > 100:
			break
	print distance

