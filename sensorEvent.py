import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BCM)

TRIG = 5
channel = 6

GPIO.setup(TRIG, GPIO.OUT)

def my_callback_one(channel):
    print('Callback one')

def my_callback_two(channel):
    print('Callback two')

GPIO.add_event_detect(channel, GPIO.FALLING)
GPIO.add_event_callback(channel, my_callback_one)

GPIO.output(TRIG,1)
time.sleep(0.000001)
GPIO.output(TRIG,False)
time.sleep(2)
"""
class SDistance(threading.Thread):
	def __init__(self,trig_pin,echo_pin,N = 5):
		threading.Thread.__init__(self)
		GPIO.setmode(GPIO.BCM)
		self.echo = echo_pin
		self.trig = trig_pin
		GPIO.setup(trig_pin,GPIO.OUT)
		GPIO.setup(echo_pin,GPIO.IN)

		GPIO.output(trig_pin,0)
		time.sleep(0.5)
		self.distance = 0
		self.data = []
		self.N = N


	def run(self):
		TRIG = self.trig
		ECHO = self.echo
		while True:
			time.sleep(1/30.0)
			GPIO.output(TRIG,1)
			time.sleep(0.000001)
			GPIO.output(TRIG,False)
			pulse_start = time.time()
			
			try:
				ans = GPIO.wait_for_edge(ECHO, GPIO.FALLING, timeout=int(100*10000/(17150)))
			except:
				continue
			pulse = time.time() - pulse_start
			distance = pulse*17150
			if len(self.data) >= self.N:
				l = self.data.pop(-1)
			self.data.append(distance)
			s = 0
			for i in self.data:
				s += i
			self.distance = s/float(self.N)





	def get(self):
		return self.distance
"""


"""
tDistance = SDistance(5,6)
tDistance2 = SDistance(19,26)
tDistance2.start()
tDistance.start()
while True:
	time.sleep(1)
	print "d1: " + str(tDistance.get())
	print "d2: " + str(tDistance2.get())
"""
