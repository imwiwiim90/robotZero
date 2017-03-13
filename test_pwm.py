import RPi.GPIO as GPIO
import sys
motor_pins = [20,2,3]
motor_id = 1

GPIO.setmode(GPIO.BCM)
pwms = []
for pin in motor_pins:
	GPIO.setup(pin, GPIO.OUT)
	pwms.append(GPIO.PWM(pin))
	pwms[-1].start(100)

while True:
	try:
		print "Motor - " + str(motor_id)
		print "[0] Change Motor"
		print "[1] Change Frequency"
		print "[2] Change Duty Cycle"
		print "[q] quit"
		i = raw_input('Insert option: ')   # use raw_input for Python 2
		if i == "q":
			break
		if i == "2":
			pwm = float(raw_input('DUTY CYCLE 0.0 - 100.0: '))
			pwms[i-1].ChangeDutyCycle(pwm)
		if i == "1":
			frq = float(raw_input('Frequency: '))
			pwms[i-1].ChangeFrequency(frq)
		if i == "0":
			motor_id = int(raw_input('Id: '))
	except:
		print "Unexpected error:", sys.exc_info()[0]
		break

p.stop()
GPIO.cleanup()