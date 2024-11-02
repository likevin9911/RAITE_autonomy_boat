#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
import tf
import math

class PIDController:
    def __init__(self):
        # Initialize the ROS node
        rospy.init_node('pid_controller_node')

        # Subscribe to the aft_mapped_to_init topic from Point-LIO
        self.odom_sub = rospy.Subscriber('/aft_mapped_to_init', Odometry, self.odom_callback)

        # Publisher to the cmd_vel topic
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel_en', Twist, queue_size=10)

        # PID control parameters (tune these values as needed)
        self.kp_linear = rospy.get_param('~kp_linear', 1.0)
        self.ki_linear = rospy.get_param('~ki_linear', 0.0)
        self.kd_linear = rospy.get_param('~kd_linear', 0.1)

        self.kp_angular = rospy.get_param('~kp_angular', 4.0)
        self.ki_angular = rospy.get_param('~ki_angular', 0.0)
        self.kd_angular = rospy.get_param('~kd_angular', 0.1)

        # Initialize variables for PID computations
        self.linear_error_sum = 0.0
        self.angular_error_sum = 0.0

        self.prev_linear_error = 0.0
        self.prev_angular_error = 0.0

        # Define the goal position (can be set via ROS parameters)
        self.goal_x = rospy.get_param('~goal_x', 5.0)
        self.goal_y = rospy.get_param('~goal_y', 5.0)

        # Current pose of the robot
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_theta = 0.0

        # Control loop rate
        self.rate = rospy.Rate(20)  # 20 Hz

        # Flag to check if odometry data has been received
        self.odom_received = False

    def odom_callback(self, msg):
        # Update the robot's current position and orientation from odometry
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y

        # Convert quaternion to Euler angles
        orientation_q = msg.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, yaw) = tf.transformations.euler_from_quaternion(orientation_list)
        self.current_theta = yaw

        # Set the flag to True since odometry data has been received
        self.odom_received = True

    def run(self):
        while not rospy.is_shutdown():
            if not self.odom_received:
                rospy.loginfo("Waiting for odometry data...")
                rospy.sleep(0.1)
                continue
                rospy.loginfo("connected")

            # Compute the distance and angle to the goal
            linear_error = math.hypot(self.goal_x - self.current_x, self.goal_y - self.current_y)
            desired_theta = math.atan2(self.goal_y - self.current_y, self.goal_x - self.current_x)
            angular_error = desired_theta - self.current_theta

            # Normalize the angular error to the range [-pi, pi]
            angular_error = (angular_error + math.pi) % (2 * math.pi) - math.pi

            # PID computations for linear velocity
            self.linear_error_sum += linear_error
            linear_error_delta = linear_error - self.prev_linear_error
            linear_output = (self.kp_linear * linear_error +
                             self.ki_linear * self.linear_error_sum +
                             self.kd_linear * linear_error_delta)

            # PID computations for angular velocity
            self.angular_error_sum += angular_error
            angular_error_delta = angular_error - self.prev_angular_error
            angular_output = (self.kp_angular * angular_error +
                              self.ki_angular * self.angular_error_sum +
                              self.kd_angular * angular_error_delta)

            # Update previous errors
            self.prev_linear_error = linear_error
            self.prev_angular_error = angular_error

            # Create and publish the velocity command
            cmd = Twist()
            cmd.linear.x = max(min(linear_output, 0.5), -0.5)  # Limit linear speed
            cmd.angular.z = max(min(angular_output, 1.0), -1.0)  # Limit angular speed

            # Stop the robot if it's close enough to the goal
            if linear_error < 0.1:
                cmd.linear.x = 0.0
                cmd.angular.z = 0.0
                self.cmd_vel_pub.publish(cmd)
                rospy.loginfo("Goal reached!")
                break

            self.cmd_vel_pub.publish(cmd)
            self.rate.sleep()

if __name__ == '__main__':
    try:
        controller = PIDController()
        controller.run()
    except rospy.ROSInterruptException:
        pass
