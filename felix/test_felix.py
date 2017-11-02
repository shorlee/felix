#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# Fachhochschule Bielefeld
# Ingenieurwissenschaften und Mathematik
# Ingenieurinformatik - Studienarbeit
# Michel Asmus, Marcel Bernauer, Phil Petschull
# ------------------------------------------------
# project: felix
# test
# ------------------------------------------------

import os
import msvcrt
import time

from felix import robot

# Wake up...
felix = robot()

#DEVICENAME = "COM3".encode('utf-8')   # needless: constructor cares of you!


#felix.enable_torque()  # now toggeable!
felix.toggle_torque()

speed = 1000
felix.get_leg().set_speed([speed, speed, speed, speed]) # check out the new .get_leg() at first!
input("will move to default position")

pos = [0, 0, 90, 90]
offset = 0.5
for id in range(len(pos)):
    print("will move servo ", id, " to default position")
    felix.get_leg().move_servo_to_degrees(id, pos[id])
    while felix.get_leg().get_servo_current_degree(id) > (pos[id] + offset) or felix.get_leg().get_servo_current_degree(id) < (
        pos[id] - offset):
        time.sleep(0.1)

# trajectory_ticks=   [[-30000,50000,45000,25000],
#                     [-15000,45000,50000,45000],
#                     [0,     0,    45000,45000],
#                     [15000,-45000,50000,45000],
#                     [30000,-50000,45000,25000],
#                     [0,     0,    75000, 45000]]

trajectory_degrees = [[-35, 60, 55, 30],
                      [-18, 55, 60, 55],
                      [0, 0, 55, 55],
                      [18, -55, 60, 55],
                      [35, -60, 55, 30],
                      [0, 0, 90, 55]]

input("will run trajectory!")
os.system("cls")
print("running trajectory!")
print("press 'e' to end")
offset = 0.1
speed = 1000
felix.get_leg().set_speed([speed, speed, speed, speed])
i = 0
while True:
    felix.get_leg().move_to_deg(trajectory_degrees[i])
    test = felix.get_leg().test_degrees(trajectory_degrees[i], offset)
    print("move to point ", i, "with degrees :", trajectory_degrees[i])

    i += 1
    if i > 5: i = 0
    if msvcrt.kbhit() != 0:
        if msvcrt.getwch() == "e":
            break

# following is needless, destructor does this safely!

#disable = input("disable torque? (y)")
#if disable == "y":
#    felix.get_leg().disable_torque()

#felix.get_leg().end_communication()
