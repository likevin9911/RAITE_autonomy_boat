#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from pymavlink import mavutil
import time

# MAVLink system and component IDs
TARGET_SYSTEM_ID = 1
TARGET_COMPONENT_ID = 1

# PWM limits
PWM_NEUTRAL = 1500          # Neutral PWM value (stop)
PWM_START = 1000            # Starting PWM value for testing
PWM_END = 2000              # Ending PWM value for testing
PWM_STEP = 100              # Increment step for PWM
PWM_DELAY = 10              # Delay in seconds between PWM changes

# Channels (1-indexed)
LEFT_MOTOR_CHANNEL = 4      # Channel 1: Left Motor
RIGHT_MOTOR_CHANNEL = 1     # Channel 4: Right Motor

def send_set_servo(master, channel, pwm):
    """
    Send a MAV_CMD_DO_SET_SERVO command to set PWM on a specific channel.

    Args:
        master: MAVLink connection object.
        channel (int): Servo channel (1-indexed).
        pwm (int): PWM value to set (typically between 1100-1900).
    """
    rospy.logdebug(f"Sending MAV_CMD_DO_SET_SERVO - Channel: {channel}, PWM: {pwm}")
    
    # Create the MAVLink message
    msg = master.mav.command_long_encode(
        0,  # target_system (0 for broadcast, but we'll specify below)
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

def initialize_motors(master):
    """
    Initialize both motors to the neutral PWM value to prevent accidental movement.

    Args:
        master: MAVLink connection object.
    """
    rospy.loginfo(f"Initializing motors to neutral ({PWM_NEUTRAL})")
    send_set_servo(master, LEFT_MOTOR_CHANNEL, PWM_NEUTRAL)  # Channel 1: Left Motor
    send_set_servo(master, RIGHT_MOTOR_CHANNEL, PWM_NEUTRAL)  # Channel 4: Right Motor
    #rospy.sleep(1)  # Allow time for PWM signals to stabilize

def run_motor_test(master):
    send_set_servo(master, 1, 2000)#left
    send_set_servo(master, 4, 1500)#right



def shutdown_handler(master):
    """
    Shutdown handler to set motors to neutral when the script is terminated.

    Args:
        master: MAVLink connection object.
    """
    rospy.loginfo("Shutdown initiated. Setting motors to neutral.")
    try:
        send_set_servo(master, LEFT_MOTOR_CHANNEL, PWM_NEUTRAL)
        send_set_servo(master, RIGHT_MOTOR_CHANNEL, PWM_NEUTRAL)
    except Exception as e:
        rospy.logerr(f"Failed to set motors to neutral during shutdown: {e}")
    finally:
        rospy.loginfo("Motors set to neutral. Shutdown complete.")

def main():
    """
    Main function to initialize the ROS node, connect to Pixhawk, and run motor tests.
    """
    # Initialize the ROS node
    rospy.init_node('mavlink_motor_test', anonymous=True, log_level=rospy.DEBUG)

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

    # Arm Pixhawk

    # Register shutdown handler to ensure motors are set to neutral
    rospy.on_shutdown(lambda: shutdown_handler(master))

    # Initialize motors to neutral
    initialize_motors(master)

    # Run PWM test on left motor
    run_motor_test(master)

    if rospy.is_shutdown():
        rospy.loginfo("ROS shutdown detected. Exiting main function.")
        return

    # Wait before starting the right motor test
    rospy.loginfo(f"\nWaiting for {PWM_DELAY} seconds before starting the right motor test...")
    try:
        rospy.sleep(PWM_DELAY)
    except rospy.ROSInterruptException:
        rospy.loginfo("ROS Interrupt during wait. Exiting main function.")
        return

    if rospy.is_shutdown():
        rospy.loginfo("ROS shutdown detected after wait. Exiting main function.")
        return

    # Run PWM test on right motor
    run_motor_test(master, motor='right')

    if rospy.is_shutdown():
        rospy.loginfo("ROS shutdown detected. Exiting main function.")
        return

    # Finalize by setting both motors to neutral
    initialize_motors(master)
    rospy.loginfo("\nMotor tests completed. Motors set to neutral.")

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        rospy.loginfo("ROS Interrupt Exception caught. Shutting down.")
    except KeyboardInterrupt:
        rospy.loginfo("KeyboardInterrupt detected. Shutting down.")
    except Exception as e:
        rospy.logerr(f"An unexpected error occurred: {e}")
