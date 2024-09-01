#!/usr/bin/env python3

import subprocess
from subprocess import Popen, PIPE
import os
import time
import rosnode
import rosgraph
import argparse
import rospy
from std_msgs.msg import *
import psutil

# pc = ['rosparam', 'set', 'use_sim_time', 'true','&&','roslaunch', 'hdl_graph_slam', 'hdl_graph_slam_501.launch']
# noi = ['roslaunch', '4WD_description', 'noise.launch']


nodes_to_exclude = ['/noise_chatter', '/interceptLidar', '/rosout', '/rviz_floam_mapping']

def get_all_ros_nodes():
    try:
        output = subprocess.check_output(['rosnode', 'list'])
        active_nodes = output.decode('utf-8').split('\n')[:-1]  # Remove the last empty item
        return active_nodes
    except subprocess.CalledProcessError:
        return []

global k

pc_m = 'roslaunch lidar_camera_fusion vlp16OnImg_offline.launch > /dev/null 2>&1'
pc_i = 'roslaunch lidar_camera_fusion interpolated_vlp16.launch > /dev/null 2>&1'


fl = 'roslaunch floam floam.launch > /dev/null 2>&1'
flm = 'roslaunch floam floam_mapping.launch > /dev/null 2>&1'

#noi = ['python3','./addLidar+DC+Noise2D.py']
noi = ['./addLidar+DC+Noise2D.py']

noi_pub = ['./node_list_dcl.py']
rvi = ['rviz', '-d', 'floam_mapping.rviz', '__anonymous:=false', '__name:=rviz_floam_mapping']

cp = ['rosclean', 'purge', '-y']
k_all_nodes = ['rosnode', 'kill', 'interpolated_node', '/word2map_tf','/gt/trajectory_server_loam', '/floam_odom_estimation_node', '/floam_laser_processing_node', '/floam_laser_mapping_node','/base_link/trajectory_server_loam']


bags = ['camera_lidar2.bag']
#bags = ['camera_lidar1.bag']
#bags = ['Parking_Lot+1.bag', 'Parking_Lot+2.bag', 'Parking_Lot+3.bag', 'Parking_Lot+4.bag', 'Parking_Lot+5.bag']


ks = ['rosnode', 'kill', '/map_saver']
tim = ['rosparam', 'set', 'use_sim_time', 'true']
mo = ['rosrun', 'map_server', 'map_saver']
state = ['./state.py']



try:
    k = 1
    m = 0
    tim = subprocess.Popen(tim)
    rviz = subprocess.Popen(rvi)
    pub_noi1 = subprocess.Popen(noi_pub)
    noi1 = subprocess.Popen(noi)


    for j in range(1):
        ros_purge = subprocess.Popen(cp)
        #play = ['rosbag', 'play', '--clock', '-q', bags[j], '-u', '10', '--topics', '/velodyne_points', '/camera/color/image_raw']
        play = ['rosbag', 'play', '--clock', '-q', bags[j], '--topics', '/velodyne_points', '/camera/color/image_raw']

        for i in range(60):
            if k == 4 and i == 0:
                k = 1
            if i == 15 or i == 30 or i == 45:
                k += 1
            m = i - 15 * (k - 1)


            # Run Lidar Depth Camera Merge/Interpo
            lidar_dc_interpol = subprocess.Popen(pc_i, shell=True)
            #subprocess.Popen(pc_m, shell=True)
            time.sleep(2)
            # Run Floam/Mapping
            floam_mapping = subprocess.Popen(flm, shell=True)
            #subprocess.Popen(fl, shell=True)


            #filename = 'mod_pc_local'+'_bag_'+str(j+1)+'_noi_'+f"{m*0.25+0.25:.3f}"+'_(xc=0,yc=0,R=35)_'+'PC_'+str(k)+'.pcd'
            #filename = 'mod_pc'+'_bag_'+str(j+1)+'_noi_'+f"{m*0.05+0.05:.3f}"+'_(x,y,z=Nosie:-x,-y,-z=Nosie)_'+'PC_'+str(k)+'.pcd'
            #filename = 'add_clouds_grid'+'_bag_'+str(j+1)+'_noi_'+str(int(m*20)+280)+'_(W=20, vx=Nosie)_'+'PC_'+str(k)+'.pcd'
            filename = 'dcl_'+'bag_'+str(j+1)+'_noi_'+str(int(m*150)+100)+'_X(-1,1)Y(-1,1)_'+'PC_'+str(k)
            #filename = 'add_snow_local'+'_bag_'+str(j+1)+'_noi_'+str(int(m*100)+1000)+'Width_X(3,3)Y(3,3)_'+'Center_(-2,0)'+'PC_'+str(k)+'.pcd'

            #sav = f'''rosservice call /hdl_graph_slam/save_map "{{resolution: 0.05, destination: '/home/sinloops/lidar-dc/Noisy_Images/{filename}'}}"'''
 #          rosrun pcl_ros pointcloud_to_pcd input:=/map _prefix:=/home/sinloops/lidar-dc/dcl_

            #sav = ['rosrun', 'pcl_ros', 'pointcloud_to_pcd', 'input:=/map', '_prefix:='+filename]
            #sav = ['rosrun', 'pcl_ros', 'pointcloud_to_pcd', 'input:=/map', '_prefix:=/home/sinloops/lidar-dc/' + filename, '> /dev/null 2>&1']\
            print('\n\nDebug SAVE\n\n')
            sav = ['rosrun', 'pcl_ros', 'pointcloud_to_pcd', f'input:=/map', f'_prefix:={filename}']


            time.sleep(0.5)
            msav = subprocess.Popen(sav)
            subprocess.call(play)  # this needs to run until complete before moving onto the next line of code
            print('\n\nDebug Before Killed All Nodes\n\n')
            time.sleep(1)

            #kan = subprocess.Popen(k_all_nodes)
            k_all_nodes = get_all_ros_nodes()
            filtered_nodes = ["rosnode", "kill"] + [node for node in k_all_nodes if node not in nodes_to_exclude]
            kan = subprocess.Popen(filtered_nodes)


            print('\n\nDebug After Killed All Nodes\n\n')
            time.sleep(1)
            print('\n\nKilled All Nodes\n\n')
            print('\n\nBag Done Playing\n\n')

            time.sleep(0.5)
            subprocess.Popen(mo)
            time.sleep(1)
            subprocess.call(ks)
            time.sleep(0.5)

            subprocess.Popen(state)
            time.sleep(0.5)



            print('\n\nDone Making '+ str(i+1) + ' Maps\n\n')
            time.sleep(1)

except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
    pass

nodes = os.popen("rosnode list").readlines()
for i in range(len(nodes)):
    nodes[i] = nodes[i].replace("\n", "")

for node in nodes:
    if node != "/rosout":
        os.system("rosnode kill "+ node)