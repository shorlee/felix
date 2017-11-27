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

#number of legs
NUMBER_OF_LEGS     =   1
#number of servos
NUMBER_OF_SERVOS   =   4 



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
                        "CLOCKWISE"         : 1,     
                        "SPEED_MAXIMUM"     : 10000     },

                    {   "ID"                : 2,
                        "BAUDRATE"          : 1000000,
                        "POSITION_MINIMUM"  : -76000,
                        "POSITION_MAXIMUM"  : 76000,
                        "CLOCKWISE"         : 1,  
                        "SPEED_MAXIMUM"     : 10000     },

                    {   "ID"                : 3,
                        "BAUDRATE"          : 1000000,
                        "POSITION_MINIMUM"  : -45000,
                        "POSITION_MAXIMUM"  : 76000,
                        "CLOCKWISE"         : 1,         
                        "SPEED_MAXIMUM"     : 10000     },

                    {   "ID"                : 4,
                        "BAUDRATE"          : 1000000,
                        "POSITION_MINIMUM"  : -76000,
                        "POSITION_MAXIMUM"  : 76000,
                        "CLOCKWISE"         : 1,
                        "SPEED_MAXIMUM"     : 10000     }]
            }]
}]
                  

#Print all the leg-data                    
def print_robot_data(robot_data):
    for i in range(0,NUMBER_OF_LEGS):
        #print leg-information
        print("Leg","",i+1,"Information:\n")
        
        #print id
        print("ID: ",robot_data[i]["legs"][i]["id"],"\n")
        
        #print all three dimensions
        print("Dimensions:")
        print("do: ",robot_data[i]["legs"][i]["d0"])
        print("a2: ",robot_data[i]["legs"][i]["a2"])
        print("a3: ",robot_data[i]["legs"][i]["a3"],"\n")
        
        #print base system transformation
        print("Base System Transformation:\n")
        print(robot_data[i]["legs"][i]["T_base"],"\n")
        
        #print positions
        print("Positions:\n")
        print("Current Position:")
        print(robot_data[i]["legs"][i]["current_pos"],"\n")
        print("Next Position:")
        print(robot_data[i]["legs"][i]["next_pos"],"\n")
        
        #print all the components
        for u in range(0,NUMBER_OF_SERVOS):
            print("Servo:           ",u+1)
            print("ID:              ",robot_data[i]["legs"][i]["servos"][u]["ID"])
            print("POSITION_MINIMUM:",robot_data[i]["legs"][i]["servos"][u]["POSITION_MINIMUM"])
            print("POSITION_MAXIMUM:",robot_data[i]["legs"][i]["servos"][u]["POSITION_MAXIMUM"])
            print("CLOCKWISE:       ",robot_data[i]["legs"][i]["servos"][u]["CLOCKWISE"])
            print("SPEED_MAXIMUM:   ",robot_data[i]["legs"][i]["servos"][u]["SPEED_MAXIMUM"],"\n")
            
        
        

#function call
print_robot_data(robot_data)        
        
        
     
    
    
    
    
    
                    
                    