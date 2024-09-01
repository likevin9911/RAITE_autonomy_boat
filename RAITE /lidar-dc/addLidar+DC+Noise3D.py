#!/usr/bin/env python3

## I'm using this script to develop types of noise for lidar-based experiments
## This uses Mizzou's first bag file, but will be adapted to Airsim whenever that gets going

import rospy, random, struct, time
import numpy as np
from sensor_msgs.msg import PointCloud2
import scipy.signal
import scipy.interpolate as spi
import matplotlib.pyplot as plt
import psutil
import sub
from sub import *
import std_msgs.msg
from std_msgs import *
from std_msgs.msg import Float32
import tf2_ros
import tf2_geometry_msgs
import geometry_msgs.msg
import threading
global my_data
my_data = 0
movingcenter = (1.0, -1.0,1.0)

num = 0 # number of points to add
funk = 0
# Define the desired topics to subscribe/publish
subscriber_topic = '/velodyne_points'
publisher_topic = '/noisyLidar'

# This defines the topic to which the node publishes
pub = rospy.Publisher(publisher_topic, PointCloud2, queue_size=0)


def add_moving_snow(msg):
    global movingcenter, my_data
    num = int(my_data)  # Number of snow points to add

    # Update moving center, including z dimension
    movingcenter += np.random.multivariate_normal(mean=[0, 0, 0], cov=[[0.1, 0, 0], [0, 0.03, 0], [0, 0, 0.05]])

    # Generate snow points, now including z
    width = [[0.5, 0.0, 0.0], [0.0, 0.5, 0.0], [0.0, 0.0, 0.5]]  # Covariance for snow points in x, y, z
    pts = np.random.multivariate_normal(mean=movingcenter, cov=width, size=num)

    newdata_parts = []

    # Process existing points
    num_existing_points = len(msg.data) // msg.point_step
    for aa in range(num_existing_points):
        offset = aa * msg.point_step
        dataIn = struct.unpack('<4fHf', msg.data[offset:offset + msg.point_step])
        newdata_parts.append(struct.pack('<4fHf', *dataIn))

    # Add new snow points, including z
    for x, y, z in pts:
        # Assuming default values for the additional fields of the new points
        binary = struct.pack('<4fHf', x, y, z, 0, 0, 0)  # Adjust these values as needed
        newdata_parts.append(binary)

    # Update the msg data with existing + new snow points
    msg.data = b''.join(newdata_parts)




def mod_pc(msg):
    global my_data # Max = 0.78
    # Extract noise factor
    fs = my_data
    # Calculate the correct number of points
    num_points = len(msg.data) // msg.point_step

    # Generate noise for each dimension for all points
    xnoise = np.random.uniform(-fs, fs, num_points)
    ynoise = np.random.uniform(-fs, fs, num_points)
    znoise = np.random.uniform(-fs, fs, num_points)

    newdata_parts = []

    for aa in range(num_points):
        # Calculate byte offset for the current point
        offset = aa * msg.point_step
        # Unpack current point data
        dataIn = struct.unpack('<4fHf', msg.data[offset:offset + msg.point_step])

        # Add noise to the x, y, z dimensions
        x = dataIn[0] + xnoise[aa]
        y = dataIn[1] + ynoise[aa]
        z = dataIn[2] + znoise[aa]

        # Repack the point with noise added
        binary = struct.pack('<4fHf', x, y, z, dataIn[3], dataIn[4], dataIn[5])
        # Collect the modified point data
        newdata_parts.append(binary)

    # Combine all modified point data into one bytes object
    msg.data = b''.join(newdata_parts)









def mod_pc_local(msg):
    global my_data
    # This function extracts data from the pointcloud message and adds noise to a local area
    # define center of 'local'
    xc = 0
    yc = 0
    R = 3 # radius of 'local'
    
    #uniform dist parameters
    xs=(-my_data, my_data)
    ys=(-my_data, my_data)
    zs=(-my_data, my_data)
    newdata = b''



    # Iterate through each point in the point cloud data
    for aa in range(len(msg.data) // msg.point_step):
        # Calculate the start and end of the current point's data
        start = aa * msg.point_step
        end = start + msg.point_step

        # Unpack the point data
        dataIn = struct.unpack('<4fHf', msg.data[start:end])

        # Check if the point is within the specified 'local' area
        if (dataIn[0] - xc)**2 + (dataIn[1] - yc)**2 < R**2:
            # Add noise to the x, y coordinates within the local area
            x = dataIn[0] + random.uniform(*xs)
            y = dataIn[1] + random.uniform(*ys)
            z = dataIn[2] + random.uniform(*zs)
        else:
            # Outside the local area, keep the original coordinates
            x, y, z = dataIn[0], dataIn[1], dataIn[2]

        # Repack the point data, including unmodified fields
        binary = struct.pack('<4fHf', x, y, z, dataIn[3], dataIn[4], dataIn[5])

        # Append the modified (or unmodified) binary data to newdata
        newdata += binary

    # Update the msg.data with the modified point cloud data
    msg.data = newdata



def del_pc_local(msg):
    global my_data
    # Define the center of the deletion sphere in the point cloud
    xc, yc, zc = 0, -2, 0  # Center coordinates of the sphere
    R = my_data  # Radius of the sphere

    newdata = b''

    # Calculate the number of points by dividing the total data length by the step size of each point
    num_points = len(msg.data) // msg.point_step

    for aa in range(num_points):
        start = aa * msg.point_step
        end = start + msg.point_step

        # Unpack the point data, assuming the format '<4fHf' where the first three floats are x, y, z
        dataIn = struct.unpack('<4fHf', msg.data[start:end])

        # Calculate the squared distance from the point to the center of the sphere
        squared_distance = (dataIn[0] - xc)**2 + (dataIn[1] - yc)**2 + (dataIn[2] - zc)**2

        # Check if the point is outside the sphere by comparing the squared distance to the squared radius
        if squared_distance > R**2:
            # If the point is outside the sphere, repack it into the new data
            binary = struct.pack('<4fHf', *dataIn)
            newdata += binary

    # Update the msg.data with the points that are outside the deletion sphere
    msg.data = newdata





def packmsg(msg, x, y, z): # done
    binary = struct.pack('<4fHf', x, y, z, dataIn[3], dataIn[4], dataIn[5])
    for b in binary:
        msg.data = msg.data + b.to_bytes(length=1, byteorder='little')

def callback(msg):
    # print("Took seconds: ")
    # noise_itterator()
    # temp = time.time()

    #add_moving_snow(msg) # same as add_local_snow, but the center of the swarm is a random walk
    
    # mod_pc(msg) # adds noise to every point in the lidar scan
    # mod_pc_local(msg) # adds noise to every point within some local neighborhood (defined in function)
    del_pc_local(msg) # deletes points within some local neighborhood
    

    pub.publish(msg)
    # print("Took seconds: ", (time.time()-temp))

def callback2(data):
    global my_data
    my_data = data.data
    rospy.loginfo_throttle(2,"Noise Level Subscribed            %s",my_data)

def listener():
    rospy.init_node('interceptLidar', anonymous=True)
    #queue_size = rospy.get_param('~queue_size', 0)
    # This defines which topic the node subscribes to.
    # '/velodyne_points' works for Mizzou's bagged data (and presumably nodes published by a Velodyne lidar)
    rospy.Subscriber(subscriber_topic, PointCloud2, callback, queue_size=5)
    rospy.Subscriber('Noise_LEVEL',Float32,callback2, queue_size=10)


    print ("Subscribed to ", subscriber_topic)
    print ("Publishing to ", publisher_topic)
    spin_rate = rospy.Rate(30)  # Set to the desired loop rate (in Hz)


    rospy.spin()




if __name__ == '__main__':
    try :
        listener()
    except rospy.ROSInterruptException:
        pass
