import pyglet
import time


class PS4Controller(object):
	def __init__(self):
		self.joystick = pyglet.input.get_joysticks()[0]

	def getKeys(self):
		j = self.joystick
		j.open()
		keys = {
			'joysticks' : {
				"left": {
					"x" : j.x,
					"y" : -j.y,
				},
				"right": {
					"x" : j.z,
					"y" : -j.rz,
				}
			},
			'arrows' : {
				'x' : j.hat_x,
				'y' : j.hat_y,
			},
			"back_buttons" : {
				"L" : j.rx+1,
                "R" : j.ry+1,
			},
			"buttons" : {
                "X" : j.buttons[1],
                "O" : j.buttons[2],
                "T" : j.buttons[3],
                "S" : j.buttons[0],
                "L1" : j.buttons[4],
                "R1" : j.buttons[5],
                "R2" : j.buttons[7],
                "R3" : j.buttons[11],
                "PLAY" : j.buttons[12],
            },
		}

		j.close()
		return keys

ps4 = PS4Controller()
while True:
	time.sleep(0.1)
	print ps4.getKeys()
