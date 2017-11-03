#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# Fachhochschule Bielefeld
# Ingenieurwissenschaften und Mathematik
# Ingenieurinformatik - Studienarbeit
# Michel Asmus, Marcel Bernauer, Phil Petschull
# ------------------------------------------------
# project: felix
# servo-class
# ------------------------------------------------

import os
import math

try:
    import dynamixel_functions as dynamixel
except Exception as e:
    print("Error: Importing dynamixel_functions failed!")
    print(e)


class servo:

    # =======================================
    # Public class attributes
    # =======================================

    # Control table address
    ADDR_PRO_TORQUE_ENABLE = 562
    ADDR_PRO_GOAL_POSITION = 596
    ADDR_PRO_GOAL_TORQUE = 604
    ADDR_PRO_GOAL_VELOCITY = 600
    ADDR_PRO_PRESENT_POSITION = 611
    ADDR_PRO_PRESENT_VELOCITY = 615
    ADDR_PRO_PRESENT_CURRENT = 621

    # Movement values
    TORQUE_ENABLE = 1
    TORQUE_DISABLE = 0
    DXL_MOVING_STATUS_THRESHOLD = 20

    # Protocol version
    PROTOCOL_VERSION = 2

    # Communication values
    COMM_SUCCESS = 0
    COMM_TX_FAIL = -1001
    port_num = -1  # Port-No. will be set in 'initialize_port'

    # For Dynamixel H42-20-S300-R
    ticks_per_turn = 303750
    ticks_per_half_turn= ticks_per_turn/2

    # Set True to get debug-info
    debug = True

    # =======================================
    # Private methods
    # =======================================

    # Constructor saves motor-specific settings
    def __init__(self, DXL_ID, BAUDRATE, POS_MIN, POS_MAX, CLOCKWISE, DEVICENAME):
        self.ID = DXL_ID
        self.BAUDRATE = BAUDRATE
        self.POS_MIN = POS_MIN
        self.POS_MAX = POS_MAX
        self.CLOCKWISE = CLOCKWISE
        self.DEVICENAME = DEVICENAME

        # maybe initalize_port() ??


    # =======================================
    # Public methods
    # =======================================

    # Establishes a connection to the motor and transmits motor-specific settings
    def initialize_port(self):

        servo.port_num = dynamixel.portHandler(self.DEVICENAME)
        dynamixel.packetHandler()
        success_open_port = dynamixel.openPort(servo.port_num)

        if servo.debug:
            if success_open_port:
                print("Succeeded to open the port!")
            else:
                print("Failed to open the port!")
                input("Press any key to terminate...")
                quit()

        if success_open_port:
            success_set_baudrate = dynamixel.setBaudRate(servo.port_num, self.BAUDRATE)
            if servo.debug:
                if success_set_baudrate:
                    print("Succeeded to change the baudrate!")
                else:
                    print("Failed to change the baudrate!")
                    input("Press any key to terminate...")
                    quit()


    # Close communication with USB-to-Dynamixel
    def close_port(self):
        dynamixel.closePort(servo.port_num)

    # Activates power consumption for halting position
    def enable_torque(self):
        dynamixel.write1ByteTxRx(servo.port_num, servo.PROTOCOL_VERSION, self.ID, servo.ADDR_PRO_TORQUE_ENABLE,
                                 self.TORQUE_ENABLE)
        dxl_comm_result = dynamixel.getLastTxRxResult(servo.port_num, servo.PROTOCOL_VERSION)
        dxl_error = dynamixel.getLastRxPacketError(servo.port_num, servo.PROTOCOL_VERSION)
        if servo.debug:
            if dxl_comm_result != servo.COMM_SUCCESS:
                print(dynamixel.getTxRxResult(servo.PROTOCOL_VERSION, dxl_comm_result))
            elif dxl_error != 0:
                print(dynamixel.getRxPacketError(servo.PROTOCOL_VERSION, dxl_error))

    # Deactivates power consumption for manual operation
    def disable_torque(self):
        dynamixel.write1ByteTxRx(servo.port_num, servo.PROTOCOL_VERSION, self.ID, servo.ADDR_PRO_TORQUE_ENABLE,
                                 servo.TORQUE_DISABLE)
        dxl_comm_result = dynamixel.getLastTxRxResult(servo.port_num, servo.PROTOCOL_VERSION)
        dxl_error = dynamixel.getLastRxPacketError(servo.port_num, servo.PROTOCOL_VERSION)
        if servo.debug:
            if dxl_comm_result != servo.COMM_SUCCESS:
                print(dynamixel.getTxRxResult(servo.PROTOCOL_VERSION, dxl_comm_result))
            elif dxl_error != 0:
                print(dynamixel.getRxPacketError(servo.PROTOCOL_VERSION, dxl_error))

    # Moves to target position
    def write_position(self, dxl_goal_position):
        if dxl_goal_position <= self.POS_MAX and dxl_goal_position >= self.POS_MIN:
            dynamixel.write4ByteTxRx(servo.port_num, servo.PROTOCOL_VERSION, self.ID, servo.ADDR_PRO_GOAL_POSITION,
                                     dxl_goal_position)
            dxl_comm_result = dynamixel.getLastTxRxResult(servo.port_num, servo.PROTOCOL_VERSION)
            dxl_error = dynamixel.getLastRxPacketError(servo.port_num, servo.PROTOCOL_VERSION)
            if servo.debug:
                if dxl_comm_result != servo.COMM_SUCCESS:
                    print(dynamixel.getTxRxResult(servo.PROTOCOL_VERSION, dxl_comm_result))
                elif dxl_error != 0:
                    print(dynamixel.getRxPacketError(servo.PROTOCOL_VERSION, dxl_error))
        elif servo.debug:
            print("Goalposition of Servo ", self.ID, " out of range!")

    # Returns present position
    def read_present_position(self):
        dxl_present_position = dynamixel.read4ByteTxRx(servo.port_num, servo.PROTOCOL_VERSION, self.ID,
                                                       servo.ADDR_PRO_PRESENT_POSITION)
        dxl_comm_result = dynamixel.getLastTxRxResult(servo.port_num, servo.PROTOCOL_VERSION)
        dxl_error = dynamixel.getLastRxPacketError(servo.port_num, servo.PROTOCOL_VERSION)
        if dxl_comm_result == servo.COMM_SUCCESS:
            return dxl_present_position
        else:
            if servo.debug:
                if dxl_comm_result != servo.COMM_SUCCESS:
                    print(dynamixel.getTxRxResult(servo.PROTOCOL_VERSION, dxl_comm_result))
                elif dxl_error != 0:
                    print(dynamixel.getRxPacketError(servo.PROTOCOL_VERSION, dxl_error))
            return servo.read_present_position(self)


    # Sets desired velocity of movement
    def write_velocity(self, dxl_goal_velocity):
        dynamixel.write4ByteTxRx(servo.port_num, servo.PROTOCOL_VERSION, self.ID, servo.ADDR_PRO_GOAL_VELOCITY,
                                 dxl_goal_velocity)
        dxl_comm_result = dynamixel.getLastTxRxResult(servo.port_num, servo.PROTOCOL_VERSION)
        dxl_error = dynamixel.getLastRxPacketError(servo.port_num, servo.PROTOCOL_VERSION)
        if servo.debug:
            if dxl_comm_result != servo.COMM_SUCCESS:
                print(dynamixel.getTxRxResult(servo.PROTOCOL_VERSION, dxl_comm_result))
            elif dxl_error != 0:
                print(dynamixel.getRxPacketError(servo.PROTOCOL_VERSION, dxl_error))

    # Convert ticks into degrees
    def tick_to_deg(self, tick):
        deg = tick*(180/(self.ticks_per_turn/2))
        return deg

    # Convert degrees into ticks
    def deg_to_tick(self, deg):
        tick = int(float(deg)*(151875/180))
        return tick