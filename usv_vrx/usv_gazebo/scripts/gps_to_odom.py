#!/usr/bin/env python
import rospy
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import TwistStamped
from nav_msgs.msg import Odometry
import tf
from pyproj import Proj
import math

class GPSToOdometry:
    def __init__(self):
        rospy.init_node('gps_to_odometry')

        # Parameters
        self.base_lat = rospy.get_param('~base_lat', None)
        self.base_lon = rospy.get_param('~base_lon', None)
        self.base_alt = rospy.get_param('~base_alt', 0.0)

        if self.base_lat is None or self.base_lon is None:
            rospy.logerr('Base latitude and longitude must be set using parameters base_lat and base_lon.')
            exit(1)

        # Set up projections
        self.wgs84_proj = Proj(proj='latlong', datum='WGS84')
        self.utm_zone = int((self.base_lon + 180) / 6) + 1
        self.utm_proj = Proj(proj='utm', zone=self.utm_zone, datum='WGS84')

        # Compute base UTM coordinates
        self.base_easting, self.base_northing = self.wgs84_proj(self.base_lon, self.base_lat)
        self.base_easting, self.base_northing = self.utm_proj(self.base_lon, self.base_lat)

        # Subscribers
        rospy.Subscriber('/mavros/global_position/raw/fix', NavSatFix, self.gps_fix_callback)
        rospy.Subscriber('/mavros/global_position/raw/gps_vel', TwistStamped, self.gps_vel_callback)

        # Publisher
        self.odom_pub = rospy.Publisher('/gps/odom', Odometry, queue_size=10)

        # Variables to store the latest messages
        self.current_fix = None
        self.current_vel = None

        # TF Broadcaster
        self.tf_broadcaster = tf.TransformBroadcaster()

    def gps_fix_callback(self, msg):
        self.current_fix = msg
        self.publish_odometry()

    def gps_vel_callback(self, msg):
        self.current_vel = msg
        self.publish_odometry()

    def publish_odometry(self):
        if self.current_fix is None or self.current_vel is None:
            return

        # Convert GPS coordinates to UTM
        easting, northing = self.utm_proj(self.current_fix.longitude, self.current_fix.latitude)

        # Compute local ENU coordinates relative to the base station
        x = easting - self.base_easting
        y = northing - self.base_northing
        z = self.current_fix.altitude - self.base_alt

        # Create odometry message
        odom = Odometry()
        odom.header.stamp = rospy.Time.now()
        odom.header.frame_id = 'odom'  # Frame in which the pose is expressed
        odom.child_frame_id = 'base_link'  # Frame attached to the robot

        # Set position
        odom.pose.pose.position.x = x
        odom.pose.pose.position.y = y
        odom.pose.pose.position.z = z  # Use altitude if needed

        # Orientation is not provided by GPS; set to zero or use IMU data
        odom.pose.pose.orientation.x = 0.0
        odom.pose.pose.orientation.y = 0.0
        odom.pose.pose.orientation.z = 0.0
        odom.pose.pose.orientation.w = 1.0

        # Set position covariance if available
        if any(self.current_fix.position_covariance):
            odom.pose.covariance = self.current_fix.position_covariance
        else:
            # Default covariance if none provided
            odom.pose.covariance = [0.0]*36
            odom.pose.covariance[0] = 1.0  # X position variance
            odom.pose.covariance[7] = 1.0  # Y position variance
            odom.pose.covariance[14] = 1.0  # Z position variance

        # Set velocity
        odom.twist.twist.linear.x = self.current_vel.twist.linear.x
        odom.twist.twist.linear.y = self.current_vel.twist.linear.y
        odom.twist.twist.linear.z = self.current_vel.twist.linear.z

        # Set velocity covariance (if needed)
        odom.twist.covariance = [0.0]*36
        odom.twist.covariance[0] = 0.05  # X velocity variance
        odom.twist.covariance[7] = 0.02  # Y velocity variance
        odom.twist.covariance[14] = 0.01  # Z velocity variance

        # Publish odometry message
        self.odom_pub.publish(odom)

        # Broadcast transform (optional)
        self.tf_broadcaster.sendTransform(
            (odom.pose.pose.position.x, odom.pose.pose.position.y, odom.pose.pose.position.z),
            (odom.pose.pose.orientation.x, odom.pose.pose.orientation.y, odom.pose.pose.orientation.z, odom.pose.pose.orientation.w),
            odom.header.stamp,
            odom.child_frame_id,
            odom.header.frame_id
        )

if __name__ == '__main__':
    try:
        GPSToOdometry()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
