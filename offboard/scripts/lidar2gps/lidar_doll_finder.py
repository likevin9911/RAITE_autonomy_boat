#!/usr/bin/env python

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
FRONT_DEGREES = 90  # Degrees in front of the LiDAR to keep
NO_GPS_WARNING_SENT = False

# Cluster size thresholds in meters
MAX_CLUSTER_SIZE_X = 0.8
MAX_CLUSTER_SIZE_Y = 0.8
MAX_CLUSTER_SIZE_Z = 0.8

# Global variables to store current data from MAVROS
current_gps = None
current_imu = None
current_odom = None

# Switch between finding all clusters or the largest one
FIND_LARGEST_CLUSTER_ONLY = True  # Set this to True if you only want the largest cluster

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
    global NO_GPS_WARNING_SENT

    if current_gps is None or current_imu is None or current_odom is None:
        if not NO_GPS_WARNING_SENT:
            rospy.logwarn("No GPS data available; continuing without GPS-based localization.")
            NO_GPS_WARNING_SENT = True
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

    # Filter points within the front degrees
    front_cloud = []
    for point in pcl_data.to_array():
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

    # Clustering to find clusters that meet the size threshold
    if len(front_cloud) > 0:
        pcl_front_cloud = pcl.PointCloud(np.array(front_cloud, dtype=np.float32))
        tree = pcl_front_cloud.make_kdtree()

        ec = pcl_front_cloud.make_EuclideanClusterExtraction()
        ec.set_ClusterTolerance(0.3)  # Adjust as needed
        ec.set_MinClusterSize(30)  # Adjust as needed
        ec.set_MaxClusterSize(15000)  # Adjust as needed
        ec.set_SearchMethod(tree)
        cluster_indices = ec.Extract()

        # Filter clusters that fit within the size threshold
        valid_clusters = []
        for indices in cluster_indices:
            points = np.array([pcl_front_cloud[i] for i in indices])
            min_point = points.min(axis=0)
            max_point = points.max(axis=0)

            size_x = max_point[0] - min_point[0]
            size_y = max_point[1] - min_point[1]
            size_z = max_point[2] - min_point[2]

            # Check if the cluster fits within the specified size thresholds
            if size_x <= MAX_CLUSTER_SIZE_X and size_y <= MAX_CLUSTER_SIZE_Y and size_z <= MAX_CLUSTER_SIZE_Z:
                valid_clusters.append((indices, points, size_x, size_y, size_z))

        if not valid_clusters:
            rospy.loginfo("No valid clusters found within the size threshold.")
            return

        if FIND_LARGEST_CLUSTER_ONLY:
            # Select the largest cluster based on the number of points
            largest_cluster = max(valid_clusters, key=lambda c: len(c[0]))
            publish_bounding_box(0, largest_cluster[1], pointcloud_msg)
        else:
            # Publish bounding boxes for all valid clusters
            for idx, cluster in enumerate(valid_clusters):
                publish_bounding_box(idx, cluster[1], pointcloud_msg)

def publish_bounding_box(cluster_id, points, pointcloud_msg):
    # Calculate the bounding box for the cluster
    min_point = points.min(axis=0)
    max_point = points.max(axis=0)

    # Calculate the center and size of the bounding box
    center_x = (min_point[0] + max_point[0]) / 2.0
    center_y = (min_point[1] + max_point[1]) / 2.0
    center_z = (min_point[2] + max_point[2]) / 2.0

    # Calculate the GPS coordinates (optional)
    latitude, longitude = convert_to_gps(center_x, center_y, center_z)
    if latitude is not None and longitude is not None:
        rospy.loginfo(f"Object GPS Coordinates: Latitude = {latitude}, Longitude = {longitude}")
    else:
        rospy.loginfo(f"Bounding Box Center: x = {center_x}, y = {center_y}, z = {center_z}")

    # Create and publish the bounding box marker for the cluster
    marker = Marker()
    marker.header.frame_id = "velodyne"  # Ensure the frame ID is set to a valid one
    marker.header.stamp = rospy.Time.now()
    marker.ns = "velodyne"
    marker.id = cluster_id  # Assign a unique ID to each cluster
    marker.type = Marker.CUBE
    marker.action = Marker.ADD

    # Bounding box center
    marker.pose.position.x = center_x
    marker.pose.position.y = center_y
    marker.pose.position.z = center_z

    # Correct the orientation quaternion (set w = 1 for identity orientation)
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0  # Identity quaternion for no rotation

    # Bounding box dimensions
    marker.scale.x = max_point[0] - min_point[0]
    marker.scale.y = max_point[1] - min_point[1]
    marker.scale.z = max_point[2] - min_point[2]

    # Color of the marker
    marker.color = ColorRGBA(1.0, 0.0, 0.0, 0.5)  # Red with 50% transparency

    # Publish the Marker
    marker_pub.publish(marker)

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
