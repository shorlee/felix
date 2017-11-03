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

servo_data=[
{"ID"                : 1,
    "BAUDRATE"          : 1000000,
    "POSITION_MINIMUM"  : -76000,
    "POSITION_MAXIMUM"  : 76000,
    "CLOCKWISE"         : 1
}
,
{
    "ID"                : 2,
    "BAUDRATE"          : 1000000,
    "POSITION_MINIMUM"  : -76000,
    "POSITION_MAXIMUM"  : 76000,
    "CLOCKWISE"         : 1
}
,
{
    "ID"                : 3,
    "BAUDRATE"          : 1000000,
    "POSITION_MINIMUM"  : -45000,
    "POSITION_MAXIMUM"  : 76000,
    "CLOCKWISE"         : 1
}
,
{
    "ID"                : 4,
    "BAUDRATE"          : 1000000,
    "POSITION_MINIMUM"  : -76000,
    "POSITION_MAXIMUM"  : 76000,
    "CLOCKWISE"         : 1,
    "SPEED_MAXIMUM"     : 10000
}
]

