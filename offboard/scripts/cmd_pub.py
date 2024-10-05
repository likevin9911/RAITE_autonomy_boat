#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
import time

# Define min and max cmd_vel values (linear.x for forward velocity)
CMD_VEL_MIN = -0.5
CMD_VEL_MAX = 0.5

def publish_cmd_vel():
    # Initialize the ROS node
    rospy.init_node('cmd_vel_publisher')

    # Set up publisher for cmd_vel
    cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    # Create a Twist message for 50% forward speed
    twist = Twist()
    twist.linear.x = 0.5 * CMD_VEL_MAX  # 50% of maximum forward speed
    twist.angular.z = 0.0  # No rotation

    # Set the rate at which to publish cmd_vel (10 Hz)
    rate = rospy.Rate(10)

    start_time = time.time()

    # Keep publishing cmd_vel for 10 seconds
    while not rospy.is_shutdown() and (time.time() - start_time < 10):
        cmd_vel_pub.publish(twist)
        rate.sleep()

    # After 10 seconds, stop the robot by publishing zero velocities
    twist.linear.x = 0.0
    twist.angular.z = 0.0
    cmd_vel_pub.publish(twist)
    print("Published 50% speed for 10 seconds, then stopped.")

if __name__ == '__main__':
    try:
        publish_cmd_vel()
    except rospy.ROSInterruptException:
        pass
