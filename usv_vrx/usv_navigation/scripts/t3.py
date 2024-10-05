#!/usr/bin/env python3

import rospy
import pcl
import csv
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
from visualization_msgs.msg import Marker
import numpy as np
from std_msgs.msg import ColorRGBA, Float32MultiArray
from sensor_msgs.msg import PointField, NavSatFix, Imu
from std_msgs.msg import Header
import math
import tf
import time

# Adjustable variables
MIN_Z_HEIGHT = -1.0
MAX_Z_HEIGHT = 2.0  # Adjust this based on the expected obstacle height
FRONT_DEGREES = 40
MAX_DISTANCE = 50.0  # Maximum distance to consider points
gps_data = None
imu_data = None
global_map = []
start_time = None
csv_file = "bounding_box_log.csv"

# Mock GPS data
mock_gps_data = {
    'latitude': 47.1186,  # Mock latitude
    'longitude': -88.5473,  # Mock longitude
    'altitude': 200.0  # Mock altitude (in meters)
}

def pointcloud_callback(pointcloud_msg):
    global start_time

    # Check if 30 seconds have passed
    if time.time() - start_time >= 30:
        rospy.signal_shutdown("Time limit reached. Shutting down.")
        return

    # Clear previous markers
    marker_pub.publish(Marker(action=Marker.DELETEALL))

    point_list = list(pc2.read_points(pointcloud_msg, field_names=("x", "y", "z"), skip_nans=True))
    if not point_list:
        return

    pcl_data = pcl.PointCloud(np.array(point_list, dtype=np.float32))

    # Voxel downsampling
    pcl_data = voxel_downsampling(pcl_data)

    # Remove ground plane
    pcl_data = ground_plane_removal(pcl_data)

    # Filter points by Z height and distance
    passthrough = pcl_data.make_passthrough_filter()
    passthrough.set_filter_field_name("z")
    passthrough.set_filter_limits(MIN_Z_HEIGHT, MAX_Z_HEIGHT)
    cloud_filtered = passthrough.filter()

    front_cloud = []
    for point in cloud_filtered.to_array():
        distance = np.sqrt(point[0]**2 + point[1]**2 + point[2]**2)
        angle = math.degrees(math.atan2(point[1], point[0]))
        if -FRONT_DEGREES / 2 <= angle <= FRONT_DEGREES / 2 and distance <= MAX_DISTANCE:
            front_cloud.append(point)

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

    if len(front_cloud) > 0:
        pcl_front_cloud = pcl.PointCloud(np.array(front_cloud, dtype=np.float32))

        # Clustering
        cluster_indices = cluster_extraction(pcl_front_cloud)

        marker_id = 0
        angles_msg = Float32MultiArray()

        for i, indices in enumerate(cluster_indices):
            points = []
            for index in indices:
                points.append([pcl_front_cloud[index][0], pcl_front_cloud[index][1], pcl_front_cloud[index][2]])

            points_array = np.array(points)
            min_point = points_array.min(axis=0)
            max_point = points_array.max(axis=0)

            center_x = (min_point[0] + max_point[0]) / 2.0
            center_y = (min_point[1] + max_point[1]) / 2.0
            center_z = (min_point[2] + max_point[2]) / 2.0
            center_angle = math.degrees(math.atan2(center_y, center_x))
            center_distance = math.sqrt(center_x**2 + center_y**2 + center_z**2)

            # Use mock GPS data to convert to GPS coordinates
            gps_coords = convert_to_gps(center_x, center_y, center_z)

            # Store in global map
            global_map.append(gps_coords)

            # Print the global map entry for the first bounding box
            if i == 0:
                print(f"Global Map Entry for Bounding Box 0: {global_map[-1]}")

            # Log data to CSV file
            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([rospy.Time.now(), center_x, center_y, center_z, center_angle, center_distance, gps_coords[0], gps_coords[1], gps_coords[2]])

            # Create bounding box marker
            marker = Marker()
            marker.header.frame_id = pointcloud_msg.header.frame_id
            marker.header.stamp = rospy.Time.now()
            marker.ns = "velodyne"
            marker.id = marker_id
            marker.type = Marker.CUBE
            marker.action = Marker.ADD
            marker.pose.position.x = center_x
            marker.pose.position.y = center_y
            marker.pose.position.z = center_z
            marker.scale.x = max_point[0] - min_point[0]
            marker.scale.y = max_point[1] - min_point[1]
            marker.scale.z = max_point[2] - min_point[2]
            marker.color = ColorRGBA(1.0, 0.0, 0.0, 0.5)
            marker_pub.publish(marker)
            marker_id += 1

        angles_pub.publish(angles_msg)

def voxel_downsampling(point_cloud, leaf_size=0.1):
    sor = point_cloud.make_voxel_grid_filter()
    sor.set_leaf_size(leaf_size, leaf_size, leaf_size)
    return sor.filter()

def ground_plane_removal(point_cloud):
    seg = point_cloud.make_segmenter()
    seg.set_model_type(pcl.SACMODEL_PLANE)
    seg.set_method_type(pcl.SAC_RANSAC)
    seg.set_distance_threshold(0.01)
    indices, coefficients = seg.segment()
    return point_cloud.extract(indices, negative=True)

def cluster_extraction(point_cloud):
    tree = point_cloud.make_kdtree()
    ec = point_cloud.make_EuclideanClusterExtraction()
    ec.set_ClusterTolerance(0.5)
    ec.set_MinClusterSize(30)
    ec.set_MaxClusterSize(15000)
    ec.set_SearchMethod(tree)
    return ec.Extract()

def convert_to_gps(x, y, z):
    # Convert local coordinates to global GPS coordinates using mock GPS data
    gps_lat = mock_gps_data['latitude'] + (x / 100000.0)  # Conversion factor should be based on real calibration
    gps_lon = mock_gps_data['longitude'] + (y / 100000.0)
    gps_alt = mock_gps_data['altitude'] + z  # z is usually the altitude difference

    return gps_lat, gps_lon, gps_alt

if __name__ == "__main__":
    # Initialize CSV file and write headers
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Center_X", "Center_Y", "Center_Z", "Center_Angle", "Center_Distance", "GPS_Latitude", "GPS_Longitude", "GPS_Altitude"])

    rospy.init_node('pointcloud_segmenter_filtered', anonymous=True)
    rospy.Subscriber("/velodyne_points", PointCloud2, pointcloud_callback)

    marker_pub = rospy.Publisher("/bounding_box", Marker, queue_size=10)
    filtered_cloud_pub = rospy.Publisher("/filtered_velodyne_points", PointCloud2, queue_size=10)
    angles_pub = rospy.Publisher("/bounding_box_angles", Float32MultiArray, queue_size=10)
    RANSAC_pub = rospy.Publisher('/ransac_output', PointCloud2, queue_size=10)

    # Start timer
    start_time = time.time()
    
    rospy.spin()
