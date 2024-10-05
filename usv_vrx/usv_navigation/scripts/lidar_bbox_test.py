#!/usr/bin/env python3

import rospy
import pcl
from sensor_msgs.msg import PointCloud2, NavSatFix
import sensor_msgs.point_cloud2 as pc2
from visualization_msgs.msg import Marker
import numpy as np
from std_msgs.msg import ColorRGBA, Float32MultiArray
from sensor_msgs.msg import PointField
from std_msgs.msg import Header
import math
import tf2_ros
import geometry_msgs.msg
from geopy.distance import geodesic

# Adjustable variables
MIN_Z_HEIGHT = -1.0  # Set this value to your desired minimum Z height
FRONT_DEGREES = 40  # Degrees in front of the LiDAR to keep

current_gps = None
bbox_gps_storage = {}

def gps_callback(gps_msg):
    global current_gps
    current_gps = (gps_msg.latitude, gps_msg.longitude, gps_msg.altitude)

def pointcloud_callback(pointcloud_msg):
    # print("Received point cloud data")

    #wait for for gps topic
    global current_gps

    if current_gps is None:
        rospy.logwarn("No GPS data available yet.")
        return

    # Convert PointCloud2 to PCL PointCloud
    point_list = list(pc2.read_points(pointcloud_msg, field_names=("x", "y", "z"), skip_nans=True))
    if not point_list:
        # print("No points found in point cloud")
        return
   
    # print(f"Number of points in point cloud: {len(point_list)}")
    pcl_data = pcl.PointCloud(np.array(point_list, dtype=np.float32))

    # Filter points by minimum Z height
    passthrough = pcl_data.make_passthrough_filter()
    passthrough.set_filter_field_name("z")
    passthrough.set_filter_limits(MIN_Z_HEIGHT, np.max(pcl_data.to_array()[:, 2]))
    cloud_filtered = passthrough.filter()
    # print(f"Height filtering applied, remaining points: {cloud_filtered.size}")

    # Filter points within the front degrees
    front_cloud = []
    for point in cloud_filtered.to_array():
        angle = math.degrees(math.atan2(point[1], point[0]))  # Calculate angle in degrees
        if -FRONT_DEGREES / 2 <= angle <= FRONT_DEGREES / 2:
            front_cloud.append(point)

    # print(f"Front {FRONT_DEGREES} degrees points selected, remaining points: {len(front_cloud)}")

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
    # print("Published filtered point cloud with front degrees and min Z height")

    # Optional: Add clustering and bounding boxes for visualization
    if len(front_cloud) > 0:
        pcl_front_cloud = pcl.PointCloud(np.array(front_cloud, dtype=np.float32))
        tree = pcl_front_cloud.make_kdtree()

        ec = pcl_front_cloud.make_EuclideanClusterExtraction()
        ec.set_ClusterTolerance(0.3)  # Adjust as needed
        ec.set_MinClusterSize(30)  # Adjust as needed
        ec.set_MaxClusterSize(15000)  # Adjust as needed
        ec.set_SearchMethod(tree)
        cluster_indices = ec.Extract()
        # print(f"Number of clusters found: {len(cluster_indices)}")

        marker_id = 0
        angles_msg = Float32MultiArray()  # To store angles of the centers

        for indices in cluster_indices:
            points = []
            for index in indices:
                points.append([pcl_front_cloud[index][0], pcl_front_cloud[index][1], pcl_front_cloud[index][2]])

            points_array = np.array(points)
            min_point = points_array.min(axis=0)
            max_point = points_array.max(axis=0)

            # Calculate the center of the bounding box
            center_x = (min_point[0] + max_point[0]) / 2.0
            center_y = (min_point[1] + max_point[1]) / 2.0
            center_z = (min_point[2] + max_point[2]) / 2.0

            # Calculate the angle of the center point
            center_angle = math.degrees(math.atan2(center_y, center_x))

            # Calculate the distance to the center point
            center_distance = math.sqrt(center_x**2 + center_y**2 + center_z**2)

            # Print the angle and distance
            print(f"Center angle: {center_angle:.2f} degrees, Distance: {center_distance:.2f} meters")

            #transform to baselink:
            try:
                transform = tf_buffer.lookup_transform('base_link', pointcloud_msg.header.frame_id, rospy.Time(0))
                point_in_velodyne = geometry_msgs.msg.PoseStamped()
                point_in_velodyne.header.frame_id = pointcloud_msg.header.frame_id
                point_in_velodyne.pose.position.x = center_x
                point_in_velodyne.pose.position.y = center_y
                point_in_velodyne.pose.position.z = center_z
                point_in_base_link = tf2_geometry_msgs.do_transform_pose(point_in_velodyne, transform)
                base_link_x = point_in_base_link.pose.position.x
                base_link_y = point_in_base_link.pose.position.y
                base_link_z = point_in_base_link.pose.position.z

                # Convert to GPS using the latest GPS data
                north_offset = base_link_x
                east_offset = base_link_y
                new_gps = geodesic(meters=north_offset).destination(current_gps, 0)  # 0 degrees is north
                new_gps = geodesic(meters=east_offset).destination(new_gps, 90)  # 90 degrees is east
                bbox_gps_coordinates = (new_gps.latitude, new_gps.longitude)

                # Store GPS coordinates and angle
                bbox_gps_storage[marker_id] = {
                    'gps_coordinates': bbox_gps_coordinates,
                    'angle': center_angle  # Store the angle or convert to a heading if needed
                }
                print(f"Stored GPS coordinates for bbox {marker_id}: {bbox_gps_storage[marker_id]}")

            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                rospy.logerr("TF transform lookup failed")
                return

            angles_msg.data.append(center_angle)  # Store the angle in the message

            # Create a Marker for each cluster's bounding box
            marker = Marker()
            marker.header.frame_id = pointcloud_msg.header.frame_id
            marker.header.stamp = rospy.Time.now()
            marker.ns = "velodyne"
            marker.id = marker_id
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
            # print(f"Published marker {marker_id}")

            marker_id += 1

        # Publish the angles of the cluster centers
        angles_pub.publish(angles_msg)
        # print("Published angles of cluster centers")

if __name__ == "__main__":
    rospy.init_node('pointcloud_segmenter_filtered', anonymous=True)

    #initialize tf listener and memory
    tf_buffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tf_buffer)
    bbox_gps_storage = {}

    #subscribe to gps topic
    rospy.Subscriber("/gps/fix", NavSatFix, gps_callback)

    rospy.Subscriber("/velodyne_points", PointCloud2, pointcloud_callback)
    marker_pub = rospy.Publisher("/bounding_box", Marker, queue_size=10)
    filtered_cloud_pub = rospy.Publisher("/filtered_velodyne_points", PointCloud2, queue_size=10)
    angles_pub = rospy.Publisher("/bounding_box_angles", Float32MultiArray, queue_size=10)  # Publish angles

    rospy.spin()