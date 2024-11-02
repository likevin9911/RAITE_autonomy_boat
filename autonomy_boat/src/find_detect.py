#!/usr/bin/env python3
import cv2 as cv
import numpy as np
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image, Imu
from std_msgs.msg import Bool
from geometry_msgs.msg import PoseStamped, Twist
import subprocess  # For killing nodes
import threading    # For handling the stop sequence without blocking

class Segmentation:
    
    def __init__(self):
        ''' Initialize environment '''
        print("Initializing Segmentation node...")

        # Initialize other variables first
        self.bridge = CvBridge()
        self.image = None
        self.stopping = None
        self.angular_velocity = None  # IMU angular velocity feedback
        self.linear_acceleration = None  # IMU linear acceleration feedback
        self.last_doll_position = None  # To remember last known position

        # Initialize phase before setting up subscribers
        self.phase = "exploring"  # Initial phase: Exploring
        print(f"Initial phase set to: {self.phase}")

        # Initialize Publishers
        self.image_pub = rospy.Publisher("/image_detection", Image, queue_size=10)
        self.doll_detected_pub = rospy.Publisher("/doll_detected", Bool, queue_size=10)
        self.goal_pub = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=10)
        self.cmd_vel_pub = rospy.Publisher("/cmd_vel_adjusted", Twist, queue_size=10)

        # Initialize Subscribers
        self.image_sub = rospy.Subscriber("/camera/color/image_raw", Image, self.image_callback)
        self.imu_sub = rospy.Subscriber("/imu/zeroed_data", Imu, self.imu_callback)

        print("Publishers and subscribers initialized.")

        # Load YOLO model
        print("Loading YOLO model...")
        try:
            self.net = cv.dnn.readNet(
                "/home/lab/catkin_ws/src/autonomy_boat/config/test3.weights",
                "/home/lab/catkin_ws/src/autonomy_boat/config/test3.cfg"
            )
            print("YOLO model loaded successfully.")
        except Exception as e:
            print(f"Error loading YOLO model: {e}")

        try:
            with open("/home/lab/catkin_ws/src/autonomy_boat/config/test3.names", "r") as f:
                self.classes = [line.strip() for line in f.readlines()]
            print("Class names loaded successfully.")
        except Exception as e:
            print(f"Error loading class names: {e}")
            self.classes = []

        self.layer_names = self.net.getLayerNames()
        self.outputlayers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
        print("YOLO output layers obtained.")

        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
        print("Color mapping for classes initialized.")

        # Initialize stopping flag
        self.stopping = False  # To ensure stop sequence is triggered only once

    def image_callback(self, data):
        if self.stopping:
            # If stopping, ignore further image processing
            return
        try:
            self.image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(f"CvBridge Error: {e}")
            return
        self.image_processing()

    def imu_callback(self, data):
        if self.stopping:
            # If stopping, ignore IMU data
            return
        self.angular_velocity = abs(data.angular_velocity.z)
        self.linear_acceleration = abs(data.linear_acceleration.x)
        # Uncomment the next line for minimal IMU feedback
        # print(f"IMU Data - Angular Velocity: {self.angular_velocity}, Linear Acceleration: {self.linear_acceleration}")

    def image_processing(self):
        ''' Process the image and detect objects '''
        if self.image is None:
            # Avoid processing when there's no image
            return

        # Print phase information only when phase changes or significant events occur
        if self.phase == "exploring":
            rospy.loginfo_throttle(5, f"Phase: {self.phase} - Searching for dolls.")
        elif self.phase == "approaching":
            rospy.loginfo_throttle(5, f"Phase: {self.phase} - Aligning and moving towards the doll.")

        height, width = self.image.shape[:2]

        blob = cv.dnn.blobFromImage(
            self.image, 0.00392, (416, 416), (0, 0, 0), True, crop=False
        )
        self.net.setInput(blob)
        outs = self.net.forward(self.outputlayers)

        doll_detected = False
        doll_position = None
        vertical_percentage = None  # Initialize to None

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.85:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    self.draw_bounding_box(x, y, w, h, class_id, confidence)

                    if self.classes[class_id].lower() == "doll":
                        doll_detected = True
                        doll_position = (center_x, center_y)
                        self.last_doll_position = doll_position  # Update last known position
                        rospy.loginfo(f"Doll detected with confidence {confidence*100:.2f}% at position ({center_x}, {center_y}).")

                        # New vertical percentage logic
                        if center_y < height / 2:
                            vertical_percentage = 50.0  # Cap at 50% if above the center
                        else:
                            vertical_percentage = round(
                                50 - ((center_y - height / 2) / (height / 2)) * 50, 2
                            )

                        horizontal_percentage = round((center_x / width) * 100, 2)
                        rospy.loginfo(f"Doll Position - Horizontal: {horizontal_percentage}%, Vertical: {vertical_percentage}%")

        # Publish whether a doll was detected
        try:
            if not rospy.is_shutdown():
                self.doll_detected_pub.publish(Bool(data=doll_detected))
        except rospy.exceptions.ROSException as e:
            rospy.logwarn(f"Failed to publish /doll_detected: {e}")

        if doll_detected and self.phase == "exploring":
            rospy.loginfo("Doll detected! Transitioning to Approaching phase.")
            self.phase = "approaching"
            self.kill_nodes()
            # Proceed to align and approach
            self.align_and_approach(doll_position, width, vertical_percentage)
        elif doll_detected and self.phase == "approaching":
            # Continuously align and approach during the Approaching phase
            self.align_and_approach(doll_position, width, vertical_percentage)
        elif not doll_detected and self.phase == "approaching":
            rospy.logwarn("Doll lost from view. Using last known position to continue approaching.")
            if self.last_doll_position is not None:
                # Use the last known vertical_percentage or set a default
                self.align_and_approach(self.last_doll_position, width, vertical_percentage=42.08)
            else:
                rospy.logwarn("No last known position available. Stopping the boat.")
                self.stop_boat()
        # No transition back to 'exploring'

        self.publish_image_detection()
        # Removed: print("Image processing completed.")

    def draw_bounding_box(self, x, y, w, h, class_id, confidence):
        ''' Draw a bounding box around the detected object '''
        color = self.colors[class_id]
        label = f"{self.classes[class_id]}: {round(confidence, 2)}"
        cv.rectangle(self.image, (x, y), (x + w, y + h), color, 2)
        cv.putText(self.image, label, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        # Optionally, print bounding box info
        # rospy.loginfo(f"Bounding box drawn for {self.classes[class_id]} at ({x}, {y}, {w}, {h}).")

    def align_and_approach(self, doll_position, frame_width, vertical_percentage):
        ''' Align the boat with the doll and move towards it '''
        rospy.loginfo("Approaching the doll...")
        center_x, center_y = doll_position
        tolerance = frame_width * 0.1  # 10% tolerance

        # Calculate angular velocity to align the doll to the center
        angular_z = 0.0
        if abs(center_x - frame_width / 2) > tolerance:
            angular_z = 0.2 if center_x < frame_width / 2 else -0.2
            rospy.loginfo(f"Rotating to align with doll. Angular Velocity set to: {angular_z}")
        else:
            rospy.loginfo("Boat is aligned with the doll. No rotation needed.")

        # Calculate linear velocity to approach the doll
        linear_x = 0.0
        if vertical_percentage > 25:
            linear_x = 0.2  # Move towards the doll
            rospy.loginfo(f"Approaching doll. Linear Velocity set to: {linear_x}")
        else:
            if not self.stopping:
                rospy.loginfo(f"Doll below vertical threshold ({vertical_percentage}%). Initiating stop sequence.")
                self.stopping = True
                # Start the stop sequence in a separate thread to avoid blocking
                threading.Thread(target=self.stop_sequence).start()
            # Optionally, maintain current velocities or take other actions
            return  # Exit the method to prevent further velocity commands

        # Publish both linear and angular velocities
        twist = Twist()
        twist.linear.x = linear_x
        twist.angular.z = angular_z
        try:
            if not rospy.is_shutdown():
                self.cmd_vel_pub.publish(twist)
                rospy.loginfo(f"Set Velocities -> Linear: {twist.linear.x}, Angular: {twist.angular.z}")
        except rospy.exceptions.ROSException as e:
            rospy.logwarn(f"Failed to publish /cmd_vel_adjusted: {e}")

    def stop_sequence(self):
        ''' Handle the stopping sequence: reverse, wait, stop, and shutdown '''
        try:
            # Step 1: Set linear velocity to -0.2 (reverse)
            rospy.loginfo("Reversing the boat. Setting linear velocity to -0.2.")
            twist = Twist()
            twist.linear.x = -0.2
            twist.angular.z = 0.0
            self.cmd_vel_pub.publish(twist)

            # Step 2: Wait for 2 seconds
            rospy.loginfo("Reversing for 2 seconds.")
            rospy.sleep(5)

            # Step 3: Stop the boat by setting velocities to zero
            rospy.loginfo("Stopping the boat. Setting velocities to zero.")
            self.stop_boat()

            # Step 4: Unregister subscribers to prevent further callbacks
            rospy.loginfo("Unregistering subscribers to prevent further callbacks.")
            self.image_sub.unregister()
            self.imu_sub.unregister()

            # Step 5: Shutdown the node
            rospy.loginfo("Stopping ROS node as stop sequence is complete.")
            rospy.signal_shutdown("Stop sequence executed successfully.")
        except Exception as e:
            rospy.logerr(f"Error during stop sequence: {e}")

    def stop_boat(self):
        ''' Stop the boat by publishing zero velocities '''
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        try:
            if not rospy.is_shutdown():
                self.cmd_vel_pub.publish(twist)
                rospy.loginfo("Boat has been stopped by publishing zero Twist.")
        except rospy.exceptions.ROSException as e:
            rospy.logwarn(f"Failed to publish stop Twist: {e}")

    def publish_image_detection(self):
        ''' Publish the processed image to /image_detection topic '''
        if self.image is not None:
            try:
                if not rospy.is_shutdown():
                    image_msg = self.bridge.cv2_to_imgmsg(self.image, "bgr8")
                    self.image_pub.publish(image_msg)
            except CvBridgeError as e:
                rospy.logerr(f"Failed to convert image: {e}")
            except rospy.exceptions.ROSException as e:
                rospy.logwarn(f"Failed to publish /image_detection: {e}")
        else:
            rospy.logwarn("No image available to publish.")

    def kill_nodes(self):
        ''' Stop both exploration and PID controller nodes '''
        if self.phase == "exploring":
            rospy.loginfo("Killing exploration and PID controller nodes...")
            try:
                subprocess.call(['rosnode', 'kill', '/jackal_explore_node'])
                rospy.loginfo("Killed node: /jackal_explore_node")
                
                subprocess.call(['rosnode', 'kill', '/boat_pid_controller'])
                rospy.loginfo("Killed node: /boat_pid_controller")

                # Initialize cmd_vel to zero immediately after killing nodes
                twist = Twist()
                twist.linear.x = 0.0
                twist.angular.z = 0.0
                self.cmd_vel_pub.publish(twist)
                rospy.loginfo("Published zero Twist message to /cmd_vel_adjusted.")
            except Exception as e:
                rospy.logerr(f"Failed to kill nodes: {e}")
        else:
            rospy.logwarn("kill_nodes called, but current phase is not 'exploring'.")

def main():
    rospy.init_node("instance_segmentation", log_level=rospy.INFO)  # Set higher log level to see info logs
    rospy.loginfo("Instance Segmentation node started.")
    segmentation = Segmentation()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.loginfo("Instance Segmentation node interrupted and is shutting down.")
    finally:
        # Ensure that the boat is stopped if the node is interrupted
        if not segmentation.stopping:
            segmentation.stop_boat()

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        rospy.loginfo("Instance Segmentation node interrupted and is shutting down.")
