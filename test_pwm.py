import RPi.GPIO as GPIO
import sys
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13,1)
p = GPIO.PWM(12)
p.start(100)
while True:
	try:
		print "[1] Change Frequency"
		print "[2] Change Duty Cycle"
		print "[q] quit"
		i = raw_input('Insert option: ')   # use raw_input for Python 2
		if i == "q":
			break
		if i == "2":
			pwm = float(raw_input('DUTY CYCLE 0.0 - 100.0: '))
			p.ChangeDutyCycle(pwm)
		if i == "1":
			frq = float(raw_input('Frequency: '))
			p.ChangeFrequency(frq)
	except:
		print "Unexpected error:", sys.exc_info()[0]
		break

p.stop()
GPIO.cleanup()