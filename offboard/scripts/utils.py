#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Imu
import numpy as np

class IMUZeroing:
    def __init__(self):
        rospy.init_node('imu_zeroing_node')

        self.imu_sub = rospy.Subscriber('/imu/data', Imu, self.imu_callback)
        self.zeroed_imu_pub = rospy.Publisher('/imu/zeroed_data', Imu, queue_size=10)

        # Variables to hold bias calculations
        self.angular_velocity_bias = np.zeros(3)
        self.linear_acceleration_bias = np.zeros(3)
        self.orientation_bias = np.zeros(4)
        self.sample_count = 0

        self.zeroing_duration = rospy.get_param('~zeroing_duration', 5.0)
        self.imu_zero_start_time = None
        self.imu_zeroed = False

    def imu_callback(self, msg):
        if not self.imu_zeroed:
            if self.imu_zero_start_time is None:
                self.imu_zero_start_time = rospy.get_time()

            # Accumulate the IMU data for averaging
            self.angular_velocity_bias += np.array([msg.angular_velocity.x, msg.angular_velocity.y, msg.angular_velocity.z])
            self.linear_acceleration_bias += np.array([msg.linear_acceleration.x, msg.linear_acceleration.y, msg.linear_acceleration.z])
            self.orientation_bias += np.array([msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w])
            self.sample_count += 1

            if rospy.get_time() - self.imu_zero_start_time >= self.zeroing_duration:
                # Compute the average bias
                self.angular_velocity_bias /= self.sample_count
                self.linear_acceleration_bias /= self.sample_count
                self.orientation_bias /= self.sample_count
                self.imu_zeroed = True
                rospy.loginfo("IMU zeroing complete. Bias values calculated.")
            return

        # Publish zeroed IMU data
        self.publish_zeroed_imu(msg)

    def publish_zeroed_imu(self, msg):
        zeroed_imu_msg = Imu()

        # Zero out angular velocity and linear acceleration
        zeroed_imu_msg.angular_velocity.x = msg.angular_velocity.x - self.angular_velocity_bias[0]
        zeroed_imu_msg.angular_velocity.y = msg.angular_velocity.y - self.angular_velocity_bias[1]
        zeroed_imu_msg.angular_velocity.z = msg.angular_velocity.z - self.angular_velocity_bias[2]

        zeroed_imu_msg.linear_acceleration.x = msg.linear_acceleration.x - self.linear_acceleration_bias[0]
        zeroed_imu_msg.linear_acceleration.y = msg.linear_acceleration.y - self.linear_acceleration_bias[1]
        zeroed_imu_msg.linear_acceleration.z = msg.linear_acceleration.z - self.linear_acceleration_bias[2]

        # Zero out orientation (if needed)
        zeroed_imu_msg.orientation.x = msg.orientation.x - self.orientation_bias[0]
        zeroed_imu_msg.orientation.y = msg.orientation.y - self.orientation_bias[1]
        zeroed_imu_msg.orientation.z = msg.orientation.z - self.orientation_bias[2]
        zeroed_imu_msg.orientation.w = msg.orientation.w - self.orientation_bias[3]

        zeroed_imu_msg.header.stamp = rospy.Time.now()
        self.zeroed_imu_pub.publish(zeroed_imu_msg)

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    try:
        node = IMUZeroing()
        node.run()
    except rospy.ROSInterruptException:
        pass
