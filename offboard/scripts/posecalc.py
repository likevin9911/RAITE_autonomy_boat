#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseArray
from tf.transformations import euler_from_quaternion
import math

def pose_array_callback(msg):
    poses = msg.poses
    yaw_angles = []

    # Step 1: Extract Yaw Angles from Each Pose
    for index, pose in enumerate(poses):
        orientation_q = pose.orientation
        quaternion = [
            orientation_q.x,
            orientation_q.y,
            orientation_q.z,
            orientation_q.w
        ]
        # Convert quaternion to Euler angles
        roll, pitch, yaw = euler_from_quaternion(quaternion)
        yaw_angles.append(yaw)
        rospy.loginfo(f"Pose {index}: Yaw = {yaw:.6f} radians")

    # Step 2: Compute Angle Differences Between Consecutive Poses
    angle_differences = []
    for i in range(1, len(yaw_angles)):
        delta_yaw = yaw_angles[i] - yaw_angles[i - 1]
        # Normalize the angle to the range [-pi, pi]
        delta_yaw = (delta_yaw + math.pi) % (2 * math.pi) - math.pi
        angle_differences.append(delta_yaw)
        rospy.loginfo(f"Angle between Pose {i-1} and Pose {i}: ?Yaw = {delta_yaw:.6f} radians")

    # Optional: Print a separator for readability
    rospy.loginfo("--------------------------------------------------")

def angle_between_poses_node():
    rospy.init_node('angle_between_poses_node', anonymous=True)
    rospy.Subscriber('/move_base/TebLocalPlannerROS/teb_poses', PoseArray, pose_array_callback)
    rospy.loginfo("Subscribed to /move_base/TebLocalPlannerROS/teb_poses topic.")
    rospy.spin()

if __name__ == '__main__':
    try:
        angle_between_poses_node()
    except rospy.ROSInterruptException:
        pass
