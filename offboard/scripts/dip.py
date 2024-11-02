#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist, PoseArray, PoseStamped
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
import math
import matplotlib.pyplot as plt
import numpy as np
from collections import deque

class BoatPIDController:
    def __init__(self):
        rospy.init_node('boat_pid_controller')

        # PID gain parameters
        self.kp_linear = rospy.get_param('~kp_linear', 0.75)
        self.ki_linear = rospy.get_param('~ki_linear', 0.0)
        self.kd_linear = rospy.get_param('~kd_linear', 0.05)

        self.kp_angular = rospy.get_param('~kp_angular', 1.0)
        self.ki_angular = rospy.get_param('~ki_angular', 0.0)
        self.kd_angular = rospy.get_param('~kd_angular', 0.0)

        # Deadband and rate limiting parameters
        self.angular_deadband = rospy.get_param('~angular_deadband', 0.01)
        self.angular_rate_limit = rospy.get_param('~angular_rate_limit', 0.02)

        #Stop Boat Variables
        self.reverse_movement_in_progress = False
        self.reverse_start_time = 0.0
        self.waiting_for_new_goal = False
        self.prev_cmd_linear = 0.0
        self.prev_cmd_angular = 0.0


        # Error thresholds and cmd_vel limits
        self.linear_error_threshold = rospy.get_param('~linear_error_threshold', 0.1)
        self.angular_error_threshold = rospy.get_param('~angular_error_threshold', 0.05)
        self.max_linear_cmd = 0.4
        self.max_linear_reverse_cmd = 0.2
        self.max_angular_cmd = 0.4
        self.reverse_velocity = -1.0

        # Reverse stopping thresholds
        self.imu_threshold = 0.2
        self.odom_velocity_threshold = 0.2

        # Maximum allowed acceleration
        self.max_linear_accel = 0.05
        self.max_angular_accel = 0.03

        # Smoothing parameters
        self.smoothing_window_size = 5

        # Subscribers and publishers
        self.odom_sub = rospy.Subscriber('/aft_mapped_to_init', Odometry, self.odom_callback)
        self.imu_sub = rospy.Subscriber('/imu/zeroed_data', Imu, self.imu_callback)
        self.teb_poses_sub = rospy.Subscriber('/move_base/TebLocalPlannerROS/teb_poses', PoseArray, self.teb_poses_callback)
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel_adjusted', Twist, queue_size=10)
        self.goal_sub = rospy.Subscriber('/move_base/current_goal', PoseStamped, self.goal_callback)

        # Pose and IMU data
        self.current_pose = None
        self.teb_poses = None
        self.yaw = 0.0
        self.angular_velocity_imu = 0.0
        self.acceleration_imu = np.array([0.0, 0.0, 0.0])
        self.odom_velocity = 0.0

        # For PID control
        self.prev_error_linear = 0
        self.prev_error_angular = 0
        self.integral_linear = 0
        self.integral_angular = 0

        # Goal tracking
        self.last_goal = None
        self.new_goal_detected = False
        self.reversing = False

        # For smoothing and filtering
        self.linear_vel_history = deque(maxlen=self.smoothing_window_size)
        self.angular_vel_history = deque(maxlen=self.smoothing_window_size)

        # For plotting
        self.time_steps = []
        self.linear_velocities = []
        self.angular_velocities = []
        self.current_pose_x = []
        self.current_pose_y = []
        self.desired_pose_x = []
        self.desired_pose_y = []
        self.start_time = rospy.get_time()

        # Set up the plot
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(10, 8))
        plt.ion()

    def imu_callback(self, msg):
        """Callback for zeroed IMU data (2D only)."""
        # Only take the x and y components; ignore z-axis data.
        self.angular_velocity_imu = msg.angular_velocity.z
        self.acceleration_imu = np.array([msg.linear_acceleration.x, msg.linear_acceleration.y])

    def odom_callback(self, msg):
        """Callback for odometry data (2D only)."""
        self.current_pose = msg.pose.pose

        # Extract yaw from the orientation (only considering 2D rotation).
        orientation_q = self.current_pose.orientation
        _, _, self.yaw = euler_from_quaternion([orientation_q.x, orientation_q.y,
                                                orientation_q.z, orientation_q.w])

        # Calculate 2D linear velocity (ignore z-axis).
        vx = msg.twist.twist.linear.x
        vy = msg.twist.twist.linear.y
        self.odom_velocity = math.sqrt(vx ** 2 + vy ** 2)

    def teb_poses_callback(self, msg):
        self.teb_poses = msg.poses


    def goal_callback(self, msg):
        """Detect goal change and reset the controller."""
        if self.last_goal is None or not self.compare_poses(self.last_goal, msg.pose):
            rospy.loginfo("New goal detected. Starting reverse maneuver.")
            self.last_goal = msg.pose
            self.new_goal_detected = True
            self.reversing = True
            self.waiting_for_new_goal = False  # Reset flag to resume movement

            # Reset angles and integral terms
            self.prev_error_angular = 0
            self.integral_angular = 0


    def compare_poses(self, pose1, pose2):
        """Compare two poses to see if they are the same (with some tolerance)."""
        return (abs(pose1.position.x - pose2.position.x) < 0.01 and
                abs(pose1.position.y - pose2.position.y) < 0.01 and
                abs(pose1.position.z - pose2.position.z) < 0.01)

    def compute_pid(self, error, prev_error, integral, kp, ki, kd):
        """Compute the PID output using the error, previous error, and integral term."""
        integral += error
        derivative = error - prev_error
        return kp * error + ki * integral + kd * derivative, integral

    def limit_cmd_vel(self, cmd_vel, max_val):
        """Limit the cmd_vel to the max_val."""
        return max(-max_val, min(cmd_vel, max_val))

    def limit_acceleration(self, current_vel, target_vel, max_accel):
        """Limit the acceleration rate."""
        accel = target_vel - current_vel
        if abs(accel) > max_accel:
            accel = max_accel if accel > 0 else -max_accel
        return current_vel + accel

    def apply_moving_average(self, history, new_value):
        history.append(new_value)
        return sum(history) / len(history)

    def is_goal_behind(self, current_position, future_poses):
        """Determine if the goal is behind the boat, with refined logic."""
        avg_x = sum([pose.position.x for pose in future_poses[:3]]) / 3.0
        avg_y = sum([pose.position.y for pose in future_poses[:3]]) / 3.0

        # Goal vector and boat heading in 2D
        goal_vector = np.array([avg_x - current_position.x, avg_y - current_position.y])
        boat_heading = np.array([math.cos(self.yaw), math.sin(self.yaw)])

        # Dot product to determine if the goal is behind
        dot_product = np.dot(boat_heading, goal_vector)

        # Check if the goal is behind based on dot product
        is_behind = dot_product < 0

        # Calculate the angle between the goal vector and boat heading
        angle_to_goal = math.atan2(goal_vector[1], goal_vector[0])
        angular_difference = self.normalize_angle(angle_to_goal - self.yaw)

        # Log the result
        direction = "left" if angular_difference < 0 else "right"
        rospy.loginfo(f"Goal is behind: {is_behind}, turning {direction}")
        
        return is_behind, angular_difference

    def normalize_angle(self, angle):
        """Normalize the angle to the range [-pi, pi]."""
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle



    def compute_angular_difference(self, future_poses):
        """Compute the angular difference (2D only) between average pose and boat's yaw."""
        if len(future_poses) < 4:
            rospy.logwarn("Insufficient future poses to calculate angular difference.")
            return 0.0  # Return zero angular difference if insufficient data

        # Extract and average the yaw from the first 4 poses
        yaws = []
        for i in range(4):
            orientation_q = future_poses[i].orientation
            _, _, yaw = euler_from_quaternion([orientation_q.x, orientation_q.y,
                                               orientation_q.z, orientation_q.w])
            yaws.append(yaw)

        # Compute the average yaw using trigonometric averaging
        avg_yaw = math.atan2(
            sum(math.sin(y) for y in yaws) / 4,
            sum(math.cos(y) for y in yaws) / 4
        )

        # Calculate angular difference and normalize to [-pi, pi]
        angular_difference = avg_yaw - self.yaw
        angular_difference = (angular_difference + math.pi) % (2 * math.pi) - math.pi

        # Round to 3 decimal places to avoid small fluctuations
        angular_difference = round(angular_difference, 3)

        # Apply deadband to ignore very small angular differences
        if abs(angular_difference) < self.angular_deadband:
            angular_difference = 0.0

        rospy.loginfo(f"Angular Difference (Avg Poses 1-4): {angular_difference} radians")
        return angular_difference




    def adjust_linear_velocity_based_on_angular(self, angular_vel, max_linear):
        """Scale linear velocity based on the absolute value of angular velocity using max values."""
        
        # Ensure both angular_vel and max_linear are within [-1, 1]
        angular_vel = max(-1.0, min(angular_vel, 1.0))  
        abs_angular = abs(angular_vel)

        # Calculate scaling factor: If angular is 1 or -1, linear should be close to 0
        # If angular is 0, linear should be close to max_linear
        scale = 1.0 - abs_angular  # Direct linear relation

        # Adjust linear velocity dynamically based on the scaling factor
        adjusted_linear = max_linear * scale

        rospy.loginfo(f"Angular Vel: {angular_vel}, Scale: {scale}, Adjusted Linear: {adjusted_linear}")
        return adjusted_linear




    def determine_turn_direction(self, goal_position):
        """Determine if the boat should turn left or right."""
        current_position = self.current_pose.position
        boat_heading = np.array([math.cos(self.yaw), math.sin(self.yaw)])

        goal_vector = np.array([goal_position.x - current_position.x, goal_position.y - current_position.y])
        cross_product = np.cross(boat_heading, goal_vector)

        return cross_product > 0  # Left turn if positive, right turn if negative


    def check_distance_to_goal(self):
        """Calculate distance to goal and reverse if within 2 meters."""
        # Check if we have both current_pose and last_goal
        if self.current_pose is None or self.last_goal is None:
            return
        # Compute the Euclidean distance between current_pose and last_goal
        dx = self.current_pose.position.x - self.last_goal.position.x
        dy = self.current_pose.position.y - self.last_goal.position.y
        distance = math.sqrt(dx**2 + dy**2)
        # Print the distance to the terminal
        rospy.loginfo(f"Distance to goal: {distance:.2f} meters")
        # If distance is less than 2m and not already reversing or waiting for new goal
        if distance < 5.0 and not self.reverse_movement_in_progress and not self.waiting_for_new_goal:
            rospy.loginfo("Distance less than 2m. Reversing for 5 seconds.")
            self.reverse_movement_in_progress = True
            self.reverse_start_time = rospy.get_time()
        if self.reverse_movement_in_progress:
            # Check if 5 seconds have passed
            current_time = rospy.get_time()
            if current_time - self.reverse_start_time < 5.0:
                # Publish cmd_vel with linear.x = -0.2, angular.z = 0
                cmd_vel = Twist()
                cmd_vel.linear.x = -0.2
                cmd_vel.angular.z = 0.0
                self.cmd_vel_pub.publish(cmd_vel)
            else:
                # Reverse movement complete
                self.reverse_movement_in_progress = False
                rospy.loginfo("Reverse movement complete. Waiting for new goal.")
                self.waiting_for_new_goal = True  # Set flag to wait for new goal
                # After reversing, set velocities to zero
                cmd_vel = Twist()
                cmd_vel.linear.x = 0.0
                cmd_vel.angular.z = 0.0
                self.cmd_vel_pub.publish(cmd_vel)




    def control_loop(self):
        rate = rospy.Rate(50)
    
        while not rospy.is_shutdown():
            if self.current_pose is None or self.teb_poses is None or len(self.teb_poses) < 5:
                rate.sleep()
                continue
    
            # Call the function to check distance to goal
            self.check_distance_to_goal()
    
            # If reverse movement is in progress due to proximity to goal, skip the rest of the loop
            if self.reverse_movement_in_progress:
                rate.sleep()
                continue
    
            # If waiting for new goal, set velocities to 0 and continue
            if self.waiting_for_new_goal:
                adjusted_cmd_vel = Twist()
                adjusted_cmd_vel.linear.x = 0.0
                adjusted_cmd_vel.angular.z = 0.0
                self.cmd_vel_pub.publish(adjusted_cmd_vel)
                rate.sleep()
                continue
    
            # Reverse and stop conditions when a new goal is detected
            if self.new_goal_detected:
                rospy.loginfo("Reversing to avoid obstacles before heading to new goal.")
                while self.reversing:
                    adjusted_cmd_vel = Twist()
                    adjusted_cmd_vel.linear.x = self.reverse_velocity
                    adjusted_cmd_vel.angular.z = 0  # No angular velocity during reverse
                    self.cmd_vel_pub.publish(adjusted_cmd_vel)
    
                    if self.stop_reverse_condition():
                        rospy.loginfo("Reverse maneuver complete. Resuming normal operation.")
                        self.reversing = False
    
                    rate.sleep()

                # Reset the yaw to avoid large jumps in angular difference
                orientation_q = self.current_pose.orientation
                _, _, self.yaw = euler_from_quaternion([orientation_q.x, orientation_q.y,
                                                        orientation_q.z, orientation_q.w])
                rospy.loginfo("Yaw reset after reverse maneuver.")
    
                self.new_goal_detected = False
                self.prev_error_linear = 0
                self.prev_error_angular = 0
                rospy.sleep(0.1)  # Brief pause to allow the system to stabilize

            future_poses = self.teb_poses[:5]
            current_position = self.current_pose.position

            # Compute angular difference using the corrected method
            angular_difference = self.compute_angular_difference(future_poses)
    
            # Check if the goal is behind the boat
            goal_behind, direction = self.is_goal_behind(current_position, future_poses)
    
            skip_pid_angular = False  # Flag to skip angular PID when reversing
    
            if goal_behind:
                rospy.loginfo(f"Goal is behind the boat, turning {'left' if angular_difference < 0 else 'right'}.")
    
                # Flip the angular difference sign to correctly reflect reverse turning direction.
                if angular_difference < 0:
                    adjusted_angular = abs(angular_difference)  # Clockwise, so negative angular velocity
                else:
                    adjusted_angular = -abs(angular_difference)  # Counter-clockwise, so positive angular velocity
    
                # Limit linear speed for reverse motion
                max_linear_speed = self.max_linear_reverse_cmd
                adjusted_linear = -1.0 * self.adjust_linear_velocity_based_on_angular(
                    adjusted_angular, max_linear_speed
                )
    
                skip_pid_angular = True  # We have already set adjusted_angular manually
            else:
                # Forward motion logic
                target_pose = self.teb_poses[2].position
                linear_error = math.sqrt((target_pose.x - current_position.x) ** 2 +
                                         (target_pose.y - current_position.y) ** 2)
    
                # Compute PID for linear velocity
                adjusted_linear, self.integral_linear = self.compute_pid(
                    linear_error, self.prev_error_linear, self.integral_linear,
                    self.kp_linear, self.ki_linear, self.kd_linear
                )
                self.prev_error_linear = linear_error
    
                # Adjust linear velocity based on angular difference
                adjusted_linear = self.adjust_linear_velocity_based_on_angular(
                    angular_difference, self.max_linear_cmd
                )
    
            if not skip_pid_angular:
                # Use the angular difference directly for angular PID control
                adjusted_angular, self.integral_angular = self.compute_pid(
                    angular_difference, self.prev_error_angular, self.integral_angular,
                    self.kp_angular, self.ki_angular, self.kd_angular
                )
                self.prev_error_angular = angular_difference  # Corrected this line
            else:
                # When skipping PID, reset integral term to prevent wind-up
                self.integral_angular = 0.0
    
            # Limit accelerations using previous command velocities
            adjusted_linear = self.limit_acceleration(self.prev_cmd_linear, adjusted_linear, self.max_linear_accel)
            adjusted_angular = self.limit_acceleration(self.prev_cmd_angular, adjusted_angular, self.max_angular_accel)
    
            # Apply moving average for smoothing
            adjusted_linear = self.apply_moving_average(self.linear_vel_history, adjusted_linear)
            adjusted_angular = self.apply_moving_average(self.angular_vel_history, adjusted_angular)

            # Limit velocities to the absolute max values
            adjusted_linear = self.limit_cmd_vel(adjusted_linear, self.max_linear_cmd)
            adjusted_angular = self.limit_cmd_vel(adjusted_angular, self.max_angular_cmd)
    
            rospy.loginfo(f"Angular Difference (Avg Poses 1-4): {angular_difference} radians")

            # Publish the command velocities
            adjusted_cmd_vel = Twist()
            adjusted_cmd_vel.linear.x = adjusted_linear
            adjusted_cmd_vel.angular.z = adjusted_angular
            self.cmd_vel_pub.publish(adjusted_cmd_vel)
    
            # Update previous command velocities
            self.prev_cmd_linear = adjusted_linear
            self.prev_cmd_angular = adjusted_angular
    
            rate.sleep()





    def stop_reverse_condition(self):
        """Check if the boat should stop reversing (2D IMU and odom only)."""
        imu_condition = (abs(self.angular_velocity_imu) < self.imu_threshold and
                         all(abs(a) < self.imu_threshold for a in self.acceleration_imu))
        odom_condition = self.odom_velocity < self.odom_velocity_threshold
        return imu_condition or odom_condition


    def update_plot(self):
        self.ax1.clear()
        self.ax1.plot(self.time_steps, self.linear_velocities, label='Linear Velocity', color='blue')
        self.ax1.plot(self.time_steps, self.angular_velocities, label='Angular Velocity', color='red')
        self.ax1.set_title('Linear and Angular Velocities')
        self.ax1.legend()

        self.ax2.clear()
        self.ax2.plot(self.current_pose_x, self.current_pose_y, label='Current Pose', color='blue')
        self.ax2.scatter(self.desired_pose_x, self.desired_pose_y, label='Desired Pose', color='green')
        self.ax2.set_title('Current Pose vs Desired Pose')
        self.ax2.legend()

        plt.draw()
        plt.pause(0.001)

if __name__ == '__main__':
    try:
        controller = BoatPIDController()
        controller.control_loop()
    except rospy.ROSInterruptException:
        pass
