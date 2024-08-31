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
import tf
from tf2_ros import TransformListener, Buffer
import csv
import os
from collections import deque

# Adjustable variables
MIN_Z_HEIGHT = -1.0  # Set this value to your desired minimum Z height
FRONT_DEGREES = 40  # Degrees in front of the LiDAR to keep
CLUSTER_TOLERANCE = 0.5  # Increase tolerance for more consistent clusters
MIN_CLUSTER_SIZE = 50  # Increase min cluster size to avoid small noise clusters
MAX_CLUSTER_SIZE = 20000  # Adjust based on your environment

# Parameters for smoothing
SMOOTHING_WINDOW_SIZE = 5

# Global variables for GPS simulation and smoothing
gps_memory = []
csv_file_path = 'gps_coordinates.csv'
bbox_history = deque(maxlen=SMOOTHING_WINDOW_SIZE)

# Initialize the CSV file
def init_csv():
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Latitude', 'Longitude', 'Timestamp'])

def write_to_csv(latitude, longitude, timestamp):
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([latitude, longitude, timestamp])
    rospy.loginfo(f"Written to CSV: Latitude = {latitude}, Longitude = {longitude}, Timestamp = {timestamp}")

def remember_location(latitude, longitude, timestamp):
    # Store GPS coordinates in the memory and write to CSV
    gps_memory.append((latitude, longitude, timestamp))
    write_to_csv(latitude, longitude, timestamp)

def simulate_gps(center_x, center_y):
    try:
        # Simulate GPS coordinates based on the Velodyne's fixed frame
        starting_latitude = 37.4275  # Example starting latitude
        starting_longitude = -122.1697  # Example starting longitude

        # Convert the distance and angle to latitude and longitude
        distance = math.sqrt(center_x**2 + center_y**2)
        angle = math.degrees(math.atan2(center_y, center_x))

        # Use the starting GPS coordinates to simulate movement
        geod = Geodesic.WGS84
        gps_result = geod.Direct(starting_latitude, starting_longitude, angle, distance)

        latitude = gps_result['lat2']
        longitude = gps_result['lon2']

        return latitude, longitude
    except Exception as e:
        rospy.logwarn("GPS Simulation Error: {}".format(e))
        return None, None

def smooth_bounding_box(min_point, max_point):
    bbox_history.append((min_point, max_point))
    
    if len(bbox_history) < SMOOTHING_WINDOW_SIZE:
        return min_point, max_point
    
    avg_min_point = np.mean([bbox[0] for bbox in bbox_history], axis=0)
    avg_max_point = np.mean([bbox[1] for bbox in bbox_history], axis=0)
    
    return avg_min_point, avg_max_point

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
        ec.set_ClusterTolerance(CLUSTER_TOLERANCE)  # Adjust as needed
        ec.set_MinClusterSize(MIN_CLUSTER_SIZE)  # Adjust as needed
        ec.set_MaxClusterSize(MAX_CLUSTER_SIZE)  # Adjust as needed
        ec.set_SearchMethod(tree)
        cluster_indices = ec.Extract()

        # Find the largest cluster
        largest_cluster_indices = max(cluster_indices, key=len)
        points = np.array([pcl_front_cloud[i] for i in largest_cluster_indices])

        # Calculate the bounding box for the largest cluster
        min_point = points.min(axis=0)
        max_point = points.max(axis=0)

        # Smooth the bounding box dimensions
        smoothed_min_point, smoothed_max_point = smooth_bounding_box(min_point, max_point)

        # Calculate the center of the bounding box
        center_x = (smoothed_min_point[0] + smoothed_max_point[0]) / 2.0
        center_y = (smoothed_min_point[1] + smoothed_max_point[1]) / 2.0
        center_z = (smoothed_min_point[2] + smoothed_max_point[2]) / 2.0

        # Simulate GPS coordinates for the largest cluster
        latitude, longitude = simulate_gps(center_x, center_y)
        if latitude is not None and longitude is not None:
            timestamp = rospy.Time.now().to_sec()
            rospy.loginfo(f"Largest Cluster GPS Coordinates: Latitude = {latitude}, Longitude = {longitude}, Timestamp = {timestamp}")
            remember_location(latitude, longitude, timestamp)

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
        marker.scale.x = smoothed_max_point[0] - smoothed_min_point[0]
        marker.scale.y = smoothed_max_point[1] - smoothed_min_point[1]
        marker.scale.z = smoothed_max_point[2] - smoothed_min_point[2]

        marker.color = ColorRGBA(1.0, 0.0, 0.0, 0.5)  # Red with 50% transparency

        # Publish the Marker
        marker_pub.publish(marker)

        # Publish the angle of the largest cluster's center
        angles_msg = Float32MultiArray()
        angles_msg.data.append(math.degrees(math.atan2(center_y, center_x)))
        angles_pub.publish(angles_msg)

if __name__ == "__main__":
    rospy.init_node('pointcloud_segmenter_filtered', anonymous=True)

    # Initialize TransformListener
    tf_buffer = Buffer()
    tf_listener = TransformListener(tf_buffer)

    # Initialize CSV file
    init_csv()

    rospy.Subscriber("/velodyne_points", PointCloud2, pointcloud_callback)

    marker_pub = rospy.Publisher("/bounding_box", Marker, queue_size=10)
    filtered_cloud_pub = rospy.Publisher("/filtered_velodyne_points", PointCloud2, queue_size=10)
    angles_pub = rospy.Publisher("/bounding_box_angles", Float32MultiArray, queue_size=10)  # Publish angles

    rospy.spin()
