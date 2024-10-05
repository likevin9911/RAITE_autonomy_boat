#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu
import numpy as np

# Global variables to hold the accumulative data for trimming
angular_velocity_sum = np.zeros(3)
linear_acceleration_sum = np.zeros(3)
count = 0
calibrating = True
trim_values = None

# Callback function for IMU data during calibration and publishing
def imu_callback(data):
    global angular_velocity_sum, linear_acceleration_sum, count, trim_values

    if calibrating:
        # Accumulate data for trimming
        angular_velocity_sum += np.array([data.angular_velocity.x, data.angular_velocity.y, data.angular_velocity.z])
        linear_acceleration_sum += np.array([data.linear_acceleration.x, data.linear_acceleration.y, data.linear_acceleration.z])
        count += 1
    else:
        # Apply the trim values and publish adjusted IMU data
        imu_msg = Imu()

        # Copy all data from the original message to preserve everything except angular velocity and linear acceleration
        imu_msg = data  # Copy the entire original message

        # Apply trim values to angular velocity and linear acceleration (only change these fields)
        imu_msg.angular_velocity.x = data.angular_velocity.x - trim_values['angular_velocity'][0]
        imu_msg.angular_velocity.y = data.angular_velocity.y - trim_values['angular_velocity'][1]
        imu_msg.angular_velocity.z = data.angular_velocity.z - trim_values['angular_velocity'][2]
       
        imu_msg.linear_acceleration.x = data.linear_acceleration.x - trim_values['linear_acceleration'][0]
        imu_msg.linear_acceleration.y = data.linear_acceleration.y - trim_values['linear_acceleration'][1]
        imu_msg.linear_acceleration.z = data.linear_acceleration.z - trim_values['linear_acceleration'][2] + 9.81
       
        # Publish the corrected IMU data
        pub.publish(imu_msg)

def compute_trim_values():
    global angular_velocity_sum, linear_acceleration_sum, count

    # Compute the average trim values
    angular_velocity_avg = angular_velocity_sum / count
    linear_acceleration_avg = linear_acceleration_sum / count

    return {
        'angular_velocity': angular_velocity_avg,
        'linear_acceleration': linear_acceleration_avg
    }

if __name__ == '__main__':
    rospy.init_node('imu_trimmer')

    # Create the publisher for the corrected IMU data
    pub = rospy.Publisher('/mavros/imu/data_py', Imu, queue_size=10)

    # Subscribe to the original IMU data topic
    rospy.Subscriber('/mavros/imu/data', Imu, imu_callback)

    # Collect IMU data for 15 seconds for calibration
    rospy.loginfo("Calibrating IMU for 15 seconds...")
    rospy.sleep(15)

    # Stop calibration and compute the trim values
    calibrating = False
    trim_values = compute_trim_values()
    rospy.loginfo("Trim values calculated: %s", trim_values)

    # Continue subscribing and applying trims to the data
    rospy.spin()

	
