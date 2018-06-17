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
import logging

logger = logging.getLogger(__name__)
logger.debug('Logging in {0} started.'.format(__name__))

from felix import robot

def run_trajectory(leg):
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
    offset = 0.01
    speed = 1000
    leg.set_speed_for_all(speed)
    i = 0
    while True:
        leg.move_to_deg(trajectory_degrees[i])
        leg.test_degrees(trajectory_degrees[i], offset)
        #print("move to point ", i, "with degrees :", trajectory_degrees[i])

        i += 1
        if i > 5: i = 0
        if msvcrt.kbhit() != 0:
            if msvcrt.getwch() == "e":
                break

# jump to main
if __name__ == '__main__':
    # Wake up...
    felix = robot()

    # felix.enable_torque()  # now toggeable!
    felix.toggle_torque()

    speed = 1000
    felix.get_leg().set_speed_for_all(speed)  # check out the new .get_leg() at first!
    input("will move to default position")

    pos = [0, 0, 90, 90]
    offset = 0.005
    for id, pos in enumerate(pos):
        print("will move servo ", id, " to default position")
        felix.get_leg().move_servo_to_degrees(id, pos)
        felix.get_leg().test_servo_degree(id, pos, offset)

    run_trajectory(felix.get_leg())