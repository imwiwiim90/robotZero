import socket
import sys
import time
import RPi.GPIO as GPIO
import json
import camera
import threading
import random
from distanceSensor import *
import os

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
        self.direction = 'steady'
        out_pins = [12,13,4,27]
        self.speed = 0
        for pin in out_pins:
            GPIO.setup(pin,GPIO.OUT)
        self.pwms = [GPIO.PWM(pin,15) for pin in out_pins]
        for pwm in self.pwms:
            pwm.start(self.speed)
            pwm.ChangeFrequency(15)

        # servos
        self.servos = [{"pin":pin} for pin in [20,21]]
        for serv in self.servos:
            GPIO.setup(serv["pin"],GPIO.OUT)
            serv["pwm"] = GPIO.PWM(serv["pin"],50)
            serv["pwm"].start(5.5)
            serv["dcycle"] = 5.5

        self.last_right = 0
        self.last_left = 0


        
    def set_direction(self,direction,hard=False):
        if self.direction == direction and not hard:
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

        for pwm,i in zip(self.pwms,dcycle):
            if i == 0:
                pwm.ChangeDutyCycle(0)
            else:
                pwm.ChangeDutyCycle(self.speed)
        self.direction = direction

    def change_velocity(self,direction):
        if direction == "up":
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
        elif keys[u'arrows'][u'x'] == 1:
            self.set_direction('right')
        elif keys[u'arrows'][u'y'] == -1:
            self.set_direction('back')
        elif keys[u'arrows'][u'y'] == 1:
            self.set_direction('front')
        else:
            self.set_direction('steady')

        if keys[u'buttons'][u'PLAY']:
            # system shutdown
            os.system("sudo shutdown -h now")

        self.setMovement(keys[u'joysticks'][u'left'][u'x'],keys[u'joysticks'][u'left'][u'y'])

        self.lockServo(keys[u'buttons'][u'X'])

        self.setServo(0,keys[u'back_buttons'][u'L'])
        self.setServo(1,keys[u'back_buttons'][u'R'])

    def lockServo(self,lock):
        self.serv_lock = lock

    def setServo(self,servo,val):
        if self.serv_lock == True:
            return

        dcycle = val*8.5/2.0 + 2
        dcycle = int(dcycle*2)/2.0

        lastv = self.servos[servo]['dcycle']
        if lastv != dcycle:
            self.servos[servo]['pwm'].ChangeDutyCycle(dcycle)
            self.servos[servo]['dcycle'] = dcycle

    def setMovement(self,x,y):
        y = int((y+1)*5)/5.0 - 1
        x = int((x+1)*5)/5.0 - 1

        left  = y - x
        right = y + x

        left =  (1 if left >  1 else left)
        left =  (-1 if left < -1 else left)
        right = (-1 if right < -1 else right)
        right = (1 if right >  1 else right)

        if left == self.last_left and right == self.last_right:
            return

        if left != self.last_left:
            self.last_left = left
            if left < 0:
                self.pwms[2].ChangeDutyCycle( 0 )
                self.pwms[3].ChangeDutyCycle( -left )
            else:
                self.pwms[3].ChangeDutyCycle( 0 )
                self.pwms[2].ChangeDutyCycle( left )

        if right != self.last_right:
            self.last_right = right
            if right < 0:
                self.pwms[0].ChangeDutyCycle( 0 )
                self.pwms[1].ChangeDutyCycle( -right )
            else:
                self.pwms[1].ChangeDutyCycle( 0 )
                self.pwms[0].ChangeDutyCycle( right )
                





# TODO
# if can detect rising edge while PWM


class KeyMTest(object):
    def __init__(self):
        pass
    def setKeys(self,k):
        pass
class SensorTest(threading.Thread):
    def __init__(self,b_dcast):
        threading.Thread.__init__(self)
        self.bcast = b_dcast

    def run(self):
        while True:
            time.sleep(1/2.0)
            self.bcast.sendData('hey there','sensor')





class SocketListener(threading.Thread):
    def __init__(self,PORT,d_bcast,keys_manager):
        threading.Thread.__init__(self)
        self.bcast = d_bcast
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
        self.bcast.set_socket(s)

    def run(self):
        while True:
            msg, addr = self.sckt.recvfrom(CHUNK_SIZE)
            self.bcast.addIP(addr)
            self.km.setKeys(json.loads(msg))

            
class VideoBroadcast(threading.Thread):
    def __init__(self,camera,lock,d_bcast):
        threading.Thread.__init__(self)
        self.cam = camera
        self.bcast = d_bcast
        self.lock = lock


    def run(self):
        while True:
            time.sleep(1.0/30.0)
            chunks = self.cam.get_image_slides() # video
            random.shuffle(chunks)
            self.lock.acquire()
            for chunk in chunks:
                self.bcast.sendData(chunk,'video')
            self.lock.release()

    def set_socket(self,skt):
        self.sckt = skt


class DataBroadcast(object):
    def __init__(self,limit=2):
        self.ips = {}
        self.limit = limit


    def addIP(self,addr):
        ip = str(addr[0]) + ":" + str(addr[1])
        if not (ip in self.ips.keys()):
            if len(self.ips) == self.limit:
                self.ips.pop(ip,None)
            self.ips[ip] = addr

    def sendData(self,msg,msg_type):
        flag = ''
        if msg_type == 'video':
            flag = chr(0) + chr(0)
        if msg_type == 'sensor':
            flag = chr(0) + chr(1)

        for ip in self.ips.keys():
            try:
                self.sckt.sendto( flag + msg , self.ips[ip])
            except socket.error, (no,msg):
                if no == socket.errno.ENETUNREACH:
                    pass
    def set_socket(self,skt):
        self.sckt = skt

class DistanceTest(object):
    def __init__(self):
        pass
    def get(self):
        return 12
    def start(self):
        pass

#error_file = open('error.log','w')
#sys.stderr = error_file
lock = threading.Lock()
key_m = Agent()
#key_m = KeyMTest()
data_broadcast = DataBroadcast(limit=1)
#video_broad = VideoBroadcast(camera.VideoCamera(),lock,data_broadcast)
skt_manager = SocketListener(8000,data_broadcast,key_m)

#distanceSensors = DistanceSensors((5,19),(6,26))

skt_manager.start()
#video_broad.start()
#distanceSensors.start()

while True:
    time.sleep(1/30.0)
    sensor_data = {
        #"left" :  distanceSensors.get(0),
        #"right" : distanceSensors.get(1),
        "speed" : key_m.speed,
    }
    lock.acquire()
    data_broadcast.sendData(json.dumps(sensor_data),'sensor')
    lock.release()
    print sensor_data


skt_manager.join()
video_broad.join()