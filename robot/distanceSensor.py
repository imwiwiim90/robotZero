import RPi.GPIO as GPIO
import time
import threading

class SDistance(threading.Thread):
	def __init__(self,trig_pin,echo_pin):
		threading.Thread.__init__(self)
		GPIO.setmode(GPIO.BCM)
		self.echo = echo_pin
		self.trig = trig_pin
		GPIO.setup(trig_pin,GPIO.OUT)
		GPIO.setup(echo_pin,GPIO.IN)

		GPIO.output(trig_pin,0)
		time.sleep(0.5)
		self.distance = 0


	def run(self):
		TRIG = self.trig
		ECHO = self.echo
		while True:
			GPIO.output(TRIG,1)
			time.sleep(0.00001)
			GPIO.output(TRIG,False)

			time_flag = time.time()
			pulse_start = time.time()
			while GPIO.input(ECHO) == 0:
				pulse_start = time.time()
				if pulse_start - time_flag > 2:
					break

			distance = 0
			while GPIO.input(ECHO) == 1:
				pulse_end = time.time()
				pulse = pulse_end - pulse_start
				distance = pulse*17150
				if distance > 100:
					break
			self.distance = distance



	def get(self):
		return self.distance



"""
tDistance = SDistance(5,6)
tDistance.start()
while True:
	time.sleep(1)
	print tDistance.get()
"""