#!/usr/bin/env python
import nxt.locator
from nxt.sensor import *
from nxt.motor import *

IDEAL = 50
SPEED = 50
KP = 1
KI = 1
KD = 1

def run():
	previous_error = 0
	integral = 0

	while true:
		error = IDEAL - LIGHT_SENSOR.get_sample()
		integral += error
		derivative = error - previous_error
		output = KP * error + KI * integral + KD * derivative
		previous_error = error

		LEFT_MOTOR.run(SPEED + output)
		LEFT_MOTOR.run(SPEED - output)

BRICK = nxt.locator.find_one_brick()
LIGHT_SENSOR = Light(BRICK, PORT_1)
print LIGHT_SENSOR.get_sample()
LEFT_MOTOR = Motor(BRICK, PORT_A)
RIGHT_MOTOR = Motor(BRICK, PORT_B)