#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# Fachhochschule Bielefeld
# Ingenieurwissenschaften und Mathematik
# Ingenieurinformatik - Studienarbeit
# Marcel Bernauer, Michel Asmus, Phil Petschull
# ------------------------------------------------
# project: felix
# leg-class by michel
# edited: 2017-10-19 16:00 (marcel)
# ------------------------------------------------
# TODO:
# a) from servo import servo
# b) for servo in self.servos
# c) debug at import


import os

try:
    import servo
except Exception as e:
    print("Error: Importing servo failed!")
    print(e)


class leg:

    # =======================================
    # Public class attributes
    # =======================================

    # none...

    # =======================================
    # Private methods
    # =======================================

    # Constructor intializes its motors
    def __init__(self, servo_dict, DEVICENAME):
        self.servos = list()
        self.num_servo = 0
        for i in servo_dict:
            self.num_servo += 1
            self.servos.append(servo.servo(i["ID"], i["BAUDRATE"],
                                           i["POSITION_MINIMUM"], i["POSITION_MAXIMUM"],
                                           i["SPEED_MAXIMUM"], i["CLOCKWISE"], DEVICENAME))
        self.servos[0].initialize_port()

    # =======================================
    # Public methods
    # =======================================

    # Activates power consumption for halting position on all motors
    def enable_torque(self):
        for i in self.servos:
            i.enable_torque()

    # Deactivates power consumption for manual operation on all motors
    def disable_torque(self):
        for i in self.servos:
            i.disable_torque()

    # Moves all motors to its target positions
    def move_to_pos(self, pos):
        # ToGo
        # current_position=self.get_current_position()
        # path=list()
        # #legth of path
        # for i in range(self.num_servo):
        #     path.append(abs(current_position[i]-pos[i]))
        # #find longest path
        # index_longest_path=-1
        # longest_path=0
        # for j in range(self.num_servo):
        #     if path[j]>longest_path:
        #         longest_path=path[j]
        #         index_longest_path=j
        # speed=[1]*self.num_servo
        for l in range(self.num_servo):
            self.servos[l].write_position(pos[l])

    # Sets desired velocity of movement for all motors
    def set_speed(self, speed):
        for i in range(len(self.servos)):
            self.servos[i].write_velocity(speed[i])

    # Gets a list of present positions from all motors
    def get_current_position(self):
        position = list()
        for i in self.servos:
            position.append(i.read_present_position())
        return position
