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

try:
    from leg import leg
except Exception as e:
    print("Error: Importing leg failed!")
    print(e)

from dict_servo import servo_all

import serial.tools.list_ports

DEVICENAME = "COM4".encode('utf-8')

# get a list of available COM-ports on a win-system
def get_comports():
    return serial.tools.list_ports.comports()

# interactive choice of COM-port
def set_comport():
    print("Determining COM-Ports...")
    ports = list(get_comports())

    if len(ports) == 1:
        print("Found 1 COM-Port:", ports[0])
        device = str(ports[0]).split()[0]

    elif len(ports) == 0:
        print("Found 0 COM-Ports :(")
        device = -1

    else:
        print("Found ", len(ports), " COM-Ports.")
        for index, port in enumerate(ports):
            print(index, port)
        device = str(ports[int(input("Please choose by typing in the desired index of the port:"))]).split()[0]

    print("Have fun with", device, "!")
    return device


# options
def menu():

    while True:

        print("Options:")
        print("0: Exit programm")
        print("1: Set your COM-port")
        print("2: Wake up FELIX")
        print("3: Toggle torque-activation")
        print("4: Read present position in degrees")
        print("5: Move to default position")
        print("6: Execute dummy trajectory given in test_felix.py")
        print("7: Move one servo to position given in degrees")
        print("8: Move all servos to destination given in degrees")
        choice = int(input("Please choose: "))
        print("Your choice is ", choice)

        if choice == 0:
            print("Exiting...")
            try:
                felix.end_communication()
                break
            except:
                break

        elif choice == 1:
            print("")
            DEVICENAME = str(set_comport()).encode('utf-8')
            
        elif choice == 2:
            felix = leg(servo_all, DEVICENAME)

        elif choice == 3:
            #felix.enable_torque()
            #
            pass

        elif choice == 4:
            pass

        elif choice == 5:
            pass

        elif choice == 6:
            pass

        elif choice == 7:
            pass

        elif choice == 8:
            pass

        else:
            print("Unknown input. Please try again.")




# main
def main():

    menu()
    
    return
    

# jump to main
if __name__ == '__main__':
    main()