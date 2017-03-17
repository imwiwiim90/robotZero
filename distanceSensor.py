import RPi.GPIO as GPIO
import time
import threading

class SDistance(threading.Thread):
	def __init__(self,trig_pin,echo_pin):
		threading.Thread.__init__(self)
		self.echo = echo_pin
		self.trig = trig_pin
		GPIO.setup(trig_pin,GPIO.OUT)
		GPIO.setup(echo_pin,GPIO.IN)

		GPIO.output(trig_pin,0)
		time.sleep(0.5)


	def run(self):
		TRIG = self.trig_pin
		ECHO = self.echo_pin
		while True:
			GPIO.output(TRIG,1)
			time.sleep(0.00001)
			GPIO.output(TRIG,False)

			GPIO.wait_for_edge(ECHO, GPIO.RISING)
			pulse_start = time.time()

			GPIO.wait_for_edge(ECHO, GPIO.FALLING, timeout=6)
			pulse_end = time.time()
			pulse = pulse_end - pulse_start
			distance = pulse*17150

			self.distance = distance



	def get(self):
		return self.distance




tDistance = SDistance(5,6)
while True:
	time.sleep(100)
	print tDistance.get()
