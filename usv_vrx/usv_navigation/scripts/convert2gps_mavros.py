#!/usr/bin/env python3

import rospy
import pcl
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
from visualization_msgs.msg import Marker
import numpy as np
from std_msgs.msg import ColorRGBA, Float32MultiArray
from sensor_msgs.msg import PointField
from std_msgs.msg import Header
import math
from geographiclib.geodesic import Geodesic
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
from mavros_msgs.msg import GPSRAW, Altitude

# Adjustable variables
MIN_Z_HEIGHT = -1.0  # Set this value to your desired minimum Z height
FRONT_DEGREES = 40  # Degrees in front of the LiDAR to keep

# Global variables to store current data from MAVROS
current_gps = None
current_imu = None
current_odom = None

def gps_callback(gps_msg):
    global current_gps
    current_gps = gps_msg

def imu_callback(imu_msg):
    global current_imu
    current_imu = imu_msg

def odom_callback(odom_msg):
    global current_odom
    current_odom = odom_msg

def convert_to_gps(center_x, center_y, center_z):
    if current_gps is None or current_imu is None or current_odom is None:
        rospy.logwarn("GPS, IMU, or Odometry data not available yet.")
        return None, None

    # Calculate distance and angle relative to the Velodyne
    distance = math.sqrt(center_x**2 + center_y**2)
    angle = math.degrees(math.atan2(center_y, center_x))

    # Extract yaw from the IMU orientation using quaternion to euler conversion
    orientation_q = current_imu.orientation
    _, _, yaw = tf.transformations.euler_from_quaternion([
        orientation_q.x,
        orientation_q.y,
        orientation_q.z,
        orientation_q.w
    ])

    # Adjust angle with current yaw
    total_angle = yaw + math.radians(angle)

    # Use the odometry position as the starting point for the geodesic conversion
    odom_position = current_odom.pose.pose.position
    reference_lat = current_gps.lat / 1e7  # Convert from GPSRAW format
    reference_lon = current_gps.lon / 1e7  # Convert from GPSRAW format
    reference_alt = current_gps.alt / 1000.0  # Convert from millimeters to meters

    # Calculate the displacement in latitude and longitude
    geod = Geodesic.WGS84
    gps_result = geod.Direct(reference_lat, reference_lon, math.degrees(total_angle), distance)

    return gps_result['lat2'], gps_result['lon2']

def pointcloud_callback(pointcloud_msg):
    # Clear previous markers
    marker_pub.publish(Marker(action=Marker.DELETEALL))

    # Convert PointCloud2 to PCL PointCloud
    point_list = list(pc2.read_points(pointcloud_msg, field_names=("x", "y", "z"), skip_nans=True))
    if not point_list:
        return

    pcl_data = pcl.PointCloud(np.array(point_list, dtype=np.float32))

    # Filter points by minimum Z height
    passthrough = pcl_data.make_passthrough_filter()
    passthrough.set_filter_field_name("z")
    passthrough.set_filter_limits(MIN_Z_HEIGHT, np.max(pcl_data.to_array()[:, 2]))
    cloud_filtered = passthrough.filter()

    # Filter points within the front degrees
    front_cloud = []
    for point in cloud_filtered.to_array():
        angle = math.degrees(math.atan2(point[1], point[0]))  # Calculate angle in degrees
        if -FRONT_DEGREES / 2 <= angle <= FRONT_DEGREES / 2:
            front_cloud.append(point)

    # Create and publish the filtered point cloud message
    header = Header()
    header.stamp = rospy.Time.now()
    header.frame_id = pointcloud_msg.header.frame_id
    fields = [
        PointField('x', 0, PointField.FLOAT32, 1),
        PointField('y', 4, PointField.FLOAT32, 1),
        PointField('z', 8, PointField.FLOAT32, 1),
    ]
    filtered_cloud_msg = pc2.create_cloud(header, fields, front_cloud)
    filtered_cloud_pub.publish(filtered_cloud_msg)

    # Clustering to find the largest cluster
    if len(front_cloud) > 0:
        pcl_front_cloud = pcl.PointCloud(np.array(front_cloud, dtype=np.float32))
        tree = pcl_front_cloud.make_kdtree()

        ec = pcl_front_cloud.make_EuclideanClusterExtraction()
        ec.set_ClusterTolerance(0.3)  # Adjust as needed
        ec.set_MinClusterSize(30)  # Adjust as needed
        ec.set_MaxClusterSize(15000)  # Adjust as needed
        ec.set_SearchMethod(tree)
        cluster_indices = ec.Extract()

        # Find the largest cluster
        largest_cluster_indices = max(cluster_indices, key=len)
        points = np.array([pcl_front_cloud[i] for i in largest_cluster_indices])

        # Calculate the bounding box for the largest cluster
        min_point = points.min(axis=0)
        max_point = points.max(axis=0)

        # Calculate the center and size of the bounding box
        center_x = (min_point[0] + max_point[0]) / 2.0
        center_y = (min_point[1] + max_point[1]) / 2.0
        center_z = (min_point[2] + max_point[2]) / 2.0

        # Calculate the GPS coordinates
        latitude, longitude = convert_to_gps(center_x, center_y, center_z)
        if latitude is not None and longitude is not None:
            rospy.loginfo(f"Object GPS Coordinates: Latitude = {latitude}, Longitude = {longitude}")

        # Create and publish the bounding box marker for the largest cluster
        marker = Marker()
        marker.header.frame_id = pointcloud_msg.header.frame_id
        marker.header.stamp = rospy.Time.now()
        marker.ns = "velodyne"
        marker.id = 0
        marker.type = Marker.CUBE
        marker.action = Marker.ADD

        # Bounding box center
        marker.pose.position.x = center_x
        marker.pose.position.y = center_y
        marker.pose.position.z = center_z

        # Bounding box dimensions
        marker.scale.x = max_point[0] - min_point[0]
        marker.scale.y = max_point[1] - min_point[1]
        marker.scale.z = max_point[2] - min_point[2]

        marker.color = ColorRGBA(1.0, 0.0, 0.0, 0.5)  # Red with 50% transparency

        # Publish the Marker
        marker_pub.publish(marker)

        # Publish the angle of the largest cluster's center
        angles_msg = Float32MultiArray()
        angles_msg.data.append(math.degrees(math.atan2(center_y, center_x)))
        angles_pub.publish(angles_msg)

if __name__ == "__main__":
    rospy.init_node('pointcloud_segmenter_filtered', anonymous=True)

    rospy.Subscriber("/mavros/global_position/raw/fix", GPSRAW, gps_callback)  # RTK GPS subscriber
    rospy.Subscriber("/mavros/imu/data", Imu, imu_callback)  # IMU subscriber
    rospy.Subscriber("/mavros/odometry/out", Odometry, odom_callback)  # Odometry subscriber

    rospy.Subscriber("/velodyne_points", PointCloud2, pointcloud_callback)

    marker_pub = rospy.Publisher("/bounding_box", Marker, queue_size=10)
    filtered_cloud_pub = rospy.Publisher("/filtered_velodyne_points", PointCloud2, queue_size=10)
    angles_pub = rospy.Publisher("/bounding_box_angles", Float32MultiArray, queue_size=10)  # Publish angles

    rospy.spin()
