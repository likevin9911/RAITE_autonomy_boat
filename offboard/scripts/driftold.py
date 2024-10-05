#!/usr/bin/env python


import casadi as cs
import numpy as np
import datetime
import rospy
from sensor_msgs.msg import NavSatFix, Imu
from geometry_msgs.msg import WrenchStamped, Twist
from message_filters import Subscriber, ApproximateTimeSynchronizer

class NMPC:
    def __init__(self):
        rospy.init_node('nmpc_controller', anonymous=True)
        
        ##################### Subscribers ###############################
        # Replace Otter USV topics with MAVROS topics for Pixhawk 6X
        self.gps_subscriber = rospy.Subscriber('/mavros/global_position/global', NavSatFix, self.gps_callback)
        self.imu_subscriber = rospy.Subscriber('/mavros/imu/data', Imu, self.imu_callback)

        ##################### Time Synchronizer ###############################
        self.ts = ApproximateTimeSynchronizer([self.gps_subscriber, self.imu_subscriber], 10, 1)
        self.ts.registerCallback(self.callback)

        ##################### Publishers ###############################
        # Replace Otter USV control with MAVROS setpoint control
        self.ctrl_pub = rospy.Publisher('/mavros/setpoint_raw/attitude', Twist, queue_size=10)
        self.ctrl_errs_pub = rospy.Publisher('controller_errs', Twist, queue_size=10)  # Keeping Twist for error messages

        ##################### Get Waypoints ###############################
        self.wpt_file = rospy.get_param("~wpt_file")
        self.wpts, self.speed_d, R_switch = self.read_wpt_data(self.wpt_file)
        self.num_wpts = self.wpts.shape[1]
        self.wpt_window_size = 40
        rospy.loginfo(f'wpts: {self.num_wpts}')

        ############## Parameter and Model Definition ###############################
        self.T = 0.1
        self.H = 40

        self.xy_max = cs.inf
        self.psi_max = cs.inf
        self.u_max = 1.5
        self.v_max = 1.5
        self.r_max = cs.pi / 6
        self.tauX_max = 292  # Force limits for motors
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

    def callback(self, gps_data, imu_data):
        start = datetime.datetime.now()
        # Insert NMPC solving code here

        # Command setup and publish
        ctrl_cmd = Twist()
        ctrl_cmd.linear.x = float(self.tauX_max)  # Set desired forward thrust force
        ctrl_cmd.angular.z = float(self.tauN_max)  # Set desired yaw torque
        self.ctrl_pub.publish(ctrl_cmd)

        # Publish control errors
        err_cmd = Twist()
        err_cmd.linear.x = float(0)  # Replace with actual error for lateral control
        err_cmd.angular.z = float(0)  # Replace with actual heading error
        self.ctrl_errs_pub.publish(err_cmd)

        # Logging
        delta_t = datetime.datetime.now() - start
        rospy.loginfo(f'total:{delta_t}')

    def setup_nmpc_problem(self):
        # Define the NMPC optimization problem
        pass

    def read_wpt_data(self, wpt_file):
        # Placeholder for reading waypoint data
        return np.array([]), 0, 0

if __name__ == '__main__':
    try:
        controller = NMPC()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
