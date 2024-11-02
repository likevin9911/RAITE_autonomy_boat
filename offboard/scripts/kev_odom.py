#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from pymavlink import mavutil
import time
from threading import Lock, Timer

class MotorController:
    def __init__(self):
        # Initialize ROS node
        rospy.init_node('mavlink_cmd_vel_listener', anonymous=True)

        # Load parameters from ROS parameter server or use defaults
        self.target_system_id = rospy.get_param('~target_system_id', 1)
        self.target_component_id = rospy.get_param('~target_component_id', 1)
        self.pwm_neutral = rospy.get_param('~pwm_neutral', 1495)
        self.pwm_forward_max = rospy.get_param('~pwm_forward_max', 2006)
        self.pwm_backward_min = rospy.get_param('~pwm_backward_min', 982)
        self.deadzone_forward = rospy.get_param('~deadzone_forward', 1540)
        self.deadzone_backward = rospy.get_param('~deadzone_backward', 1460)
        self.cmd_vel_min = rospy.get_param('~cmd_vel_min', -1.0)
        self.cmd_vel_max = rospy.get_param('~cmd_vel_max', 1.0)
        self.wheel_base = rospy.get_param('~wheel_base', 0.5)
        self.mavlink_connection = rospy.get_param('~mavlink_connection', 'udpin:192.168.144.25:15001')

        # Calibration factors
        self.left_motor_calibration = rospy.get_param('~left_motor_calibration', 1.0)
        self.right_motor_calibration = rospy.get_param('~right_motor_calibration', 1.0)

        # Initialize MAVLink connection
        self.master = self.connect_mavlink()

        # Initialize lock for thread safety
        self.vel_lock = Lock()

        # Initialize motors to neutral
        self.initialize_motors()

        # Subscribe to cmd_vel topic
        self.cmd_vel_subscriber = rospy.Subscriber(
            '/cmd_vel_adjusted',
            Twist,
            self.cmd_vel_callback
        )

        # Initialize watchdog timer
        self.watchdog_timeout = rospy.get_param('~watchdog_timeout', 1.0)  # seconds
        self.watchdog_timer = Timer(self.watchdog_timeout, self.watchdog_callback)
        self.watchdog_timer.start()

        rospy.loginfo("MotorController initialized and running.")

    def connect_mavlink(self):
        """Establish MAVLink connection."""
        try:
            master = mavutil.mavlink_connection(self.mavlink_connection)
            master.target_system = self.target_system_id
            master.target_component = self.target_component_id
            rospy.loginfo("Waiting for Pixhawk heartbeat...")
            master.wait_heartbeat(timeout=10)
            rospy.loginfo(
                f"Heartbeat received from system {master.target_system} component {master.target_component}"
            )
            return master
        except Exception as e:
            rospy.logerr(f"Failed to connect to Pixhawk: {e}")
            rospy.signal_shutdown("MAVLink connection failed.")

    def send_motor_pwms(self, left_pwm, right_pwm):
        """
        Send PWM values to both motors simultaneously on Channels 1 and 3.

        Args:
            left_pwm (int): PWM value for the left motor (Channel 1).
            right_pwm (int): PWM value for the right motor (Channel 3).
        """
        # Validate PWM values
        if not (self.pwm_backward_min <= left_pwm <= self.pwm_forward_max):
            rospy.logwarn(f"Left PWM {left_pwm} out of range. Clamping to valid range.")
            left_pwm = max(self.pwm_backward_min, min(self.pwm_forward_max, left_pwm))
        
        if not (self.pwm_backward_min <= right_pwm <= self.pwm_forward_max):
            rospy.logwarn(f"Right PWM {right_pwm} out of range. Clamping to valid range.")
            right_pwm = max(self.pwm_backward_min, min(self.pwm_forward_max, right_pwm))

        rc_channel_values = [65535] * 8  # No override for all channels
        rc_channel_values[0] = left_pwm   # Channel 1: Left Motor
        rc_channel_values[2] = right_pwm  # Channel 3: Right Motor

        try:
            self.master.mav.rc_channels_override_send(
                self.master.target_system,
                self.master.target_component,
                *rc_channel_values
            )
            rospy.logdebug(
                f"Sent PWM Override - Channels: {rc_channel_values}"
            )
            rospy.loginfo(
                f"Sent PWM Override - Left: {left_pwm} (Ch1), Right: {right_pwm} (Ch3)"
            )
        except Exception as e:
            rospy.logerr(f"Failed to send PWM commands: {e}")

    def scale_velocity_to_pwm(self, velocity, deadzone, min_pwm, max_pwm):
        """
        Scale the velocity input (-1 to 1) to a PWM value based on direction.

        Args:
            velocity (float): Velocity command ranging from -1.0 to 1.0.
            deadzone (int): PWM value representing the neutral position.
            min_pwm (int): PWM value for maximum reverse speed.
            max_pwm (int): PWM value for maximum forward speed.

        Returns:
            int: Scaled PWM value.
        """
        if velocity > 0:
            pwm = deadzone + int(round(velocity * (max_pwm - deadzone)))
        elif velocity < 0:
            pwm = deadzone + int(round(velocity * (deadzone - min_pwm)))
        else:
            pwm = deadzone
        return pwm

    def cmd_vel_callback(self, msg):
        """
        Callback function to convert cmd_vel messages to motor PWM commands.

        Args:
            msg (Twist): ROS Twist message containing velocity commands.
        """
        with self.vel_lock:
            linear_vel = max(
                self.cmd_vel_min, min(self.cmd_vel_max, msg.linear.x)
            )
            angular_vel = max(
                self.cmd_vel_min, min(self.cmd_vel_max, msg.angular.z)
            )

        rospy.logdebug(f"Received cmd_vel - Linear: {linear_vel}, Angular: {angular_vel}")

        if angular_vel == 0:
            # Straight movement: both motors get the same speed
            motor_speed = linear_vel
            pwm_base = self.deadzone_forward if motor_speed >= 0 else self.deadzone_backward
            pwm = self.scale_velocity_to_pwm(motor_speed, pwm_base, self.pwm_backward_min, self.pwm_forward_max)
            left_pwm = int(pwm * self.left_motor_calibration)
            right_pwm = int(pwm * self.right_motor_calibration)
            rospy.logdebug("Straight movement detected. Setting both PWMs to the same value.")
        else:
            # Differential drive calculations
            left_motor_speed = linear_vel - (angular_vel * self.wheel_base / 2.0)
            right_motor_speed = linear_vel + (angular_vel * self.wheel_base / 2.0)

            # Clamp motor speeds
            left_motor_speed = max(self.cmd_vel_min, min(self.cmd_vel_max, left_motor_speed))
            right_motor_speed = max(self.cmd_vel_min, min(self.cmd_vel_max, right_motor_speed))

            rospy.logdebug(f"Differential drive speeds - Left: {left_motor_speed}, Right: {right_motor_speed}")

            # Determine PWM bases based on direction
            if linear_vel >= 0:
                left_pwm_base = self.deadzone_forward
                right_pwm_base = self.deadzone_forward
                max_pwm = self.pwm_forward_max
                min_pwm = self.pwm_backward_min
            else:
                left_pwm_base = self.deadzone_backward
                right_pwm_base = self.deadzone_backward
                max_pwm = self.pwm_forward_max  # Even in reverse, max forward PWM is the upper limit
                min_pwm = self.pwm_backward_min

            # Convert motor speeds to PWM values
            left_pwm = self.scale_velocity_to_pwm(left_motor_speed, left_pwm_base, min_pwm, max_pwm)
            right_pwm = self.scale_velocity_to_pwm(right_motor_speed, right_pwm_base, min_pwm, max_pwm)

            # Apply calibration factors
            left_pwm = int(left_pwm * self.left_motor_calibration)
            right_pwm = int(right_pwm * self.right_motor_calibration)

        # Clamp PWM values to valid range
        left_pwm = max(self.pwm_backward_min, min(self.pwm_forward_max, left_pwm))
        right_pwm = max(self.pwm_backward_min, min(self.pwm_forward_max, right_pwm))

        rospy.logdebug(f"Converted PWM - Left: {left_pwm}, Right: {right_pwm}")

        # Send PWM commands
        self.send_motor_pwms(left_pwm, right_pwm)

    def initialize_motors(self):
        """Initialize both motors to the neutral PWM value to prevent accidental movement."""
        rospy.loginfo(f"Initializing motors to neutral PWM: {self.pwm_neutral}")
        self.send_motor_pwms(self.pwm_neutral, self.pwm_neutral)
        time.sleep(1)  # Allow time for PWM signals to stabilize

    def watchdog_callback(self):
        """
        Callback function to execute when watchdog timer expires.
        Sets PWM to neutral to prevent unintended movement.
        """
        rospy.logwarn("Watchdog timeout reached. Setting motors to neutral.")
        self.send_motor_pwms(self.pwm_neutral, self.pwm_neutral)

    def shutdown_hook(self):
        """
        Function to execute on node shutdown.
        """
        rospy.loginfo("Shutting down MotorController. Setting motors to neutral.")
        self.send_motor_pwms(self.pwm_neutral, self.pwm_neutral)
        self.watchdog_timer.cancel()

    def run(self):
        """Keep the node running."""
        rospy.on_shutdown(self.shutdown_hook)
        rospy.spin()

if __name__ == '__main__':
    try:
        controller = MotorController()
        controller.run()
    except rospy.ROSInterruptException:
        pass
