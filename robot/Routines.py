import threading
import time

class Seesaw(threading.Thread):
    def __init__( self,agent ):
        threading.Thread.__init__(self)
        self.agent = agent
        self.terminate = False

    def run(self):
        agent = self.agent
        straight_time = 2
        time_start  = time.time()
        speed_aux   = agent.speed
        agent.speed = 100
        agent.set_direction("front")
        while True:
            if self.terminate:
                break
            if time.time() - time_start > straight_time:
                break
            time.sleep(0.01)
        agent.speed = speed_aux
        agent.set_direction("steady")
        self.end()

    def end(self):
        self.terminate = True


class Test(threading.Thread):
    def __init__( self,agent ):
        threading.Thread.__init__(self)
        self.agent = agent
        self.terminate = False

    def run(self):
        while True:
            time.sleep(0.5)
            print "in routine"
            if self.terminate:
                break

    def end(self):
        self.terminate = True

class FollowWall(threading.Thread):
    def __init__( self,agent ):
        threading.Thread.__init__(self)
        self.agent = agent
        self.terminate = False

    def run(self):
        while True:
                time.sleep(0.01)
                break

    def end(self):
        self.terminate = True

class StraightWalls(threading.Thread):
    def __init__( self,agent ):
        threading.Thread.__init__(self)
        self.agent = agent
        self.terminate = False

    def run(self):
        agent = self.agent
        speed_aux   = agent.speed
        agent.setMovement(0,0.5)
        turn_state = "left"
        while True:
            if self.terminate:
                break
            if turn_state == "left":
                if agent.distances[0] < 30:
                    turn_state = "right"
                    agent.setMovement(-0.05,0.5)
                if agent.distances[1] < 25:
                    agent.setMovement(0.4,0.5)
            if turn_state == "right":
                if agent.distances[1] < 30:
                    turn_state = "left"
                    agent.setMovement(0.1,0.5)
                if agent.distances[0] < 25:
                    agent.setMovement(-0.3,0.5)
            time.sleep(0.01)
        agent.speed = speed_aux
        agent.set_direction("steady")
        self.end()

    def end(self):
        self.terminate = True
