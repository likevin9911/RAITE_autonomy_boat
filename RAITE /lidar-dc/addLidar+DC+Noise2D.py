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
import std_msgs.msg
from std_msgs import *
from std_msgs.msg import Float32
import tf2_ros
import tf2_geometry_msgs
import geometry_msgs.msg
import threading
global my_data
my_data = 0

num = 0 # number of points to add
funk = 0
# Define the desired topics to subscribe/publish
subscriber_topic = '/velodyne_points'
#subscriber_topic = '/velodyne_points_filtered'

#subscriber_topic = '/wamv/sensors/lidars/lidar_wamv/points'

publisher_topic = '/noisyLidar'

# This defines the topic to which the node publishes
pub = rospy.Publisher(publisher_topic, PointCloud2, queue_size=0)



global movingcenter
global lastSample
lastSample = np.array([0])
movingcenter = (5.0, -3.0, 2.0)



def SCpdf(W,vx): # done

    # make a discretized cube centered on the origin of width W meters, and with vx voxels per dimension
    #W = 4
    #vx = 100
    
    # Compute filter kernel with radius correlation_scale (can probably be a bit smaller)
    correlation_scale = 5 # units are meters
    x = np.linspace(-W/2, W/2, vx)
    y = np.linspace(-W/2, W/2, vx)
    X, Y = np.meshgrid(x, y)
    dist = np.sqrt(X*X + Y*Y)
    filter_kernel = np.exp(-dist**2/(2*correlation_scale))

    #print(x.size)
    #print(X.size)
    #print(x)
    #print(X)

    # Generate n-by-n grid of spatially correlated noise
    n = x.size
    noise = np.random.randn(n, n)
    noise = scipy.signal.fftconvolve(noise, filter_kernel, mode='same')
    return noise,X,Y,x,y
    # don't run below for n>>5
    #for a in range(n):
    #    plt.figure()
    #    plt.imshow(noise[a,:,:])
    
def add_clouds_grid(msg): # blobs
    global my_data
    noise,X,Y,x,y = SCpdf(W=20, vx=int(my_data))
    # remap noise to [0,100] to represent lidar intensitites
    lidar_intensities = np.interp(noise, (noise.min(), noise.max()), (0, 100))
    
    #Threshold lidar intensitites
    #thresh = 80
    thresh = 98
    lidar_intensities[lidar_intensities < thresh] = 0
    
    # clip important chunks from spatial coordinates
    nX = X[lidar_intensities > 0]
    nY = Y[lidar_intensities > 0]
    lid_int = lidar_intensities[lidar_intensities > 0]
    # print(nX.shape)
    # print(nY.shape)
    # print(lid_int.shape)
    # print("adding this many points: ",nX.size)
    for ind in range(nX.size):
        packmsg(msg,nX[ind],nY[ind],0)



def add_snow(msg): # done
    global my_data
    # This function adds random points to the point cloud
    # The points added are drawn from a uniform distribution
    # The variables xs and ys control the area of space the noise inhabits
    # The variable num indicates the number of points to add
    xs=(-1, 1)
    ys=(-1, 1)
    zs=(-1, 1)

    num = my_data       
    for _ in range(int(num)):
        x = random.uniform(*xs)
        y = random.uniform(*ys)
        z = random.uniform(*zs)
        packmsg(msg,x,y,z)
        
def add_local_snow(msg): # done
    global my_data
    num = int(my_data)
    # This function adds random points to the point cloud near a particular location
    # Like a swarm of mosquitoes
    # The points added are drawn from a normal distribution
    # The variable num indicates the number of points to add
    
    center = [-2,0] # center of the swarm, in the robot frame (the swarm will move with the robot)
    width = [[3, 3],[3, 3]] # size of swarm
    
    pts = np.random.multivariate_normal(mean=center, cov=width, size=num)
    
    for row in pts:
        (x,y) = row
        packmsg(msg,x,y,0)

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
    global my_data # Max = 0.65
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

# def noise_itterator():
#     start_time = time.time()
#     val = (time.time() - start_time)
#     ys=(-val, val)
#     xs=(-val, val)

#     return ys,xs


def mod_pc_local(msg):
    global my_data
    # This function extracts data from the pointcloud message and adds noise to a local area
    # define center of 'local'
    xc = 0
    yc = 0
    R = 35 # radius of 'local'
    
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

# def del_pc_local(msg): # done
#     global my_data
#     # This function deletes points within a local area
#     # define center of 'local'
#     xc = 0
#     yc = 0
#     R = my_data # radius of 'local'

#     newdata = b''

#     for aa in range(len(msg.data)):
#         #xyz_array = ros_numpy.point_cloud2.pointcloud2_to_xyz_array(msg)


#         if len(msg.data[aa*msg.point_step:aa*msg.point_step+msg.point_step]) != 0:
            
#             # The format '<4fHf' has been validated only for /velodyne_points topic
#             # Airsim may be different
#             dataIn = struct.unpack('<4fI',msg.data[aa*msg.point_step:aa*msg.point_step+msg.point_step])
            
#             if ( pow(dataIn[0] - xc, 2) + pow(dataIn[1] - yc, 2) ) > R**R:
#                 binary = struct.pack('<4fI', dataIn[0], dataIn[1], dataIn[2], 50, 0)
#                 for b in binary:
#                     newdata = newdata + b.to_bytes(length=1, byteorder='little')
#     msg.data = newdata


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



#python2
# def packmsg(msg, x, y, z):
#     binary = struct.pack('<3f', x, y, z)
#     for b in binary:
#         msg.data = msg.data + chr(ord(b))


#Python3
def packmsg(msg, x, y, z): # done
    binary = struct.pack('<3f', x, y, z)
    for b in binary:
        msg.data = msg.data + b.to_bytes(length=1, byteorder='little')

#def packmsg(msg, x, y, z): # done
#    binary = struct.pack('<4fI', x, y, z,50,0)
#    for b in binary:
#        msg.data = msg.data + b.to_bytes(length=1, byteorder='little')



def callback(msg):
    # print("Took seconds: ")
    # noise_itterator()
    # temp = time.time()

    #add_snow(msg) # add fake returns generated uniformly, can change sample space within function
    # add_local_snow(msg) # add a swarm of mosquitoes, can change size/loc within function
    # add_moving_snow(msg) # same as add_local_snow, but the center of the swarm is a random walk

    #add_clouds_grid(msg) # adds points generated from a spatially correlated PDF, sampled on a regular grid
    # add_clouds(msg) # adds points generated from a spatially correlated PDF without a regular grid
    
    #mod_pc(msg) # adds noise to every point in the lidar scan
    #mod_pc_local(msg) # adds noise to every point within some local neighborhood (defined in function)
    #del_pc_local(msg) # deletes points within some local neighborhood
    

    pub.publish(msg)
    # print("Took seconds: ", (time.time()-temp))


def callback2(data):
    global my_data
    my_data = data.data
    rospy.loginfo_throttle(2,"Noise Level Subscribed            %s",my_data)

def listener():
    rospy.init_node('interceptLidar', anonymous=False)
    #queue_size = rospy.get_param('~queue_size', 0)
    # This defines which topic the node subscribes to.
    # '/velodyne_points' works for Mizzou's bagged data (and presumably nodes published by a Velodyne lidar)
    rospy.Subscriber(subscriber_topic, PointCloud2, callback, queue_size=5)
    rospy.Subscriber('Noise_LEVEL',Float32,callback2, queue_size=10)


    #print ("Subscribed to ", subscriber_topic)
    print("Publishing to " + publisher_topic)
    spin_rate = rospy.Rate(30)  # Set to the desired loop rate (in Hz)


    rospy.spin()




if __name__ == '__main__':
    try :
        listener()
    except rospy.ROSInterruptException:
        pass
