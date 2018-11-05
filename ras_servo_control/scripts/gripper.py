#!/usr/bin/env python

import rospy
import rospy
import std_msgs.msg
import geometry_msgs.msg
import time 
from arduino_servo_control.srv import *


FLAG_GRIPPED = False
FLAG_FOUND_OBJECT = False
FLAG_CLOSE = True
FLAG_OPEN = False
FLAG_GRIP = False


#####################################################
#                    flag callback                  #
#####################################################
def flag_callback(msg):
    global FLAG_GRIPPED, FLAG_FOUND_OBJECT,FLAG_CLOSE, FLAG_GRIP, FLAG_OPEN
    flag = msg.data
    #rospy.loginfo('flag')
    if flag == "detect_object_done" and not FLAG_FOUND_OBJECT: 
        FLAG_OPEN = True
        FLAG_FOUND_OBJECT = True
    elif flag == "path_following_done":
        if  FLAG_FOUND_OBJECT:
            FLAG_GRIP = True
            FLAG_GRIPPED = True
        elif FLAG_GRIPPED:
            FLAG_OPEN = True
            FLAG_FOUND_OBJECT = False
            FLAG_GRIPPED = False
        else:
            pass
    else:
        pass

def main():
    global FLAG_GRIPPED, FLAG_FOUND_OBJECT, FLAG_CLOSE, FLAG_GRIP, FLAG_OPEN
    rospy.init_node('gripper_node')
    GRIP = rospy.ServiceProxy('/arduino_servo_control/set_servo_angles', SetServoAngles)
    time.sleep(2)
    rospy.Subscriber("/flag_done", std_msgs.msg.String, flag_callback)
    while not rospy.is_shutdown():
        if FLAG_OPEN:
            GRIP(70, 110) 
            print("open")
            time.sleep(1)
            FLAG_OPEN = False
        elif FLAG_CLOSE:
            GRIP(170, 10)
            print("close")
            time.sleep(1)
            FLAG_CLOSE = False
        elif FLAG_GRIP:
            GRIP(130,50)
            print("grip")
            time.sleep(1)
            FLAG_GRIP = False
        else:
            pass
    

if __name__ == '__main__':
    main()