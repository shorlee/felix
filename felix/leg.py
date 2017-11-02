#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# Fachhochschule Bielefeld
# Ingenieurwissenschaften und Mathematik
# Ingenieurinformatik - Studienarbeit
# Michel Asmus, Marcel Bernauer, Phil Petschull
# ------------------------------------------------
# project: felix
# leg-class
# ------------------------------------------------


import os
import time

try:
    from servo import servo
except Exception as e:
    print("Error: Importing servo failed!")
    print(e)


class leg:

    # =======================================
    # Public class attributes
    # =======================================

    torque = False

    sampling = 4    # seconds to wait for queries

    # =======================================
    # Private methods
    # =======================================

    # Constructor intializes its motors
    def __init__(self, servo_dict, DEVICENAME):
        self.servos = list()
        self.num_servo = 0
        for i in servo_dict:
            self.num_servo += 1
            self.servos.append(servo(i["ID"], i["BAUDRATE"],
                                     i["POSITION_MINIMUM"], i["POSITION_MAXIMUM"],
                                     i["SPEED_MAXIMUM"], i["CLOCKWISE"], DEVICENAME))
        self.servos[0].initialize_port()

    # =======================================
    # Public methods
    # =======================================

    # Activates power consumption for halting position on all motors
    def enable_torque(self):
        leg.torque = True
        for i in self.servos:
            i.enable_torque()

    # Deactivates power consumption for manual operation on all motors
    def disable_torque(self):
        leg.torque = False
        for i in self.servos:
            i.disable_torque()

    # Moves all motors to its target positions given in ticks
    def move_to_pos(self, pos):
        for i in range(self.num_servo):
            self.servos[i].write_position(pos[i])

    # Moves all motors to its target positions given in degrees
    def move_to_deg(self, deg):
        pos=list()
        for i in range(len(deg)):
            pos.append(self.servos[i].deg_to_tick(deg[i]))
        leg.move_to_pos(self,pos)

    # Moves only one motor to its target positions in ticks
    def move_servo_to_position(self, servoID, pos):
        self.servos[servoID].write_position(pos)

    # Moves only one motor to its target positions in degrees
    def move_servo_to_degrees(self, servoID, deg):
        self.servos[servoID].write_position(int(self.servos[servoID].deg_to_tick(deg)))

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

    # Get present position only for one servo in ticks
    def get_servo_current_position(self, servoID):
        return self.servos[servoID].read_present_position()

    # Get present position only for one servo in degree
    def get_servo_current_degree(self, servoID):
        return self.servos[servoID].tick_to_deg(self.servos[servoID].read_present_position())

    # Convert degrees into ticks
    def degrees_to_ticks(self,deg):
        ticks=list()
        for i in range(len(deg)):
            ticks.append(self.servos[i].deg_to_tick(deg[i]))
        return ticks

    # Test is present position in ticks is in range pos +- offset for all servos
    def test_position(self,pos,offset):
        current_pos=self.get_current_position()
        for i in range(len(pos)):
            if  (pos[i]>(current_pos[i]+offset) or pos[i]<(current_pos[i]-offset)):
                return False
            else:
                return True

    # Test is present position in degrees is in range deg +- offset for all servos
    def test_degrees(self,deg,offset):
        pos=list()
        offset_deg=self.servos[0].deg_to_tick(offset)
        for i in range(len(deg)):
            pos.append(self.servos[i].deg_to_tick(deg[i]))
        print("pos: ",pos)
        print("offset: ",offset_deg)
        while leg.test_position(self,pos,offset_deg) is False:
            time.sleep(self.sampling)
        return True

    # Close communication with servos
    def end_communication(self):
        self.servos[0].close_port
        return