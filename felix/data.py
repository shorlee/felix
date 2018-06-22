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


import numpy as np

robot_data = [
    {   "legs" :
            [{  "id"    :   1,

                # dimensions
                "d0"   :   115,
                "a2"   :   300,
                "a3"   :   250,

                #TODO: base system transformation
                "T_base"    : np.array([  # Translation um x = +0.0325 und y = -0.0325  ??
                    [ 1,  0,  0, -0.0325],
                    [ 0,  1,  0,  0.0325],
                    [ 0,  0,  1,  0],
                    [ 0,  0,  0,  1]]),

                # positions
                "current_pos"   :   [0, 0, 0, 0],
                "next_pos"      :   [0, 0, 0, 0],
                
                # components
                "servos" :
                    [{  "ID"                : 1,
                        "BAUDRATE"          : 1000000,
                        "POSITION_MINIMUM"  : -76000,
                        "POSITION_MAXIMUM"  : 76000,
                        "CLOCKWISE"         : True,    # positive
                        "SPEED_MAXIMUM"     : 10000     },

                    {   "ID"                : 2,
                        "BAUDRATE"          : 1000000,
                        "POSITION_MINIMUM"  : -76000,
                        "POSITION_MAXIMUM"  : 76000,
                        "CLOCKWISE"         : True,     # positive
                        "SPEED_MAXIMUM"     : 10000     },

                    {   "ID"                : 3,
                        "BAUDRATE"          : 1000000,
                        "POSITION_MINIMUM"  : -45000,
                        "POSITION_MAXIMUM"  : 76000,
                        "CLOCKWISE"         : True,    # negative
                        "SPEED_MAXIMUM"     : 10000     },

                    {   "ID"                : 4,
                        "BAUDRATE"          : 1000000,
                        "POSITION_MINIMUM"  : -76000,
                        "POSITION_MAXIMUM"  : 76000,
                        "CLOCKWISE"         : True,     # negative
                        "SPEED_MAXIMUM"     : 10000     }]
            }]
        }]
