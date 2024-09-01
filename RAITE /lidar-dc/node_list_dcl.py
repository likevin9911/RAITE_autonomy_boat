#!/usr/bin/env python3
import rosnode
import rosgraph
import sys
import argparse
import rospy
from std_msgs.msg import *
import time 

def talker():
    global noise
    noise = 0.5
    pub = rospy.Publisher('Noise_LEVEL', Float32, queue_size=0)
    rospy.init_node('noise_chatter', anonymous=False)
    rate = rospy.Rate(10) # 10hz
    

    while not rospy.is_shutdown():
        rospy.loginfo_throttle(2,"Noise Level Published    %s",noise)
        pub.publish(noise)
        node_names = rosnode.get_node_names()
        for node in node_names:
            if node == '/map_saver':
                noise += 0
                rospy.loginfo("Increasing noise to +++++++++++++++++++++++ %s", noise)
                pub.publish(noise)
                time.sleep(2)
            elif noise > 22000:
                noise = 100




if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
