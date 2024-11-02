#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
import time
from std_msgs.msg import Bool

class StopBoatController:
    def __init__(self):
        rospy.init_node('stop_boat_controller')

        # -----------------------------------------
        # Parameters Affecting Stopping Performance
        # -----------------------------------------

        # Maximum reverse linear velocity (m/s)
        self.max_reverse_linear_vel = rospy.get_param('~max_reverse_linear_vel', -0.2)

        # Maximum reverse angular velocity (rad/s)
        self.max_reverse_angular_vel = rospy.get_param('~max_reverse_angular_vel', 0.2)

        # Deceleration rate (m/s^2)
        self.linear_deceleration = rospy.get_param('~linear_deceleration', 0.05)

        # Angular deceleration rate (rad/s^2)
        self.angular_deceleration = rospy.get_param('~angular_deceleration', 0.05)

        # Thresholds to consider the boat stopped
        self.linear_velocity_threshold = rospy.get_param('~linear_velocity_threshold', 0.05)
        self.angular_velocity_threshold = rospy.get_param('~angular_velocity_threshold', 0.05)

        # Time to maintain reverse thrust (seconds)
        self.reverse_thrust_duration = rospy.get_param('~reverse_thrust_duration', 2.0)

        # Rate at which to publish stop commands (Hz)
        self.publish_rate = rospy.get_param('~publish_rate', 20)

        # -----------------------------------------

        # Publisher to send stop commands
        self.stop_cmd_pub = rospy.Publisher('/stop_cmd_vel', Twist, queue_size=10)

        # Publisher to signal when stopping is complete
        self.stop_complete_pub = rospy.Publisher('/stop_complete', Bool, queue_size=1)

        # Subscriber to get current velocities
        self.odom_sub = rospy.Subscriber('/aft_mapped_to_init', Odometry, self.odom_callback)

        # Current velocities
        self.current_linear_vel = 0.0
        self.current_angular_vel = 0.0

        # Flag to indicate if odometry data has been received
        self.odom_received = False

    def odom_callback(self, msg):
        """Callback to update current linear and angular velocities."""
        vx = msg.twist.twist.linear.x
        vy = msg.twist.twist.linear.y
        self.current_linear_vel = math.sqrt(vx ** 2 + vy ** 2)
        self.current_angular_vel = msg.twist.twist.angular.z
        self.odom_received = True

    def stop_boat(self):
        """Logic to stop the boat dynamically."""
        rate = rospy.Rate(self.publish_rate)

        # Wait until odometry data is received
        while not self.odom_received and not rospy.is_shutdown():
            rospy.loginfo("Waiting for odometry data...")
            rate.sleep()

        rospy.loginfo("Odometry data received. Starting stop procedure.")

        # Initialize variables for deceleration
        start_time = time.time()
        elapsed_time = 0.0

        while not rospy.is_shutdown():
            # Calculate elapsed time
            elapsed_time = time.time() - start_time

            # Calculate desired velocities
            decel_linear_vel = max(0.0, self.current_linear_vel - self.linear_deceleration * elapsed_time)
            decel_angular_vel = max(0.0, abs(self.current_angular_vel) - self.angular_deceleration * elapsed_time)

            # Determine direction
            linear_direction = -1 if self.current_linear_vel > 0 else 1
            angular_direction = -1 if self.current_angular_vel > 0 else 1

            # Compute adjusted velocities
            adjusted_linear_vel = linear_direction * decel_linear_vel
            adjusted_angular_vel = angular_direction * decel_angular_vel

            # Limit the reverse velocities to the maximum allowed values
            adjusted_linear_vel = max(self.max_reverse_linear_vel, adjusted_linear_vel)
            adjusted_angular_vel = max(-self.max_reverse_angular_vel, min(adjusted_angular_vel, self.max_reverse_angular_vel))

            # Create and publish stop command
            stop_cmd = Twist()
            stop_cmd.linear.x = adjusted_linear_vel
            stop_cmd.angular.z = adjusted_angular_vel
            self.stop_cmd_pub.publish(stop_cmd)

            rospy.loginfo(f"Stopping... Linear Vel: {adjusted_linear_vel:.2f}, Angular Vel: {adjusted_angular_vel:.2f}")

            # Check if the boat has stopped
            if abs(self.current_linear_vel) <= self.linear_velocity_threshold and abs(self.current_angular_vel) <= self.angular_velocity_threshold:
                rospy.loginfo("Boat has stopped.")
                break

            # Limit the duration of reverse thrust
            if elapsed_time >= self.reverse_thrust_duration:
                rospy.loginfo("Reverse thrust duration exceeded.")
                break

            rate.sleep()

        # Send zero velocities to ensure the boat remains stopped
        stop_cmd = Twist()
        self.stop_cmd_pub.publish(stop_cmd)
        rospy.loginfo("Stop command executed. Boat should be stopped.")

        # Signal that stopping is complete
        self.stop_complete_pub.publish(Bool(data=True))

    def run(self):
        self.stop_boat()
        # Shutdown the node after stopping
        rospy.signal_shutdown("Boat has stopped. Exiting stop_boat.py.")

if __name__ == '__main__':
    try:
        controller = StopBoatController()
        controller.run()
    except rospy.ROSInterruptException:
        pass
