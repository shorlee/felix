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

try:
    from test_felix import run_trajectory
except Exception as e:
    print("Error: Importing run_trajectory failed!")
    print(e)

from data import robot_data         # servo constants
import serial.tools.list_ports      # available COM-ports


class robot():

    # =======================================
    # Public class attributes
    # =======================================
    
    # =======================================
    # Private methods
    # =======================================

    # Constructor
    def __init__(self):
        print("constructing...")

        # determine COM-port...
        DEVICENAME = self.set_comport()
        if DEVICENAME:
            print("Working with", DEVICENAME)
            DEVICENAME = str(DEVICENAME).encode('utf-8')
        else:
            print("Aborted port-detection. Exiting...")
            return

        # Wake up...
        self.leg = leg(robot_data[0]["legs"][0], DEVICENAME)    # here just robot 0 and its leg 0


    # Destructor
    def __del__(self):

        # safely turn off torque if necessary
        if self.leg.torque:
            input("Please watch out, hit enter to disable torque...")
            self.leg.disable_torque()

        print("destructing...")

        # safe exit
        self.leg.end_communication()


    # give away the leg
    def get_leg(self):
        return self.leg


    # get a list of available COM-ports on a win-system
    def get_comports(self):
        return serial.tools.list_ports.comports()


    # interactive choice of COM-port
    def set_comport(self):
        while True:
            print("Determining COM-Ports...")
            ports = list(self.get_comports())   # element is like: "COM # - USB Serial Port (COM#)"
    
            if not len(ports):
                print("Found 0 COM-Ports :(\n")
                if len(input("Enter anything to exit or hit enter to look for again...")):
                    return False

            elif len(ports) == 1:
                print("Found 1 COM-Port:", ports[0])    # take the only one
                return str(ports[0]).split()[0]

            else:
                print("Found ", len(ports), " COM-Ports.")  # choose it by typing in the index of the port shown
                for index, port in enumerate(ports):
                    print(index, port)
                return str(ports[int(input("Please choose by typing in the desired index of the port:"))]).split()[0]


    # automatically enable/disable torque
    def toggle_torque(self):
        if not self.leg.torque:
            self.leg.enable_torque()
            print("Torque enabled.")
        else:
            self.leg.disable_torque()
            print("Torque disabled.")


    # =======================================
    # Public methods
    # =======================================

    # options
    def menu(self):

        print("\nWelcome to FELIX - Feedback Error Learning with dynamIXel!")

        options = {
            'e' : "[e]xit programm",
            'i' : "[i]nformation about the robot (data.py)",
            't' : "[t]oggle torque-activation",
            's' : "set movement [s]peed for all servos",
            'r' : "[r]ead present position in degrees",
            'd' : "move to [d]efault position",
            'x' : "e[x]ecute dummy trajectory given in test_felix.py",
            'o' : "move [o]ne servo to position given in degrees",
            'a' : "move [a]ll servos to destination given in degrees"
            }

        while True:
            print("\n--------------------------------------------")
            print("Your Options:")
            for option in options.values():
                print(option)
            print("--------------------------------------------")

            choice = input("Please choose: ")   # user input


            # input processing
            if choice == 'e':
                break

            elif choice == 'i':
                for key, value in self.leg.leg_data.items():
                    print(key, " = ", value)

            elif choice == 't':
                self.toggle_torque()

            elif choice == 's':
                self.leg.set_speed_for_all(int(input("Please input speed:")))
                pass
                #self.leg.set_speed(input("Please input speed (default: 1000):"))

            elif choice == 'r':
                for servo_id, servo_pos in enumerate(self.leg.get_current_degrees()):
                    print("> servo", servo_id, "is at %7.3f degree." % servo_pos)

            elif choice == 'd':
                if self.leg.torque:
                    offset = 0.005
                    pos = [0, 0, 90, 90]
                    for id, pos in enumerate(pos):
                        print("will move servo", id, "to default position")
                        self.leg.move_servo_to_degrees(id, pos)
                        self.leg.test_servo_degree(id, pos, offset)
                else: print("Please enable torque first!")

            elif choice == 'x':
                if self.leg.torque:
                    run_trajectory(self.leg)
                else:
                    print("Please enable torque first!")

            elif choice == 'o':
                self.leg.move_servo_to_degrees(int(input("Please input servo-id:")), float(input("Please input position:")))

            elif choice == 'a':
                if self.leg.torque:
                    pos=list()
                    for i in range(self.leg.num_servo):
                        pos.append(input("Please input position for servo {}: ".format(i)))
                    self.leg.move_to_deg(pos)
                else: print("Please enable torque first!")
                #self.leg.move_to_deg([int(x) for x in input("Please input position (default: 0 0 90 90):").split()])

            else:
                print("Invalid input... Please try again")


# main
def main():

    print("Starting FELIX...")

    # Wake up...
    felix = robot()

    # UI
    felix.menu()

    

# jump to main
if __name__ == '__main__':
    main()