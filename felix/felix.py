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
    import test_felix
except Exception as e:
    print("Error: Importing test_felix failed!")
    print(e)

from data import robot_data         # servo constants
import serial.tools.list_ports      # available COM-ports
import numpy as np
import copy




class robot():

    # =======================================
    # Public class attributes
    # =======================================
    
    #TODO: configure debug-structure (robot)

    OUTPUTFILE = "Output.txt"

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
        self.leg = leg(robot_data[0]["legs"][0], DEVICENAME)    # here its just robot 0 and its leg 0


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


    # get a list of available COM-ports on a win-system and macosx
    def get_comports(self):
        return serial.tools.list_ports.comports()


    # interactive choice of COM-port (win and macosx tested!)
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

    # save angles and position into an .txt file
    def write_angles_position(self,angles, position):
        try:
            file = open(self.OUTPUTFILE, "a")
        except Exception as e:
            print("Error: Could not open file!")
            print(e)
            return()
        text = ""
        for angle in angles:
            text = text + str("%.2f " % angle)
        for comp in range(len(position)-1):
            text = text + str("%.2f " % position[comp])
        text = text + "\n"
        file.write(text)
        file.close()

    # read angles and positions from txt. file
    def read_angles_position_from_file(self):
        try:
            file = open(self.OUTPUTFILE, "r")
        except Exception as e:
            print("Error: Could not open file!")
            print(e)
            return()
        text=file.readlines()
        combined = list()
        for line in text:
            elements=line.split()
            angles=list()
            position=list()
            for angle in range(0,4):
                angles.append(elements[angle])
            for pos in range(4,7):
                position.append(elements[pos])
            combined.append([angles,position])
        return (combined)

    # print list of angles and positions

    def print_angles_positions(self,list):
        for index, element in enumerate(list):
            print("point:",index)
            print("angles:")
            for join, angle in enumerate(element[0]):
                print(join,":",angle)
            print("X:",element[1][0])
            print("Y:", element[1][1])
            print("Z:", element[1][2],"\n")


    # =======================================
    # Public methods
    # =======================================
        
    #print robot_data     
    def print_robot_data(self):
        for robot in robot_data:
            #print list of legs
            print("\n")
            print("Leg-Information:")
            print("------------------------------------")
            for leg in robot["legs"]:
                for item in leg:
                    if item is "T_base":
                        print("\n")
                        print("T_base:")
                        print("\n")
                        for tbase in leg[item]:
                            for column in tbase:
                                print('{:10}'.format(column), end=' ')   
                            print("\n")
                    elif item is "servos":
                        print("\n")
                        print("Servos")
                        print("------------------------------------")
                        print("\n")
                        for servo in leg[item]:
                            for key,value in servo.items():
                                print('{:26} : {}'.format(key,value))
                            print("\n")  
                    else:
                        print("\n")
                        print('{:26} : {}'.format(item,leg[item]))
                  
                print("------------------------------------")        

    # options
    def menu(self):

        print("\nWelcome to FELIX - Feedback Error Learning with dynamIXel!")

        options = {
            'e' : "[e]xit programm",
            'i' : "[i]nformation about the robot (data.py)",
            't' : "[t]oggle torque-activation",
            's' : "set movement [s]peed for all servos",
            'r' : "[r]ead present position",
            'p' : "[p]rint saved list of angles and positions",
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


            # [e]xit programm
            if choice == 'e':
                break


            # [i]nformation about the robot (data.py)
            elif choice == 'i':
                self.print_robot_data()
                #for key, value in self.leg.leg_data.items():
                    #print(key,)
                #self.print_data() (only for self.leg !)


            # [t]oggle torque-activation
            elif choice == 't':
                self.toggle_torque()


            # set movement [s]peed for all servos
            elif choice == 's':
                self.leg.set_speed_for_all(int(input("Please input speed:")))       # ?! whats this?
                pass
                #self.leg.set_speed(input("Please input speed (default: 1000):"))


            # [r]ead present position
            elif choice == 'r':
                # -- angles
                angles = self.leg.get_current_degrees()
                for servo_id, servo_pos in enumerate(angles):
                    print("> servo", servo_id, "is at %7.3f degree." % servo_pos)
                # -- xyz
                position = self.leg.forwardkin_alpha2end(*angles)
                print("> leg is at XYZ (alpha2end):", position)
                # -- save
                saving = input("> save angles and position? (y/n)")
                if saving == 'y':
                    self.write_angles_position(angles,position)
                    print("angles and position saved")


            # [p]rint saved list of angles and positions
            elif choice == 'p':
                self.print_angles_positions(self.read_angles_position_from_file())


            # move to [d]efault position
            elif choice == 'd':
                if self.leg.torque:
                    offset = 0.005
                    pos = [0, 0, 90, 90]
                    for id, pos in enumerate(pos):
                        print("will move servo", id, "to default position")
                        self.leg.move_servo_to_degrees(id, pos)
                        self.leg.test_servo_degree(id, pos, offset)
                else: print("Please enable torque first!")

            
            # e[x]ecute dummy trajectory given in test_felix.py
            elif choice == 'x':
                if self.leg.torque:
                    test_felix.run_trajectory(self.leg)
                else:
                    print("Please enable torque first!")


            # move [o]ne servo to position given in degrees
            elif choice == 'o':
                self.leg.move_servo_to_degrees(int(input("Please input servo-id:")), float(input("Please input position:")))


            # move [a]ll servos to destination given in degrees
            elif choice == 'a':
                if self.leg.torque:
                    pos=list()
                    for i in range(self.leg.num_servo):
                        pos.append(input("Please input position for servo {}: ".format(i)))
                    self.leg.move_to_deg(pos)
                else: print("Please enable torque first!")
                #self.leg.move_to_deg([int(x) for x in input("Please input position (default: 0 0 90 90):").split()])


            # else
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

