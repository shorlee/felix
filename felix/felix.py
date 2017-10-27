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

DEVICENAME = "COM7".encode('utf-8')

# Wake up...
felix = leg(servo_all,DEVICENAME)