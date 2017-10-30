#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# Fachhochschule Bielefeld
# Ingenieurwissenschaften und Mathematik
# Ingenieurinformatik - Studienarbeit
# Marcel Bernauer, Michel Asmus, Phil Petschull
# ------------------------------------------------
# project: felix
# main
# edited: 2017-10-27 16:00 (michel)
# ------------------------------------------------

import os
import msvcrt
import time

from leg import leg
from dict_servo import servo_all

DEVICENAME = "COM3".encode('utf-8')

felix = leg(servo_all,DEVICENAME)
felix.enable_torque()
speed=1000
felix.set_speed([speed,speed,speed,speed])
input("Will move to default position")

pos=[0,0,75000,75000]
offset=50
for id in range(len(pos)):
    felix.move_servo_to_position(id, pos[id])
    while felix.get_servo_current_position(id) > (pos[id] + 10) or felix.get_servo_current_position(id) < (pos[id] - 10):
        time.sleep(0.1)


# felix.move_servo_to_position(id, pos)
# while felix.get_servo_current_position(id)>(pos+10) or felix.get_servo_current_position(id)<(pos-10):
#     time.sleep(0.1)
#
# id=1
# felix.move_servo_to_position(id, pos)
# while felix.get_servo_current_position(id)>(pos+10) or felix.get_servo_current_position(id)<(pos-10):
#     time.sleep(0.1)
#
# id=2
# pos=75000
# felix.move_servo_to_position(id, pos)
# while felix.get_servo_current_position(id)>(pos+10) or felix.get_servo_current_position(id)<(pos-10):
#     time.sleep(0.1)
#
# id=3
# pos=75000
# felix.move_servo_to_position(id, pos)
# while felix.get_servo_current_position(id)>(pos+10) or felix.get_servo_current_position(id)<(pos-10):
#     time.sleep(0.1)


trajectory=[[-30000,50000,45000,25000],
            [-15000,45000,50000,45000],
            [0,     0,    45000,45000],
            [15000,-45000,50000,45000],
            [30000,-50000,45000,25000],
            [0,     0,    75000, 45000]]

input("Will run trajectory!")
offset=100
speed=3000
felix.set_speed([speed,speed,speed,speed])
i=0
while True:
    felix.move_to_pos(trajectory[i])
    os.system("cls")
    print("running trajectory!!")
    test=felix.test_position(trajectory[i], offset)
    while test==False:
        time.sleep(0.1)
        test = felix.test_position(trajectory[i], offset)


    i += 1
    if i > 5:
        i = 0

    # if msvcrt.getch().decode()=="e":
    #     break

input("Will diable torque!")
felix.disable_torque()
felix.end_communication()