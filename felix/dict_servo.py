#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# Fachhochschule Bielefeld
# Ingenieurwissenschaften und Mathematik
# Ingenieurinformatik - Studienarbeit
# Michel Asmus, Marcel Bernauer, Phil Petschull
# ------------------------------------------------
# project: felix
# servo-specific settings
# ------------------------------------------------
# TODO:
# a) position-max and -min still in ticks


servo1={
    "ID"                : 1,
    "BAUDRATE"          : 1000000,
    "POSITION_MINIMUM"  : -76000,
    "POSITION_MAXIMUM"  : 76000,
    "CLOCKWISE"         : 1,
    "SPEED_MAXIMUM"     : 10000,
    "DH_Theta"          : 0,
    "DH_d"              : 0,
    "DH_a"              : 0,
    "DH_Alpha"          : 0
}

servo2={
    "ID"                : 2,
    "BAUDRATE"          : 1000000,
    "POSITION_MINIMUM"  : -76000,
    "POSITION_MAXIMUM"  : 76000,
    "CLOCKWISE"         : 1,
    "SPEED_MAXIMUM"     : 10000,
    "DH_Theta"          : 0,
    "DH_d"              : 0,
    "DH_a"              : 0,
    "DH_Alpha"          : 0
}

servo3={
    "ID"                : 3,
    "BAUDRATE"          : 1000000,
    "POSITION_MINIMUM"  : -45000,
    "POSITION_MAXIMUM"  : 76000,
    "CLOCKWISE"         : 1,
    "SPEED_MAXIMUM"     : 10000,
    "DH_Theta": 0,
    "DH_d": 0,
    "DH_a": 0,
    "DH_Alpha": 0
}

servo4={
    "ID"                : 4,
    "BAUDRATE"          : 1000000,
    "POSITION_MINIMUM"  : -76000,
    "POSITION_MAXIMUM"  : 76000,
    "CLOCKWISE"         : 1,
    "SPEED_MAXIMUM"     : 10000,
    "DH_Theta": 0,
    "DH_d": 0,
    "DH_a": 0,
    "DH_Alpha": 0
}

servo_all=[servo1,servo2,servo3,servo4]
