#!/usr/bin/env python
import time
import nxt.locator
from nxt.sensor import *
from nxt.motor import *

WHITE = 50.0
BLACK = 30.0
SPEED = 20.0

DIFF = WHITE - BLACK
IDEAL = (WHITE + BLACK) / 2.0
MAX_OUTPUT = 50
MAX_I = 15

KP = 10.0
KI = 0.4
KD = 100.0

DEBUG = False

def run():
	previous_error = 0.0
	integral = 0.0

	while True:
		error = (IDEAL - get_light()) / (DIFF / 2)
		integral += error
		if integral > MAX_I: integral = MAX_I
		elif integral < -MAX_I: integral = -MAX_I
		derivative = error - previous_error
		output = KP * error + KI * integral + KD * derivative
		previous_error = error

		if DEBUG:
			print "------\n"
			print KP * error
			print KI * integral
			print KD * derivative

		if output > MAX_OUTPUT: output = MAX_OUTPUT
		if output < -MAX_OUTPUT: output = -MAX_OUTPUT
		LEFT_MOTOR.run(SPEED + output)
		RIGHT_MOTOR.run(SPEED - output)

		time.sleep(0.01)

def get_light():
	return LIGHT_SENSOR.get_sample() / 10.0

BRICK = nxt.locator.find_one_brick()
LIGHT_SENSOR = Light(BRICK, PORT_1)
LIGHT_SENSOR.set_illuminated(True)
LEFT_MOTOR = Motor(BRICK, PORT_A)
RIGHT_MOTOR = Motor(BRICK, PORT_B)

try:
	run()
except:
	LEFT_MOTOR.run(0)
	RIGHT_MOTOR.run(0)