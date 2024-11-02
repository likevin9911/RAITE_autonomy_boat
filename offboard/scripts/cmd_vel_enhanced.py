#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist  # Correct import
from pymavlink import mavutil
import time
from threading import Lock

class PIDController:
    def __init__(self):
        # Initialize the node
        rospy.init_node('pid_velocity_controller', anonymous=True)
        
        # Parameters for PID
        self.Kp_linear = rospy.get_param('~Kp_linear', 1.0)
        self.Ki_linear = rospy.get_param('~Ki_linear', 0.5)
        self.Kd_linear = rospy.get_param('~Kd_linear', 0.0)
        
        self.Kp_angular = rospy.get_param('~Kp_angular', 1.0)
        self.Ki_angular = rospy.get_param('~Ki_angular', 2.0)
        self.Kd_angular = rospy.get_param('~Kd_angular', 0.03)
        
        self.dt = rospy.get_param('~dt', 0.1)  # Time step
        
        # Initialize previous errors and integrals
        self.prev_error_linear = 0.0
        self.integral_linear = 0.0
        
        self.prev_error_angular = 0.0
        self.integral_angular = 0.0
        
        # Current velocity commands
        self.current_linear = 0.0
        self.current_angular = 0.0
        
        # Desired velocity commands
        self.desired_linear = 0.0
        self.desired_angular = 0.0
        
        # Publisher for enhanced cmd_vel
        self.pub = rospy.Publisher('/cmd_vel_enhanced', Twist, queue_size=10)
        
        # Subscriber to cmd_vel
        rospy.Subscriber('/cmd_vel', Twist, self.cmd_vel_callback)
        
        # Timer for PID updates
        rospy.Timer(rospy.Duration(self.dt), self.update_pid)
        
    def cmd_vel_callback(self, msg):
        """Callback to receive desired velocity commands."""
        self.desired_linear = msg.linear.x
        self.desired_angular = msg.angular.z
    
    def update_pid(self, event):
        """Compute PID and publish enhanced velocity commands."""
        # Calculate errors
        error_linear = self.desired_linear - self.current_linear
        error_angular = self.desired_angular - self.current_angular
        
        # Integrate errors
        self.integral_linear += error_linear * self.dt
        self.integral_angular += error_angular * self.dt
        
        # Derivative of errors
        derivative_linear = (error_linear - self.prev_error_linear) / self.dt
        derivative_angular = (error_angular - self.prev_error_angular) / self.dt
        
        # PID formula
        control_linear = (self.Kp_linear * error_linear +
                          self.Ki_linear * self.integral_linear +
                          self.Kd_linear * derivative_linear)
        
        control_angular = (self.Kp_angular * error_angular +
                           self.Ki_angular * self.integral_angular +
                           self.Kd_angular * derivative_angular)
        
        # Update previous errors
        self.prev_error_linear = error_linear
        self.prev_error_angular = error_angular
        
        # Update current velocities
        self.current_linear += control_linear
        self.current_angular += control_angular
        
        # Create and publish enhanced Twist message
        enhanced_twist = Twist()
        enhanced_twist.linear.x = self.current_linear
        enhanced_twist.angular.z = self.current_angular
        
        self.pub.publish(enhanced_twist)
        print(f"Published Enhanced cmd_vel: linear.x = {enhanced_twist.linear.x}, angular.z = {enhanced_twist.angular.z}")
        
        # Optional: Log the PID computations
        rospy.logdebug(f"Desired Linear: {self.desired_linear}, Enhanced Linear: {self.current_linear}")
        rospy.logdebug(f"Desired Angular: {self.desired_angular}, Enhanced Angular: {self.current_angular}")

def main():
    try:
        pid_controller = PIDController()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()
