#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from pymavlink import mavutil
import time
from threading import Lock

# MAVLink system and component IDs
TARGET_SYSTEM_ID = 1
TARGET_COMPONENT_ID = 1

# PWM limits
PWM_NEUTRAL = 1495          # Neutral PWM value (stop)
PWM_FORWARD_MIN = 1520      # Minimum PWM to move forward
PWM_FORWARD_MAX = 1748      # Maximum PWM for forward movement
PWM_BACKWARD_MAX = 1470     # Maximum PWM to move backward (closest to neutral)
PWM_BACKWARD_MIN = 1243     # Minimum PWM for reverse movement

# cmd_vel input ranges
CMD_VEL_MIN = -1.0
CMD_VEL_MAX = 1.0

# Scaling factors
LINEAR_SCALE = 1.2   # Adjusts the influence of linear velocity
ANGULAR_SCALE = 500  # Adjusts the influence of angular velocity (in PWM units)

# Lock for thread safety
vel_lock = Lock()

# Channels (1-indexed)
LEFT_MOTOR_CHANNEL = 4      # Channel 1: Left Motor
RIGHT_MOTOR_CHANNEL = 1     # Channel 4: Right Motor

def send_set_servo(master, channel, pwm):
    """
    Send a MAV_CMD_DO_SET_SERVO command to set PWM on a specific channel.

    Args:
        master: MAVLink connection object.
        channel (int): Servo channel (1-indexed).
        pwm (int): PWM value to set (typically between 1243-1748).
    """
    rospy.logdebug(f"Sending MAV_CMD_DO_SET_SERVO - Channel: {channel}, PWM: {pwm}")
    
    # Create the MAVLink message
    msg = master.mav.command_long_encode(
        0,  # target_system (0 for broadcast)
        0,  # target_component (0 for broadcast)
        mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
        0,  # confirmation
        channel,  # param1: Servo number (1-18)
        pwm,      # param2: PWM value
        0, 0, 0, 0, 0  # params 3-7 unused
    )
    
    # Send the message
    try:
        master.mav.send(msg)
        rospy.loginfo(f"Sent MAV_CMD_DO_SET_SERVO - Channel {channel}: PWM {pwm}")
    except Exception as e:
        rospy.logerr(f"Failed to send MAV_CMD_DO_SET_SERVO: {e}")

def send_motor_pwms(master, left_pwm, right_pwm):
    """
    Send PWM values to both motors using MAV_CMD_DO_SET_SERVO.

    Args:
        master: MAVLink connection object.
        left_pwm (int): PWM value for the left motor (Channel 1).
        right_pwm (int): PWM value for the right motor (Channel 4).
    """
    # Send PWM for Left Motor
    send_set_servo(master, LEFT_MOTOR_CHANNEL, left_pwm)
    
    # Send PWM for Right Motor
    send_set_servo(master, RIGHT_MOTOR_CHANNEL, right_pwm)

def scale_velocity_to_pwm(velocity):
    """
    Scale the linear velocity input (-1 to 1) to a PWM value, avoiding the dead zone.

    Args:
        velocity (float): Linear velocity ranging from -1.0 to 1.0.

    Returns:
        int: Base PWM value for both motors.
    """
    # Apply scaling factor
    scaled_velocity = velocity * LINEAR_SCALE

    # Clamp the scaled velocity to -1 to +1
    scaled_velocity = max(-1.0, min(1.0, scaled_velocity))

    if scaled_velocity > 0:
        # Map velocities from 0 to 1 to PWM_FORWARD_MIN to PWM_FORWARD_MAX
        pwm = PWM_FORWARD_MIN + scaled_velocity * (PWM_FORWARD_MAX - PWM_FORWARD_MIN)
    elif scaled_velocity < 0:
        # Map velocities from -1 to 0 to PWM_BACKWARD_MAX to PWM_BACKWARD_MIN
        pwm = PWM_BACKWARD_MAX + scaled_velocity * (PWM_BACKWARD_MAX - PWM_BACKWARD_MIN)
    else:
       pwm  = PWM_NEUTRAL  # No movement

    pwm = int(round(pwm))
    # Clamp PWM to valid range
    pwm = max(PWM_BACKWARD_MIN, min(PWM_FORWARD_MAX, pwm))
    return pwm

def cmd_vel_callback(msg, args):
    """
    Callback function to convert cmd_vel messages to motor PWM commands.

    Args:
        msg (Twist): ROS Twist message containing velocity commands.
        args (tuple): Tuple containing the MAVLink master connection.
    """
    master = args[0]

    with vel_lock:
        linear_vel = msg.linear.x   # Forward/Backward velocity
        angular_vel = msg.angular.z # Left/Right angular velocity

    # Calculate base PWM from linear velocity
    base_pwm = scale_velocity_to_pwm(linear_vel)

    # Calculate PWM offset from angular velocity
    angular_pwm_offset = angular_vel * ANGULAR_SCALE

    # Calculate final PWM values
    left_pwm = base_pwm + angular_pwm_offset
    right_pwm = base_pwm - angular_pwm_offset


    # Clamp PWM values to valid range
    left_pwm = int(round(max(PWM_BACKWARD_MIN, min(PWM_FORWARD_MAX, left_pwm))))
    right_pwm = int(round(max(PWM_BACKWARD_MIN, min(PWM_FORWARD_MAX, right_pwm))))

    # Log the velocity commands and corresponding PWM values
    rospy.loginfo(f"cmd_vel: linear={linear_vel}, angular={angular_vel}")
    rospy.loginfo(f"Left PWM: {left_pwm}, Right PWM: {right_pwm}")

    # Send the PWM commands to the motors
    send_motor_pwms(master, left_pwm, right_pwm)

def initialize_motors(master):
    """
    Initialize both motors to the neutral PWM value to prevent accidental movement.

    Args:
        master: MAVLink connection object.
    """
    rospy.loginfo("Initializing motors to neutral (1495)")
    send_motor_pwms(master, PWM_NEUTRAL, PWM_NEUTRAL)
    time.sleep(1)  # Allow time for PWM signals to stabilize

def shutdown_handler(master):
    """
    Shutdown handler to set motors to neutral when the script is terminated.

    Args:
        master: MAVLink connection object.
    """
    rospy.loginfo("Shutdown initiated. Setting motors to neutral.")
    try:
        send_motor_pwms(master, PWM_NEUTRAL, PWM_NEUTRAL)
    except Exception as e:
        rospy.logerr(f"Failed to set motors to neutral during shutdown: {e}")
    finally:
        rospy.loginfo("Motors set to neutral. Shutdown complete.")

def main():
    """
    Main function to initialize the ROS node, connect to Pixhawk, and subscribe to cmd_vel messages.
    """
    # Initialize the ROS node
    rospy.init_node('mavlink_cmd_vel_listener')

    # Connect to the Pixhawk via MAVLink
    try:
        master = mavutil.mavlink_connection('udpin:192.168.144.25:15001')
        rospy.loginfo("MAVLink connection established.")
    except Exception as e:
        rospy.logerr(f"Failed to connect to Pixhawk: {e}")
        return

    master.target_system = TARGET_SYSTEM_ID
    master.target_component = TARGET_COMPONENT_ID

    # Wait for the first heartbeat to confirm connection
    rospy.loginfo("Waiting for Pixhawk heartbeat...")
    try:
        master.wait_heartbeat(timeout=30)  # Timeout after 30 seconds
        rospy.loginfo(f"Heartbeat received from system {master.target_system} component {master.target_component}")
    except Exception as e:
        rospy.logerr(f"Heartbeat not received: {e}")
        return

    # Register shutdown handler to ensure motors are set to neutral
    rospy.on_shutdown(lambda: shutdown_handler(master))

    # Initialize motors to neutral
    initialize_motors(master)

    # Subscribe to the /cmd_vel_adjusted topic to receive velocity commands
    rospy.Subscriber('/cmd_vel_adjusted', Twist, cmd_vel_callback, (master,))

    # Keep the node running until shutdown
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        rospy.loginfo("ROS Interrupt Exception caught. Shutting down.")
    except KeyboardInterrupt:
        rospy.loginfo("KeyboardInterrupt detected. Shutting down.")
    except Exception as e:
        rospy.logerr(f"An unexpected error occurred: {e}")
