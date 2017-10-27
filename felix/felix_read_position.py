import os

from leg import leg
from dict_servo import servo_all

DEVICENAME = "COM3".encode('utf-8')

felix = leg(servo_all,DEVICENAME)
felix.disable_torque()
while True:
    print(felix.get_current_position())
    input("Will read current position")