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
# edited: 2017-10-19 16:00 (marcel)
# ------------------------------------------------
# TODO:
# a)

from leg import leg
from dict_servo import servo_all

DEVICENAME = "COM3".encode('utf-8')

# Wake up...
felix = leg(servo_all,DEVICENAME)
felix.enable_torque()
input("Will diable torque")
felix.disable_torque()
felix.end_communication()