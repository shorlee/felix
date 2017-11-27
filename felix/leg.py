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

    #TODO: configure debug-structure (leg)

    # trace activation of torque
    torque = False

    # Set True to get debug-info
    debug = False

    sampling = 0.1    # seconds to wait for queries

    # =======================================
    # Private methods
    # =======================================

    # Constructor intializes its motors
    def __init__(self, data, DEVICENAME):

        # save reference to dictionary
        self.leg_data = data


        #TODO: optimize leg initialization

        # build servo objects
        self.servos = list()
        self.num_servo = 0
        for servo_dict in self.leg_data["servos"]:
            self.num_servo += 1
            self.servos.append(servo(servo_dict["ID"], servo_dict["BAUDRATE"],
                                     servo_dict["POSITION_MINIMUM"], servo_dict["POSITION_MAXIMUM"],
                                     servo_dict["CLOCKWISE"], DEVICENAME))
        self.servos[0].initialize_port()    # do port intialization just once because of daisy chain

    # =======================================
    # Public methods
    # =======================================

    # (analytical) forward kinematics with angles given in degrees
    def forwardkin_alpha2end(self, alpha, beta, gamma, delta):
        
        d0 = self.leg_data["d0"]
        a2 = self.leg_data["a2"]
        a3 = self.leg_data["a3"]
        
        alpha = np.radians(alpha)
        beta = np.pi/2 + np.radians(beta)
        gamma = np.pi/2 + np.radians(gamma)
        delta = np.radians(delta)

        pos = [0, 0, 0, 1]
        pos[0] = ( a3 * np.cos(delta) * ( np.cos(alpha) * np.cos(beta) * np.cos(gamma) + np.sin(alpha) * np.sin(gamma) ) ) + ( a3 * np.sin(delta) * ( -np.cos(alpha) * np.cos(beta) * np.sin(gamma) + np.sin(alpha) * np.cos(gamma) ) ) + ( a2 * ( np.cos(alpha) * np.cos(beta) * np.cos(gamma) + np.sin(alpha) * np.sin(gamma) ) )
        pos[1] = ( a3 * np.cos(delta) * ( np.sin(alpha) * np.cos(beta) * np.cos(gamma) - np.cos(alpha) * np.sin(gamma) ) ) + ( a3 * np.sin(delta) * ( -np.sin(alpha) * np.cos(beta) * np.sin(gamma) - np.cos(alpha) * np.cos(gamma) ) ) + ( a2 * ( np.sin(alpha) * np.cos(beta) * np.cos(gamma) - np.cos(alpha) * np.sin(gamma) ) )
        pos[2] = ( a3 * np.sin(beta) * np.cos(gamma) * np.cos(delta) ) - ( a3 * np.sin(beta) * np.sin(gamma) * np.sin(delta) ) + ( a2 * np.sin(beta) * np.cos(gamma) ) + d0
        return pos


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

    # Sets desired velocity of movement for all motors with individual value
    def set_speed_for_each(self, speed):
        for i in range(len(self.servos)):
            self.servos[i].write_velocity(speed[i])

    # Sets desired velocity of movement for all motors with same value
    def set_speed_for_all(self,speed):
        for i in range(len(self.servos)):
            self.servos[i].write_velocity(speed)

    # Gets a list of present positions from all motors
    def get_current_position(self):
        position = list()
        for i in self.servos:
            position.append(i.read_present_position())
        return position

    def get_current_degrees(self):
        pos_tick=self.get_current_position()
        pos_deg=list()
        for id,pos in enumerate (pos_tick):
            pos_deg.append(self.servos[id].tick_to_deg(pos))
        return pos_deg

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
                #if self.debug: print("position not reached!")
                return False
            else:
                if self.debug: print("position reached!")
                return True


    # Test is present position in degrees is in range deg +- offset for all servos
    def test_degrees(self,deg,offset):
        pos=list()
        offset_deg=self.servos[0].deg_to_tick(offset)
        for i in range(len(deg)):
            pos.append(self.servos[i].deg_to_tick(deg[i]))
        while leg.test_position(self,pos,offset_deg) is False:
            time.sleep(self.sampling)
        return True

    def test_servo_degree(self,servoID,deg,offset):
        while True:
            pos=self.get_servo_current_degree(servoID)
            if deg-offset<pos < deg+offset:
                return


    # Close communication with servos
    def end_communication(self):
        self.servos[0].close_port
        return