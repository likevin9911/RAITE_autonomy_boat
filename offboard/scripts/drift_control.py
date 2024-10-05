#!/usr/bin/env python

import casadi as cs
import numpy as np
import datetime
import rospy
from sensor_msgs.msg import NavSatFix, Imu
from geometry_msgs.msg import Twist, PoseStamped
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseArray
from message_filters import ApproximateTimeSynchronizer, Subscriber

class NMPC:
    def __init__(self):
        rospy.init_node('nmpc_controller', anonymous=True)
        
        ##################### Parameters ###############################
        self.goal_frame_id = rospy.get_param('~goal_frame_id', 'map')

        ##################### Subscribers ###############################
        # Subscribe to GPS and IMU topics
        self.gps_subscriber = Subscriber('/mavros/global_position/raw/fix', NavSatFix)
        self.imu_subscriber = Subscriber('/mavros/imu/data', Imu)

        # Subscribe to waypoint topics
        self.waypoint_single_sub = rospy.Subscriber('/waypoints', PoseWithCovarianceStamped, self.waypoint_single_callback)
        self.waypoint_array_sub = rospy.Subscriber('/waypoints_array', PoseArray, self.waypoint_array_callback)

        ##################### Time Synchronizer ###############################
        # Set up ApproximateTimeSynchronizer
        self.ts = ApproximateTimeSynchronizer([self.gps_subscriber, self.imu_subscriber], queue_size=10, slop=1.0)
        self.ts.registerCallback(self.callback)

        ##################### Publishers ###############################
        self.ctrl_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.ctrl_errs_pub = rospy.Publisher('controller_errs', Twist, queue_size=10)
        
        # Path publisher for RViz visualization
        self.path_pub = rospy.Publisher('/planned_path', Path, queue_size=10)
        
        # Initialize Path message
        self.path_msg = Path()
        self.path_msg.header.frame_id = self.goal_frame_id  # Set frame to 'map' or 'odom'
        self.planned_path = []  # List to hold the sequence of planned poses

        ##################### Waypoint Storage ###############################
        self.current_waypoint = None
        self.waypoints_queue = []

        ############## Parameter and Model Definition ###############################
        self.T = 0.1
        self.H = 40

        self.xy_max = cs.inf
        self.psi_max = cs.inf
        self.u_max = 1.5
        self.v_max = 1.5
        self.r_max = cs.pi / 6
        self.tauX_max = 292
        self.tauN_max = 292

        self.xy_min = -self.xy_max
        self.psi_min = -self.psi_max
        self.u_min = -self.u_max
        self.v_min = -self.v_max
        self.r_min = -self.r_max
        self.tauX_min = -self.tauX_max
        self.tauN_min = -self.tauN_max

        self.m1 = 60.5
        self.m2 = 137.5
        self.m3 = 45.265
        self.d1 = 77.554
        self.d2 = 0
        self.d3 = 45.265

        # Casadi model symbols
        x = cs.SX.sym('x')
        y = cs.SX.sym('y')
        psi = cs.SX.sym('psi')
        u = cs.SX.sym('u')
        v = cs.SX.sym('v')
        r = cs.SX.sym('r')

        self.states = cs.vertcat(x, y, psi, u, v, r)
        self.n_states = self.states.size()[0]

        tauX = cs.SX.sym('tauX')
        tauN = cs.SX.sym('tauN')

        self.controls = cs.vertcat(tauX, tauN)
        self.n_controls = self.controls.size()[0]

        # NMPC Problem setup
        self.setup_nmpc_problem()

    def gps_callback(self, gps_data):
        pass

    def imu_callback(self, imu_data):
        pass

    def waypoint_single_callback(self, waypoint_msg):
        # Handle single waypoint from PoseWithCovarianceStamped
        rospy.loginfo(f"Received single waypoint at frame: {self.goal_frame_id}")
        self.current_waypoint = waypoint_msg.pose.pose

    def waypoint_array_callback(self, waypoints_msg):
        # Handle multiple waypoints from PoseArray
        rospy.loginfo(f"Received {len(waypoints_msg.poses)} waypoints in frame: {self.goal_frame_id}")
        self.waypoints_queue = waypoints_msg.poses

    def callback(self, gps_data, imu_data):
        start = datetime.datetime.now()
        # Insert NMPC solving code here based on GPS, IMU, and waypoint data

        # Command setup and publish
        ctrl_cmd = Twist()
        ctrl_cmd.linear.x = float(self.tauX_max)  # Example control value
        ctrl_cmd.angular.z = float(self.tauN_max)  # Example yaw control
        self.ctrl_pub.publish(ctrl_cmd)

        # Publish control errors
        err_cmd = Twist()
        err_cmd.linear.x = float(0)  # Replace with actual error for lateral control
        err_cmd.angular.z = float(0)  # Replace with actual heading error
        self.ctrl_errs_pub.publish(err_cmd)

        # Update planned path
        self.update_planned_path(gps_data, imu_data)

        # Logging
        delta_t = datetime.datetime.now() - start
        rospy.loginfo(f'total:{delta_t}')

    def update_planned_path(self, gps_data, imu_data):
        # Create a new PoseStamped message for the current position
        pose_stamped = PoseStamped()
        pose_stamped.header.frame_id = self.goal_frame_id
        pose_stamped.header.stamp = rospy.Time.now()

        # Set the position and orientation (from GPS and IMU data)
        # This is a placeholder, you'll need to calculate the real position from gps_data and imu_data
        pose_stamped.pose.position.x = gps_data.latitude  # Example, replace with real calculations
        pose_stamped.pose.position.y = gps_data.longitude
        pose_stamped.pose.position.z = 0  # Assuming a 2D path for now

        # Set orientation (from IMU data)
        pose_stamped.pose.orientation = imu_data.orientation

        # Add to the path
        self.planned_path.append(pose_stamped)
        self.path_msg.poses = self.planned_path

        # Update header timestamp and publish the path
        self.path_msg.header.stamp = rospy.Time.now()
        self.path_pub.publish(self.path_msg)

    def setup_nmpc_problem(self):
        # Define the NMPC optimization problem
        pass

if __name__ == '__main__':
    try:
        controller = NMPC()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
