#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# Fachhochschule Bielefeld
# Ingenieurwissenschaften und Mathematik
# Ingenieurinformatik - Studienarbeit
# Michel Asmus, Marcel Bernauer, Phil Petschull
# ------------------------------------------------
# project: felix
# main
# ------------------------------------------------
# TODO:
# a) start-menu for choosing COM-port

from leg import leg
from dict_servo import servo_all

DEVICENAME = "COM4".encode('utf-8')

# Wake up...
felix = leg(servo_all,DEVICENAME)
felix.enable_torque()
input("Will disable torque")
felix.disable_torque()
felix.end_communication()