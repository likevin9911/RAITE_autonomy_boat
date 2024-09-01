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

# process1 = subprocess.run(['roslaunch', '4WD_description', 'noise.launch'],check=True,text=True)
# process2 = subprocess.run(['ls', '-l'],check=True,text=True)
# # list_of_files = subprocess.run(['ls', '-la'], capture_output=True, text=True)
# # print(list_of_files.stdout)


def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;


# def restart_program():
#     """Restarts the current program, with file objects and descriptors
#        cleanup
#     """

#     try:
#         p = psutil.Process(os.getpid())
#         for handler in p.get_open_files() + p.connections():
#             os.close(handler.fd)
#     except Exception, e:
#         logging.error(e)

#     python = sys.executable
#     os.execl(python, python, *sys.argv)

hec = ['roslaunch', '4WD_description', 'hector.launch']
bag = ['roslaunch', '4WD_description', 'bag.launch','!']
init = ['roslaunch', '4WD_description', 'init.launch']
noi = ['roslaunch', '4WD_description', 'noise.launch']
mov_del = ['./state.py']
noi_pub = ['./node_list.py']
bags_p = ['Bag1.bag', 'Bag2.bag','Bag3.bag','Bag4.bag','Bag5.bag','Bag6.bag' ]
cp = ['rosclean','purge','-y']
kh =['ronode', 'kill','hector_mapping']
try:
   # ros_purge = subprocess.Popen(cp)
   pub_noi = subprocess.Popen(noi_pub)
   start_up = subprocess.Popen(init)
   noise = subprocess.Popen(noi)
   k = 1
   m = 0
   # # if (not checkIfProcessRunning('play')) & (not checkIfProcessRunning('hector_mapping')):
   #    print('Start Init, Noise, Hector, and Bag')
   #    # p2 = subprocess.run(bag)
   #    # p3 = subprocess.run(hec)
   #    print('Bag & Hector Playing So we are Mapping:)...')
   for j in range(6):
       play = ['rosbag', 'play', '-q','-u','30', bags_p[j], '--topics', '/scan']
       file_manager = subprocess.Popen(mov_del)
       for i in range(2):
            if k == 4 and i == 0:
                k = 1
            if i == 15 or i == 30 or i == 45:
                k += 1
            m = i-15*(k-1)
            file_manager = subprocess.Popen(mov_del)
            time.sleep(0.1)
            p = subprocess.Popen(hec)
            time.sleep(0.1)
        

            print('\n\nStarting Hector Mapping\n\n')
            # print('\n\n\n'+str((i+1)+100)+'\n\n\n')

            o = subprocess.call(play)
            time.sleep(0.1)

            print('\n\nBag Done Playing\n\n')
            words = 'mod_pc'+'_bag_'+str(j+1)+'_noi_'+str(m+15)+'H:'+str(k)
            mo = ['rosrun','map_server','map_saver','-f', words]
            l = subprocess.call(mo)
            print('\n\nDone Making '+ str(i) + ' Maps\n\n')
            time.sleep(1)
            # kill_hec = subprocess.Popen(kh)



except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
   pass


nodes = os.popen("rosnode list").readlines()
for i in range(len(nodes)):
    nodes[i] = nodes[i].replace("\n","")

for node in nodes:
    os.system("rosnode kill "+ node)

