#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# Fachhochschule Bielefeld
# Ingenieurwissenschaften und Mathematik
# Ingenieurinformatik - Studienarbeit
# Michel Asmus, Marcel Bernauer
# ------------------------------------------------
# project: felix
# servo-class
# ------------------------------------------------

import os
import math
import logging
import sys

logger = logging.getLogger(__name__)
logger.debug('Logging in {0} started.'.format(__name__))

try:
    import dynamixel_functions as dynamixel
    logger.debug('Imported dynamixel_functions.')
except Exception as e:
    logger.critical("Importing dynamixel_functions failed!")
    logger.debug(e)


class servo:

    # =======================================
    # Public class attributes
    # =======================================

    #TODO: configure debug-structure (servo)

    #TODO: maybe build a dictionary?

    # Control table address
    ADDR_PRO_MAX_POSITION_LIMIT = 36
    ADDR_PRO_MIN_POSITION_LIMIT = 40
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

        #TODO: optimize initialization

        self.ID = DXL_ID
        self.BAUDRATE = BAUDRATE
        self.POS_MIN = POS_MIN
        self.POS_MAX = POS_MAX
        self.CLOCKWISE = CLOCKWISE
        self.DEVICENAME = DEVICENAME


    # =======================================
    # Public methods
    # =======================================

    # Establishes a connection to the motor and transmits motor-specific settings
    def initialize_port(self):
        try:
            servo.port_num = dynamixel.portHandler(self.DEVICENAME)
        except Exception as e:
            logger.critical('Working with dynamixel porthandler failed. Exiting...')
            logger.debug(e)
            quit()

        dynamixel.packetHandler()
        success_open_port = dynamixel.openPort(servo.port_num)

        if servo.debug:
            if success_open_port:
                logger.info("Succeeded to open the port!")
            else:
                logger.critical("Failed to open the port! Exiting...")
                quit()

        if success_open_port:
            success_set_baudrate = dynamixel.setBaudRate(servo.port_num, self.BAUDRATE)
            if servo.debug:
                if success_set_baudrate:
                    logger.info("Succeeded to change the baudrate!")
                else:
                    logger.critical("Failed to change the baudrate! Exiting...")
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
        if not self.CLOCKWISE:
            dxl_goal_position=dxl_goal_position*(-1)
        dynamixel.write4ByteTxRx(servo.port_num, servo.PROTOCOL_VERSION, self.ID, servo.ADDR_PRO_GOAL_POSITION,
                                 dxl_goal_position)
        dxl_comm_result = dynamixel.getLastTxRxResult(servo.port_num, servo.PROTOCOL_VERSION)
        dxl_error = dynamixel.getLastRxPacketError(servo.port_num, servo.PROTOCOL_VERSION)
        if servo.debug:
            if dxl_comm_result != servo.COMM_SUCCESS:
                print(dynamixel.getTxRxResult(servo.PROTOCOL_VERSION, dxl_comm_result))
            elif dxl_error != 0:
                print(dynamixel.getRxPacketError(servo.PROTOCOL_VERSION, dxl_error))
        if self.debug:
            if dxl_goal_position > self.POS_MAX or dxl_goal_position < self.POS_MIN:
                print("Goalposition of Servo ", self.ID, " out of range!")

    # Returns present position
    def read_present_position(self):
        dxl_present_position = dynamixel.read4ByteTxRx(servo.port_num, servo.PROTOCOL_VERSION, self.ID,
                                                       servo.ADDR_PRO_PRESENT_POSITION)

        dxl_comm_result = dynamixel.getLastTxRxResult(servo.port_num, servo.PROTOCOL_VERSION)
        dxl_error = dynamixel.getLastRxPacketError(servo.port_num, servo.PROTOCOL_VERSION)
        if dxl_comm_result == servo.COMM_SUCCESS:
            if not self.CLOCKWISE:
                dxl_present_position=dxl_present_position*(-1)
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

    # Sets maximum and minimum of possible position
    # Positions given in ticks
    def write_position_limits(self):
        #try to change maximum position
        dynamixel.write4ByteTxRx(servo.port_num, servo.PROTOCOL_VERSION, self.ID, servo.ADDR_PRO_MAX_POSITION_LIMIT, self.POS_MAX )
        dxl_comm_result = dynamixel.getLastTxRxResult(servo.port_num, servo.PROTOCOL_VERSION)
        dxl_error = dynamixel.getLastRxPacketError(servo.port_num, servo.PROTOCOL_VERSION)
        if servo.debug:
            if dxl_comm_result != servo.COMM_SUCCESS:
                print("successfully changed maximum position")
                print(dynamixel.getTxRxResult(servo.PROTOCOL_VERSION, dxl_comm_result))
            elif dxl_error != 0:
                print(dynamixel.getRxPacketError(servo.PROTOCOL_VERSION, dxl_error))
        # try to change minimum position
        dynamixel.write4ByteTxRx(servo.port_num, servo.PROTOCOL_VERSION, self.ID, servo.ADDR_PRO_MIN_POSITION_LIMIT, self.POS_MIN)
        dxl_comm_result = dynamixel.getLastTxRxResult(servo.port_num, servo.PROTOCOL_VERSION)
        dxl_error = dynamixel.getLastRxPacketError(servo.port_num, servo.PROTOCOL_VERSION)
        if servo.debug:
            if dxl_comm_result != servo.COMM_SUCCESS:
                print("successfully changed minimum position")
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