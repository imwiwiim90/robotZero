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
			time.sleep(0.000001)
			GPIO.output(TRIG,False)
			pulse_start = time.time()
			

			ans = GPIO.wait_for_edge(ECHO, GPIO.FALLING, timeout=int(100*1000/(17150)))
			pulse = time.time() - pulse_start
			distance = pulse*17150

			self.distance = distance



	def get(self):
		return self.distance




tDistance = SDistance(5,6)
tDistance2 = SDistance(19,26)
tDistance2.start()
tDistance.start()
while True:
	time.sleep(1)
	print "d1: " + str(tDistance.get())
	print "d2: " + str(tDistance2.get())

