#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseArray, Pose
import tf
import numpy as np

class WaypointPublisher:
    def __init__(self):
        rospy.init_node('waypoint_publisher', anonymous=True)

        # Parameters
        self.num_waypoints = rospy.get_param('~num_waypoints', 20)
        self.waypoint_distance = rospy.get_param('~waypoint_distance', 1.0)  # 1 meter apart

        # Publishers
        self.waypoint_pub = rospy.Publisher('/waypoints', PoseWithCovarianceStamped, queue_size=10)
        self.waypoint_array_pub = rospy.Publisher('/waypoints_array', PoseArray, queue_size=10)

        # Subscriber
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)

        self.current_pose = None

    def odom_callback(self, odom_msg):
        self.current_pose = odom_msg.pose.pose
        self.generate_and_publish_waypoints()

    def generate_and_publish_waypoints(self):
        if self.current_pose is None:
            return

        # Extract current position and orientation
        current_x = self.current_pose.position.x
        current_y = self.current_pose.position.y
        _, _, current_yaw = tf.transformations.euler_from_quaternion([
            self.current_pose.orientation.x,
            self.current_pose.orientation.y,
            self.current_pose.orientation.z,
            self.current_pose.orientation.w
        ])

        # Generate waypoints in front of the current position
        waypoints_array = PoseArray()
        waypoints_array.header.frame_id = "map"
        waypoints_array.header.stamp = rospy.Time.now()

        for i in range(self.num_waypoints):
            # Create a new waypoint in a straight line
            waypoint = Pose()
            waypoint.position.x = current_x + (i + 1) * self.waypoint_distance * np.cos(current_yaw)
            waypoint.position.y = current_y + (i + 1) * self.waypoint_distance * np.sin(current_yaw)
            waypoint.position.z = self.current_pose.position.z

            # Set orientation to be the same as current orientation
            waypoint.orientation = self.current_pose.orientation

            waypoints_array.poses.append(waypoint)

            # Publish individual waypoint as PoseWithCovarianceStamped
            waypoint_cov = PoseWithCovarianceStamped()
            waypoint_cov.header.frame_id = "map"
            waypoint_cov.header.stamp = rospy.Time.now()
            waypoint_cov.pose.pose = waypoint
            self.waypoint_pub.publish(waypoint_cov)

        # Publish all waypoints as PoseArray
        self.waypoint_array_pub.publish(waypoints_array)
        rospy.loginfo(f'Published {self.num_waypoints} waypoints in front of the current pose.')

if __name__ == '__main__':
    try:
        wp_publisher = WaypointPublisher()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
