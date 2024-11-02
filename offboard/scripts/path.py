#!/usr/bin/env python3

import os
import subprocess
import signal

# Run utils.py before anything else
utils_path = os.path.join(os.path.dirname(__file__), 'utils.py')
utils_process = subprocess.Popen(['python3', utils_path])

import rospy
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist, PoseStamped
from nav_msgs.msg import Odometry, Path
from std_msgs.msg import Bool  # For communication with stop_boat.py
from tf.transformations import euler_from_quaternion
import math
import matplotlib.pyplot as plt
import numpy as np
from collections import deque

class BoatPIDController:
    def __init__(self):
        rospy.init_node('boat_pid_controller')

        # PID gain parameters
        self.kp_linear = rospy.get_param('~kp_linear', 1.0)
        self.ki_linear = rospy.get_param('~ki_linear', 0.0)
        self.kd_linear = rospy.get_param('~kd_linear', 0.05)

        self.kp_angular = rospy.get_param('~kp_angular', 1.0)  # Reduced proportional gain
        self.ki_angular = rospy.get_param('~ki_angular', 0.0)
        self.kd_angular = rospy.get_param('~kd_angular', 0.5)  # Increased derivative gain

        # Deadband and rate limiting parameters
        self.angular_deadband = rospy.get_param('~angular_deadband', 0.05)  # Increased deadband
        self.angular_rate_limit = rospy.get_param('~angular_rate_limit', 0.02)  # Reduced rate limit for smoother transitions

        # Error thresholds and cmd_vel limits
        self.linear_error_threshold = rospy.get_param('~linear_error_threshold', 0.1)
        self.angular_error_threshold = rospy.get_param('~angular_error_threshold', 0.05)
        self.max_linear_cmd = rospy.get_param('~max_linear_cmd', 0.25)  # Max linear velocity set to 0.25
        self.min_linear_cmd = rospy.get_param('~min_linear_cmd', 0.05)  # Reduced minimum linear command
        self.max_angular_cmd = rospy.get_param('~max_angular_cmd', 0.25)  # Max angular velocity set to 0.25
        self.min_angular_cmd = rospy.get_param('~min_angular_cmd', 0.01)  # Minimum angular velocity threshold

        # Maximum allowed acceleration
        self.max_linear_accel = 0.05
        self.max_angular_accel = 0.05  # Adjusted for smoother angular acceleration

        # Smoothing parameters
        self.smoothing_window_size = 5

        # Subscribers and publishers
        self.odom_sub = rospy.Subscriber('/aft_mapped_to_init', Odometry, self.odom_callback)
        self.imu_sub = rospy.Subscriber('/imu/zeroed_data', Imu, self.imu_callback)
        self.global_plan_sub = rospy.Subscriber('/move_base/GlobalPlanner/plan', Path, self.global_plan_callback)
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel_adjusted', Twist, queue_size=10)
        self.goal_sub = rospy.Subscriber('/move_base/current_goal', PoseStamped, self.goal_callback)

        # Subscriber to receive stop commands from stop_boat.py
        self.stop_cmd_sub = rospy.Subscriber('/stop_cmd_vel', Twist, self.stop_cmd_callback)

        # Subscriber to know when stopping is complete
        self.stop_complete_sub = rospy.Subscriber('/stop_complete', Bool, self.stop_complete_callback)

        # Pose and IMU data
        self.current_pose = None
        self.global_plan = None
        self.yaw = 0.0
        self.angular_velocity_imu = 0.0
        self.acceleration_imu = np.array([0.0, 0.0])
        self.odom_velocity = 0.0

        # For PID control
        self.prev_error_linear = 0
        self.prev_error_angular = 0
        self.integral_linear = 0
        self.integral_angular = 0

        # Previous command outputs for rate limiting
        self.prev_linear_cmd = 0.0
        self.prev_angular_cmd = 0.0

        # Goal tracking
        self.last_goal = None
        self.new_goal_detected = False

        # For smoothing and filtering
        self.linear_vel_history = deque(maxlen=self.smoothing_window_size)
        self.angular_vel_history = deque(maxlen=self.smoothing_window_size)
        self.angular_error_history = deque(maxlen=5)  # For filtering angular error

        # For plotting
        self.time_steps = []
        self.linear_velocities = []
        self.angular_velocities = []
        self.start_time = rospy.get_time()

        # Set up the plot
        self.fig, self.ax1 = plt.subplots(figsize=(10, 5))
        plt.ion()

        # Flag to indicate if the boat is currently stopping
        self.stopping = False

        # Variable to store stop command
        self.stop_cmd_vel = None

        # Process handle for stop_boat.py
        self.stop_boat_process = None

        # Distance threshold to trigger stopping when close to the goal (in meters)
        self.goal_distance_threshold = 0.2

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

    def global_plan_callback(self, msg):
        self.global_plan = msg.poses  # msg.poses is a list of PoseStamped

    def stop_cmd_callback(self, msg):
        """Callback to receive stop command velocities from stop_boat.py."""
        self.stop_cmd_vel = msg

    def stop_complete_callback(self, msg):
        """Callback to handle when stop_boat.py signals stopping is complete."""
        if msg.data:
            rospy.loginfo("Received stop complete signal.")
            self.stopping = False
            # Reset any necessary flags or variables
            self.prev_error_linear = 0
            self.prev_error_angular = 0
            self.integral_linear = 0
            self.integral_angular = 0
            self.prev_linear_cmd = 0.0
            self.prev_angular_cmd = 0.0

            # Close the stop_boat.py process if still running
            if self.stop_boat_process is not None and self.stop_boat_process.poll() is None:
                self.stop_boat_process.terminate()
                try:
                    self.stop_boat_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.stop_boat_process.kill()
                self.stop_boat_process = None

    def goal_callback(self, msg):
        """Detect goal change and initiate stop procedure if needed."""
        if self.last_goal is None or not self.compare_poses(self.last_goal, msg.pose):
            rospy.loginfo("New goal detected.")
            self.last_goal = msg.pose
            self.new_goal_detected = True

            # Set stopping flag
            self.stopping = True

            # Start stop_boat.py as a subprocess to stop the boat
            stop_boat_path = os.path.join(os.path.dirname(__file__), 'stop_boat.py')
            rospy.loginfo("Starting stop_boat.py to stop the boat due to new goal.")
            self.stop_boat_process = subprocess.Popen(['python3', stop_boat_path])

    def compare_poses(self, pose1, pose2):
        """Compare two poses to see if they are the same (with some tolerance)."""
        return (abs(pose1.position.x - pose2.position.x) < 0.01 and
                abs(pose1.position.y - pose2.position.y) < 0.01 and
                abs(pose1.position.z - pose2.position.z) < 0.01)

    def compute_pid(self, error, prev_error, integral, kp, ki, kd):
        """Compute the PID output using the error, previous error, and integral term."""
        derivative = error - prev_error
        integral += error
        output = kp * error + ki * integral + kd * derivative
        return output, integral

    def limit_cmd_vel(self, cmd_vel, max_val):
        """Limit the cmd_vel to the max_val."""
        cmd_vel_limited = max(-max_val, min(cmd_vel, max_val))
        # Apply minimum threshold for angular velocity
        if abs(cmd_vel_limited) < self.min_angular_cmd:
            cmd_vel_limited = 0.0
        return cmd_vel_limited

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
        num_poses = min(3, len(future_poses))
        avg_x = sum([pose.pose.position.x for pose in future_poses[:num_poses]]) / num_poses
        avg_y = sum([pose.pose.position.y for pose in future_poses[:num_poses]]) / num_poses

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
        """Compute the angular difference between the average path direction and boat's yaw."""

        num_poses = len(future_poses)
        if num_poses < 2:
            rospy.logwarn("Insufficient future poses to calculate angular difference.")
            return 0.0  # Return zero angular difference if insufficient data

        # Extract positions from future poses
        positions = np.array([[pose.pose.position.x, pose.pose.position.y] for pose in future_poses])

        # Fit a line using linear regression (least squares)
        x = positions[:, 0]
        y = positions[:, 1]

        # Handle the case where all x are the same (vertical line)
        if np.allclose(x, x[0]):
            path_angle = math.pi / 2 if y[-1] - y[0] > 0 else -math.pi / 2
        else:
            # Center the data
            x_mean = np.mean(x)
            y_mean = np.mean(y)
            x_cent = x - x_mean
            y_cent = y - y_mean

            # Calculate the best fit line angle
            numerator = np.sum(x_cent * y_cent)
            denominator = np.sum(x_cent ** 2)
            if denominator == 0:
                rospy.logwarn("Denominator for line fitting is zero.")
                return 0.0

            slope = numerator / denominator
            path_angle = math.atan(slope)

            # Adjust angle based on the direction of movement
            if x[-1] - x[0] < 0:
                path_angle += math.pi

        # Normalize path angle
        path_angle = self.normalize_angle(path_angle)

        # Calculate angular difference
        angular_difference = self.normalize_angle(path_angle - self.yaw)

        # Apply deadband to ignore very small angular differences
        if abs(angular_difference) < self.angular_deadband:
            angular_difference = 0.0

        # Apply low-pass filter to angular difference
        self.angular_error_history.append(angular_difference)
        angular_difference_filtered = sum(self.angular_error_history) / len(self.angular_error_history)

        rospy.loginfo(f"Computed path angle: {path_angle}, Angular difference (filtered): {angular_difference_filtered}")
        return angular_difference_filtered

    def adjust_linear_velocity_based_on_angular(self, angular_vel, max_linear, min_linear):
        """Scale linear velocity based on the absolute value of angular velocity using max and min values."""
        # Ensure angular_vel is within [-max_angular_cmd, max_angular_cmd]
        angular_vel = max(-self.max_angular_cmd, min(angular_vel, self.max_angular_cmd))
        abs_angular = abs(angular_vel)

        # Calculate scaling factor: 1 when abs_angular is 0, 0 when abs_angular is max_angular_cmd
        scale = 1.0 - abs_angular / self.max_angular_cmd

        # Adjust linear velocity dynamically based on the scaling factor
        adjusted_linear = min_linear + (max_linear - min_linear) * scale

        rospy.loginfo(f"Angular Vel: {angular_vel}, Scale: {scale}, Adjusted Linear: {adjusted_linear}")
        return adjusted_linear

    def control_loop(self):
        rate = rospy.Rate(50)

        while not rospy.is_shutdown():
            if self.current_pose is None or self.global_plan is None or len(self.global_plan) < 2:
                rate.sleep()
                continue

            if self.stopping:
                # Use stop commands from stop_boat.py
                if self.stop_cmd_vel is not None:
                    # Optionally apply smoothing here if needed
                    self.cmd_vel_pub.publish(self.stop_cmd_vel)
                    rospy.loginfo("Executing stop command from stop_boat.py")
                else:
                    rospy.logwarn("No stop command received yet.")
                rate.sleep()
                continue

            # Check if the boat is within the goal distance threshold
            goal_reached = self.is_goal_reached()
            if goal_reached and not self.stopping:
                rospy.loginfo("Boat is within goal distance threshold. Initiating stop procedure.")
                self.stopping = True
                # Start stop_boat.py as a subprocess to stop the boat
                stop_boat_path = os.path.join(os.path.dirname(__file__), 'stop_boat.py')
                rospy.loginfo("Starting stop_boat.py to stop the boat due to proximity to goal.")
                self.stop_boat_process = subprocess.Popen(['python3', stop_boat_path])
                rate.sleep()
                continue

            future_poses = self.global_plan[:min(10, len(self.global_plan))]  # Adjust based on available poses
            current_position = self.current_pose.position

            # Compute angular difference using the modified method
            angular_difference = self.compute_angular_difference(future_poses)

            # Check if the goal is behind the boat
            goal_behind, direction = self.is_goal_behind(current_position, future_poses)

            if goal_behind:
                rospy.loginfo(f"Goal is behind the boat, turning {'left' if angular_difference < 0 else 'right'}.")

                # Set linear velocity to zero and adjust angular velocity to turn in place
                adjusted_linear = 0.0
                adjusted_angular = angular_difference

            else:
                # Forward motion logic
                target_index = min(5, len(self.global_plan) - 1)  # Adjust index to not exceed list length
                target_pose = self.global_plan[target_index].pose.position
                linear_error = math.sqrt((target_pose.x - current_position.x) ** 2 +
                                         (target_pose.y - current_position.y) ** 2)

                # Compute PID for linear velocity
                adjusted_linear_pid, self.integral_linear = self.compute_pid(
                    linear_error, self.prev_error_linear, self.integral_linear,
                    self.kp_linear, self.ki_linear, self.kd_linear
                )
                # Update prev_error_linear
                self.prev_error_linear = linear_error

                # Adjust linear velocity based on angular difference
                adjusted_linear = self.adjust_linear_velocity_based_on_angular(
                    self.prev_angular_cmd, self.max_linear_cmd, self.min_linear_cmd
                )

                # Compute PID for angular velocity
                adjusted_angular_pid, self.integral_angular = self.compute_pid(
                    angular_difference, self.prev_error_angular, self.integral_angular,
                    self.kp_angular, self.ki_angular, self.kd_angular
                )
                # Update prev_error_angular
                self.prev_error_angular = angular_difference

                adjusted_angular = adjusted_angular_pid

            # Limit the angular velocity to the max value
            adjusted_angular = self.limit_cmd_vel(adjusted_angular, self.max_angular_cmd)

            # Apply angular velocity ramp-up/ramp-down for smoother transitions
            adjusted_angular = self.smooth_angular_velocity(adjusted_angular)

            # Limit accelerations
            adjusted_linear = self.limit_acceleration(self.prev_linear_cmd, adjusted_linear, self.max_linear_accel)
            adjusted_angular = self.limit_acceleration(self.prev_angular_cmd, adjusted_angular, self.max_angular_accel)

            # Apply moving average for smoothing
            adjusted_linear = self.apply_moving_average(self.linear_vel_history, adjusted_linear)
            adjusted_angular = self.apply_moving_average(self.angular_vel_history, adjusted_angular)

            # Limit velocities to the absolute max values
            adjusted_linear = max(0.0, min(adjusted_linear, self.max_linear_cmd))  # Ensure linear velocity is non-negative
            adjusted_angular = self.limit_cmd_vel(adjusted_angular, self.max_angular_cmd)

            rospy.loginfo(f"Adjusted Linear Vel: {adjusted_linear}, Adjusted Angular Vel: {adjusted_angular}")

            # Publish the command velocities
            adjusted_cmd_vel = Twist()
            adjusted_cmd_vel.linear.x = adjusted_linear
            adjusted_cmd_vel.angular.z = adjusted_angular
            self.cmd_vel_pub.publish(adjusted_cmd_vel)

            # Update previous command outputs
            self.prev_linear_cmd = adjusted_linear
            self.prev_angular_cmd = adjusted_angular

            # Update plotting data
            current_time = rospy.get_time() - self.start_time
            self.time_steps.append(current_time)
            self.linear_velocities.append(adjusted_linear)
            self.angular_velocities.append(adjusted_angular)
            self.update_plot()

            rate.sleep()

    def is_goal_reached(self):
        """Check if the boat is within the goal distance threshold."""
        if self.last_goal is None or self.current_pose is None:
            return False

        # Calculate distance to the goal
        goal_position = self.last_goal.position
        current_position = self.current_pose.position
        distance = math.sqrt((goal_position.x - current_position.x) ** 2 +
                             (goal_position.y - current_position.y) ** 2)

        rospy.loginfo(f"Distance to goal: {distance:.2f} meters")
        return distance <= self.goal_distance_threshold

    def smooth_angular_velocity(self, target_angular_vel):
        """Smoothly adjust angular velocity to reduce oscillations."""
        # Implement a simple low-pass filter
        alpha = 0.1  # More smoothing
        smoothed_angular = alpha * target_angular_vel + (1 - alpha) * self.prev_angular_cmd
        return smoothed_angular

    def update_plot(self):
        self.ax1.clear()
        self.ax1.plot(self.time_steps, self.linear_velocities, label='Linear Velocity', color='blue')
        self.ax1.plot(self.time_steps, self.angular_velocities, label='Angular Velocity', color='red')
        self.ax1.set_title('Linear and Angular Velocities')
        self.ax1.set_xlabel('Time (s)')
        self.ax1.set_ylabel('Velocity')
        self.ax1.legend()

        plt.draw()
        plt.pause(0.001)

    def shutdown(self):
        """Shutdown handler to clean up resources."""
        # Terminate the utils.py process
        if utils_process.poll() is None:
            utils_process.terminate()
            try:
                utils_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                utils_process.kill()

        # Terminate the stop_boat.py process if still running
        if self.stop_boat_process is not None and self.stop_boat_process.poll() is None:
            self.stop_boat_process.terminate()
            try:
                self.stop_boat_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.stop_boat_process.kill()
            self.stop_boat_process = None

        plt.close(self.fig)

if __name__ == '__main__':
    try:
        controller = BoatPIDController()
        rospy.on_shutdown(controller.shutdown)
        controller.control_loop()
    except rospy.ROSInterruptException:
        pass
