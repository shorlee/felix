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

from dict_servo import servo_all    # servo constants
import serial.tools.list_ports      # available COM-ports


# get a list of available COM-ports on a win-system
def get_comports():
    return serial.tools.list_ports.comports()

# interactive choice of COM-port
def set_comport():
    while True:
        print("Determining COM-Ports...")
        ports = list(get_comports())
    
        if not len(ports):
            print("Found 0 COM-Ports :(\n")
            if len(input("Enter anything to exit or hit enter to try again...")):
                return False

        elif len(ports) == 1:
            print("Found 1 COM-Port:", ports[0])
            return str(ports[0]).split()[0]

        else:
            print("Found ", len(ports), " COM-Ports.")
            for index, port in enumerate(ports):
                print(index, port)
            return str(ports[int(input("Please choose by typing in the desired index of the port:"))]).split()[0]



# options
def menu(felix):

    print("\nWelcome to FELIX - Feedback Error Learning with dynamIXel!")

    while True:
        print("\n--------------------------------------------")
        print("Options:")
        print("0: Exit programm")
        print("1: Toggle torque-activation")
        print("2: Read present position in degrees")
        print("3: Move to default position")
        print("4: Execute dummy trajectory given in test_felix.py")
        print("5: Move one servo to position given in degrees")
        print("6: Move all servos to destination given in degrees")
        print("--------------------------------------------")
        
        choice = ""
        while True:
            try:
                choice = int(input("Please choose: "))
                break
            except:
                choice = ""

        print("Your choice is", choice)

        # exit
        if choice == 0:
            print("Exiting...")
            break

        # toggle torque
        elif choice == 1:
            #if not felix.active_torque:
            #    felix.enable_torque()
            #    print("Torque is now enabled.")
            #else:
            #    felix.disable_torque()
            #    print("Torque is now disabled.")
            pass

        # read position in degrees
        elif choice == 2:
            pass

        elif choice == 3:
            pass

        elif choice == 4:
            pass

        elif choice == 5:
            pass

        elif choice == 6:
            pass

        else:
            print("Option is not available. Please try again.")




# main
def main():

    print("Starting FELIX...")

    # determine COM-port...
    DEVICENAME = set_comport()
    if DEVICENAME:
        print("Working with", DEVICENAME)
        DEVICENAME = str(DEVICENAME).encode('utf-8')
    else:
        print("Aborted port-detection. Exiting...")
        return

    # Wake up...
    felix = leg(servo_all, DEVICENAME)

    # UI
    menu(felix)
    
    # go to sleep
    felix.end_communication()

    return
    

# jump to main
if __name__ == '__main__':
    main()