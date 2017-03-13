import socket
import sys
import time
#import RPi.GPIO as GPIO
import json
import camera
import threading
import random

CHUNK_SIZE = 4096


"""
12 -> left - front
13 -> left - back
4 -> right - front
27 -> right - back
"""


class Agent(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.direction = steady
        out_pins = [12,13,4,27]
        self.speed = 0
        for pin in out_pins:
            GPIO.setup(pin,GPIO.OUT)
        self.pwms = [GPIO.PWM(pin,15) for pin in out_pins]
        for pwm in self.pwms:
            pwm.start(self.speed)
            pwm.ChangeFrequency(15)
        
    def set_direction(self,direction,hard=False):
        if self.direction == direction && not hard:
            return
        if direction == "left":
            dcycle = [0,1,1,0]
        if direction == "right":
            dcycle = [1,0,0,1]
        if direction == "back":
            dcycle = [0,1,0,1]
        if direction == "front":
            dcycle = [1,0,1,0]
        if direction == "steady":
            dcycle = [0,0,0,0]

        for pwm,i in zip(pwms,dcycle):
            if i == 0:
                pwm.ChangeDutyCycle(0)
            else:
                pwm.ChangeDutyCycle(self.speed)
        self.direction = direction

    def change_velocity(self,direction):
        if direction == "up"
            self.speed += 1
        else:
            self.speed -= 1

        if self.speed > 100:
            self.speed = 100
        if self.speed < 0:
            self.speed = 0


    def setKeys(self,keys):
        if keys[u'buttons'][u'R1']:
            self.change_velocity('up')
        if keys[u'buttons'][u'L1']:
            self.change_velocity('down')

        if keys[u'arrows'][u'x'] == -1:
            self.set_direction('left')
        else if keys[u'arrows'][u'x'] == 1:
            self.set_direction('right')
        else if keys[u'arrows'][u'y'] == -1:
            self.set_direction('left')
        else if keys[u'arrows'][u'y'] == 1:
            self.set_direction('right')
        else:
            self.set_direction('steady')



class SocketListener(threading.Thread):
    def __init__(self,PORT,video,keys_manager):
        threading.Thread.__init__(self)
        self.video = video
        self.km = keys_manager
        try: 
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error:
            print 'Failed to create socket'
            sys.exit()
        try:
            s.bind(("", PORT)) # as server
        except socket.error , msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()
        print 'Socket bind complete'
        self.sckt = s
        self.video.set_socket(s)

    def run(self):
        while True:
            msg, addr = self.sckt.recvfrom(CHUNK_SIZE)
            self.video.addIP(addr)
            self.km.setKeys(json.loads(msg))

            
class VideoBroadcast(threading.Thread):
    def __init__(self,camera,limit=10):
        threading.Thread.__init__(self)
        self.ips = {}
        self.limit = limit
        self.cam = camera
        self.lock = threading.Lock()

    def run(self):
        while True:
            time.sleep(1.0/30.0)
            chunks = self.cam.get_image_slides() # video
            random.shuffle(chunks)
            self.lock.acquire()
            for chunk in chunks:
                for ip in self.ips.keys():
                    self.sckt.sendto(chr(0)+chr(0)+chunk , self.ips[ip]) #video type
            self.lock.release()

    def addIP(self,addr):
        ip = str(addr[0]) + ":" + str(addr[1])
        if not (ip in self.ips.keys()):
            self.lock.acquire()
            if len(self.ips) == self.limit:
                self.ips.pop(ip,None)
            self.ips[ip] = addr
            self.lock.release()

    def set_socket(self,skt):
        self.sckt = skt

error_file = open('error.log','w')
sys.stderr = error_file

key_m = Agent()
video_broad = VideoBroadcast(camera.VideoCamera(),limit=2)
skt_manager = SocketListener(8000,video_broad,key_m)

skt_manager.start()
video_broad.start()


skt_manager.join()
video_broad.join()