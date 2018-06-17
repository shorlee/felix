#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# Fachhochschule Bielefeld
# Ingenieurwissenschaften und Mathematik
# Ingenieurinformatik - Studienarbeit
# Michel Asmus, Marcel Bernauer
# ------------------------------------------------
# project: felix
# main
# ------------------------------------------------

#>> argument parser
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--debug', help='display specific debugging information', action='store_true')
parser.add_argument('--verbose', help='increase output verbosity', action='store_true')
parser.add_argument('--virtual', help='virtual COM-port for simulation mode', action='store_true')
args = parser.parse_args()

#>> logging
import logging

if args.debug:
    logging.basicConfig(datefmt='%H:%M:%S', format='%(asctime)s.%(msecs)03d - %(levelname)8s - %(filename)14s - %(message)s', level=logging.DEBUG)
else:
    logging.basicConfig(datefmt='%H:%M:%S', format='%(asctime)s.%(msecs)03d - %(levelname)8s - %(filename)14s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)
logger.debug('Logging in {0} started.'.format(__name__))

#>> official libraries
try:
    import serial.tools.list_ports      # used for getting available COM-ports
    logger.debug('Imported pyserial.')
except Exception as e:
    logger.critical('Importing pyserial failed!')
    logger.debug(e)

try:
    import numpy as np
    logger.debug('Imported numpy.')
except Exception as e:
    logger.critical('Importing numpy failed!')
    logger.debug(e)

#>> local libraries
try:
    from data import robot_data         # servo constants
    logger.debug('Imported robot_data.')
except Exception as e:
    logger.critical('Importing robot_data failed!')
    logger.debug(e)

try:
    from leg import leg
    logger.debug('Imported leg.')
except Exception as e:
    logger.critical('Importing leg failed!')
    logger.debug(e)

try:
    import test_felix
    logger.debug('Imported test_felix.')
except Exception as e:
    logger.critical('Importing test_felix failed!')
    logger.debug(e)


#>> main class
class robot():

    # =======================================
    # Public class attributes
    # =======================================
    
    OUTPUTFILE = 'Output.txt'

    # =======================================
    # Private methods
    # =======================================

    # Constructor
    def __init__(self):
        logger.debug('constructing...')

        if args.virtual:
            logger.info('Using virtual COM-port. Entering simulation mode...')
            DEVICENAME = False
        else:
            # determine COM-port...
            DEVICENAME = self.set_comport()
            if DEVICENAME:
                logger.info('Working with {}'.format(DEVICENAME))
                DEVICENAME = str(DEVICENAME).encode('utf-8')
            else:
                logger.critical('Aborted port-detection. Exiting...')
                quit()

        # Wake up...
        self.leg = leg(robot_data[0]['legs'][0], DEVICENAME)    # here its just robot 0 and its leg 0


    # Destructor
    def __del__(self):

        logger.debug('destructing...')

        # safely turn off torque if necessary
        if hasattr(self, 'leg'):
            if self.leg.torque:
                input('Please watch out, hit enter to disable torque...')
                self.leg.disable_torque()

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
            logger.info('Determining COM-Ports...')
            ports = list(self.get_comports())   # element is like: 'COM # - USB Serial Port (COM#)'
    
            if not len(ports):
                logger.critical('Found 0 COM-Ports :( (Maybe you want to run it with --virtual ?)')
                #if len(input('Enter anything to exit or hit enter to look for again...')):
                return False

            elif len(ports) == 1:
                logger.info('Found 1 COM-Port: {0}'.format(ports[0]))    # take the only one
                return str(ports[0]).split()[0]

            else:
                logger.error('Found {0} COM-Ports.'.format(len(ports)))  # choose it by typing in the index of the port shown
                for index, port in enumerate(ports):
                    print(index, port)
                return str(ports[int(input('Please choose by typing in the desired index of the port:'))]).split()[0]


    # automatically enable/disable torque
    def toggle_torque(self):
        if not self.leg.torque:
            self.leg.enable_torque()
            logger.info('Torque enabled.')
        else:
            self.leg.disable_torque()
            logger.info('Torque disabled.')

    # save angles and position into an .txt file
    def write_angles_position(self,angles, position):
        try:
            file = open(self.OUTPUTFILE, 'a')
        except Exception as e:
            logger.error("Could not open file '{0}'.".format(self.OUTPUTFILE))
            logger.debug(e)
            return ()
        text = ''
        for angle in angles:
            text = text + str('%.2f ' % angle)
        for comp in range(len(position)-1):
            text = text + str('%.2f ' % position[comp])
        text = text + '\n'
        file.write(text)
        file.close()

    # read angles and positions from txt. file
    def read_angles_position_from_file(self):
        try:
            file = open(self.OUTPUTFILE, 'r')
        except Exception as e:
            logger.error("Could not open file '{0}'.".format(self.OUTPUTFILE))
            logger.debug(e)
            return ()
        text = file.readlines()
        combined = list()
        for line in text:
            elements = line.split()
            angles = list()
            position = list()
            for angle in range(0,4):
                angles.append(elements[angle])
            for pos in range(4,7):
                position.append(elements[pos])
            combined.append([angles,position])
        return (combined)

    # print list of angles and positions

    def print_angles_positions(self,list):
        for index, element in enumerate(list):
            print('point:',index)
            print('angles:')
            for join, angle in enumerate(element[0]):
                print(join,':',angle)
            print('X:',element[1][0])
            print('Y:', element[1][1])
            print('Z:', element[1][2],'\n')


    # =======================================
    # Public methods
    # =======================================
        
    #print robot_data     
    def print_robot_data(self):
        for robot_id, robot_element in enumerate(robot_data):
            print('\n> robot {0}'.format(robot_id))
            for leg_id, leg_element in enumerate(robot_element['legs']):
                print('\n> > leg {0}\n'.format(leg_id))
                for leg_info, leg_value in leg_element.items():
                    if leg_info is 'servos':
                        for servo_id, servo_element in enumerate(leg_value):
                            print('\n> > > servo {0}\n'.format(servo_id))
                            for servo_key, servo_value in servo_element.items():
                                print('--- {0}\n{1}'.format(servo_key, servo_value))
                    else:
                        print('-- {0}\n{1}'.format(leg_info, leg_value))

    # options
    def menu(self):

        print('\nWelcome to FELIX - Feedback Error Learning with dynamIXel!')

        options = {
            'e' : '[e]xit programm',
            'i' : '[i]nformation about the robot (data.py)',
            't' : '[t]oggle torque-activation',
            's' : 'set movement [s]peed for all servos',
            'r' : '[r]ead present position',
            'p' : '[p]rint saved list of angles and positions',
            'd' : 'move to [d]efault position',
            'x' : 'e[x]ecute dummy trajectory given in test_felix.py',
            'o' : 'move [o]ne servo to position given in degrees',
            'a' : 'move [a]ll servos to destination given in degrees'
            }

        while True:
            print('\n--------------------------------------------')
            print('Your Options:')
            for option in options.values():
                print(option)
            print('--------------------------------------------')

            choice = input('Please choose: ')   # user input


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
                if not args.virtual:
                    self.toggle_torque()
                else:
                    logger.info('Not (yet) supported in simulation mode.')


            # set movement [s]peed for all servos
            elif choice == 's':
                if not args.virtual:
                    self.leg.set_speed_for_all(int(input('Please input speed (default: 1000):')))
                else:
                    logger.info('Not (yet) supported in simulation mode.')


            # [r]ead present position
            elif choice == 'r':
                if not args.virtual:
                    # -- angles
                    angles = self.leg.get_current_degrees()
                    for servo_id, servo_pos in enumerate(angles):
                        print('> servo', servo_id, 'is at %7.3f degree.' % servo_pos)
                    # -- xyz
                    position = self.leg.forwardkin_alpha2end(*angles)
                    print('> leg is at XYZ (alpha2end):', position)
                    # -- save
                    saving = input('> save angles and position? (y/n)')
                    if saving == 'y':
                        self.write_angles_position(angles,position)
                        print('angles and position saved')
                else:
                    logger.info('Not (yet) supported in simulation mode.')


            # [p]rint saved list of angles and positions
            elif choice == 'p':
                self.print_angles_positions(self.read_angles_position_from_file())


            # move to [d]efault position
            elif choice == 'd':
                if not args.virtual:
                    if self.leg.torque:
                        offset = 0.005
                        pos = [0, 0, 90, 90]
                        for id, pos in enumerate(pos):
                            print('will move servo', id, 'to default position')
                            self.leg.move_servo_to_degrees(id, pos)
                            self.leg.test_servo_degree(id, pos, offset)
                    else: print('Please enable torque first!')
                else:
                    logger.info('Not (yet) supported in simulation mode.')

            
            # e[x]ecute dummy trajectory given in test_felix.py
            elif choice == 'x':
                if not args.virtual:
                    if self.leg.torque:
                        test_felix.run_trajectory(self.leg)
                    else:
                        logger.warning('Please enable torque first!')
                else:
                    logger.info('Not (yet) supported in simulation mode.')


            # move [o]ne servo to position given in degrees
            elif choice == 'o':
                if not args.virtual:
                    self.leg.move_servo_to_degrees(int(input('Please input servo-id:')), float(input('Please input position:')))
                else:
                    logger.info('Not (yet) supported in simulation mode.')


            # move [a]ll servos to destination given in degrees
            elif choice == 'a':
                if not args.virtual:
                    if self.leg.torque:
                        pos=list()
                        for i in range(self.leg.num_servo):
                            pos.append(input('Please input position for servo {}: '.format(i)))
                        self.leg.move_to_deg(pos)
                    else:
                        logger.warning('Please enable torque first!')
                    #self.leg.move_to_deg([int(x) for x in input('Please input position (default: 0 0 90 90):').split()])
                else:
                    logger.info('Not (yet) supported in simulation mode.')


            # else
            else:
                print('Invalid input... Please try again')


# main
def main():

    logger.info('Starting FELIX...')

    # Wake up...
    felix = robot()

    # UI
    felix.menu()

    

# jump to main
if __name__ == '__main__':
    main()

