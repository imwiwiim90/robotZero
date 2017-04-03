import RPi.GPIO as GPIO
import time
import threading


class DistanceSensors(threading.Thread):
	def __init__(self,TRIG,ECHO,agent,N = 5):
		threading.Thread.__init__(self)
		GPIO.setmode(GPIO.BCM)
		self.echo = ECHO
		self.trig = TRIG
		GPIO.setup(TRIG,GPIO.OUT)
		GPIO.setup(ECHO,GPIO.IN,pull_up_down=GPIO.PUD_UP)
		self.agent = agent
		GPIO.output(TRIG,0)
		time.sleep(0.5)
		self.distance = {channel:0 for channel in ECHO}
		self.time_start = {channel: time.time() for channel in ECHO}

		for echo in ECHO:
			GPIO.add_event_detect(echo, GPIO.FALLING)
			GPIO.add_event_callback(echo, self.echo_callback)



	def echo_callback(self,channel):
		self.distance[channel] = (time.time() - self.time_start[channel])*17150
		agent.setDistance(self.echo.index(channel),self.distance[channel])


	def run(self):
		TRIG = self.trig
		ECHO = self.echo
		while True:
			time.sleep(1/30.0)
			GPIO.output(TRIG,1)
			time.sleep(0.000001)
			GPIO.output(TRIG,False)
			self.time_start = {channel: time.time() for channel in ECHO}
			
	def get(self,_id):
		return self.distance[self.echo[_id]]

"""
tDistance = DistanceSensors((5,19),(6,26))
tDistance.start()
while True:
	time.sleep(1)
	print "d1: " + str(tDistance.get(0))
	print "d2: " + str(tDistance.get(1))
"""