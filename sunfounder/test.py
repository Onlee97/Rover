#!/usr/bin/env python
'''
**********************************************************************
* Filename    : ultra_sonic_avoidance.py
* Description : An example for sensor car kit to followe light
* Author      : Dream
* Brand       : SunFounder
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Dream    2016-09-27    New release
**********************************************************************
'''

#from SunFounder_Ultrasonic_Avoidance import Ultrasonic_Avoidance
from picar import front_wheels
from picar import back_wheels
import time
import picar
import random
import curses
import time

#force_turning = 0    # 0 = random direction, 1 = force left, 2 = force right, 3 = orderdly

picar.setup()

#ua = Ultrasonic_Avoidance.Ultrasonic_Avoidance(20)
fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')
fw.turning_max = 45

forward_speed = 70
backward_speed = 70

back_distance = 10
turn_distance = 20

timeout = 10
last_angle = 90
last_dir = 0
def rand_dir():
	global last_angle, last_dir
	if force_turning == 0:
		_dir = random.randint(0, 1)
	elif force_turning == 3:
		_dir = not last_dir
		last_dir = _dir
		print('last dir  %s' % last_dir)
	else:
		_dir = force_turning - 1
	angle = (90 - fw.turning_max) + (_dir * 2* fw.turning_max)
	last_angle = angle
	return angle

def opposite_angle():
	global last_angle
	if last_angle < 90:
		angle = last_angle + 2* fw.turning_max
	else:
		angle = last_angle - 2* fw.turning_max
	last_angle = angle
	return angle

def start_avoidance():
	print('start_avoidance')

	count = 0
	while True:
		distance = ua.get_distance()
		print("distance: %scm" % distance)
		if distance > 0:
			count = 0
			if distance < back_distance: # backward
				print( "backward")
				fw.turn(opposite_angle())
				bw.backward()
				bw.speed = backward_speed
				time.sleep(1)
				fw.turn(opposite_angle())
				bw.forward()
				time.sleep(1)
			elif distance < turn_distance: # turn
				print("turn")
				fw.turn(rand_dir())
				bw.forward()
				bw.speed = forward_speed
				time.sleep(1)
			else:
				fw.turn_straight()
				bw.forward()
				bw.speed = forward_speed

		else:						# forward
			fw.turn_straight()
			if count > timeout:  # timeout, stop;
				bw.stop()
			else:
				bw.backward()
				bw.speed = forward_speed
				count += 1

def stop():
	bw.stop()
	fw.turn_straight()

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)
delaytime = 0.2

fwAngle = 90
def fwTurn(c):
    global fwAngle
    if (c == "left"):
        if (fwAngle != 45):
            fwAngle -= 45
    if (c == "right"):
        if (fwAngle != 135):
            fwAngle += 45
    return fwAngle

bwSpeed = 0
def bwDrive(c):
    global bwSpeed
    if (c == "stop"):
        bwSpeed = 0
    elif (c == "up" and bwSpeed != 100):
        c += 25
    elif (c == "down" and bwSpeed != 0):
        c -= 25
    return bwSpeed


if __name__ == '__main__':
#	try:
#		start_avoidance()
#	except KeyboardInterrupt:
#		stop()
    while(True):
        char = screen.getch()
        if char == ord('q'):
            break
        elif char == ord('e'):
            print('e')
            bw.stop()
            time.sleep(delaytime)
        elif char == ord('w'):
            print('w')
            bw.speed = 70
#            bw.forward()
            bw.backward()
            time.sleep(delaytime)
        elif char == ord('s'):
            print('s')
            bw.speed = 70
#            bw.backward()
            bw.forward()
            time.sleep(delaytime)
        elif char == ord('a'):
            print('a')
            fw.turn(fwTurn("left"))
            time.sleep(delaytime)
        elif char == ord('d'):
            print('d')
            fw.turn(fwTurn("right"))
            time.sleep(delaytime)
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    stop()
    time.sleep(delaytime)
		#		fw.turn(opposite_angle())
		#		bw.backward()
		#		bw.speed = backward_speed
		#		time.sleep(1)
		#		fw.turn(opposite_angle())
		#		bw.forward()
		#		time.sleep(1)
