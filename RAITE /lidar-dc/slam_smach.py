#!/usr/bin/env python3

import subprocess
import globals
from subprocess import Popen, PIPE
import atexit
import os
import random
import sys
import psutil
import logging
from datetime import datetime
import time
import rosnode
import rosgraph
import sys
import argparse
import rospy
from std_msgs.msg import *



global k

slap =  ['roslaunch', '4WD_description', 'slam.launch','!']
bag = ['roslaunch', '4WD_description', 'bag.launch','!']
init = ['roslaunch', '4WD_description', 'init.launch']
noi = ['roslaunch', '4WD_description', 'noise.launch']
mov_del = ['./state.py']
noi_pub = ['./node_list.py']
bags_p = ['Bag1.bag', 'Bag2.bag','Bag3.bag','Bag4.bag','Bag5.bag','Bag6.bag' ]
bags_slam = ['BAG1_NOMAP.bag','BAG2_NOMAP.bag','BAG13NOMAP.bag','BAG4_NOMAP.bag','BAG5_NOMAP.bag','BAG6_NOMAP.bag' ]
cp = ['rosclean','purge','-y']
kh =['rosnode', 'kill','slam_gmapping']
sla = ['rosrun', 'gmapping', 'slam_gmapping','scan:=final']
#       rosrun gmapping slam_gmapping scan:=final
ext=['./ext.py']
try:
   k = 1
   m = 0
   ros_purge = subprocess.Popen(cp)
   pub_noi = subprocess.Popen(noi_pub)
   start_up = subprocess.Popen(init)
   noise = subprocess.Popen(noi)
   for j in range(6):
       # play = ['rosbag', 'play', '-q', bags_p[j], '--topics', '/scan']
       play = ['rosbag', 'play', '-q', bags_slam[j]]

       file_manager = subprocess.Popen(mov_del)
       for i in range(60):
            if k == 4 and i == 0:
                k = 1
            if i == 15 or i == 30 or i == 45:
                k += 1
            m = i-15*(k-1)

            file_manager = subprocess.Popen(mov_del)
            time.sleep(0.1)
            # kill_hec = subprocess.Popen(kh)
            pp = subprocess.Popen(ext)

            time.sleep(0.2)
            o = subprocess.call(play)
            time.sleep(0.1)

            print('\n\nBag Done Playing\n\n')
            words = 'add_snow'+'_bag_'+str(j+1)+'_noi_'+str(int(m*100)+600)+'S:'+str(k)
            mo = ['rosrun','map_server','map_saver','-f', words]
            l = subprocess.call(mo)
            print('\n\nDone Making '+ str(i) + ' Maps\n\n')
            time.sleep(1)



except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
   pass

file_manager = subprocess.Popen(mov_del)


nodes = os.popen("rosnode list").readlines()
for i in range(len(nodes)):
    nodes[i] = nodes[i].replace("\n","")

for node in nodes:
    os.system("rosnode kill "+ node)

