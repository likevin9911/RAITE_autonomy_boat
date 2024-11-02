#!/usr/bin/env python3
import cv2 as cv
import numpy as np
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image, Imu
from std_msgs.msg import Bool, Int32
from geometry_msgs.msg import PoseStamped, Twist
import subprocess  # For killing nodes

class Segmentation:
   
    def __init__(self):
        ''' Initialize environment '''
        print("Initializing Segmentation node...")

        # Initialize Publishers
        self.image_pub = rospy.Publisher("/image_detection", Image, queue_size=10)
        self.doll_detected_pub = rospy.Publisher("/doll_detected", Bool, queue_size=10)
        self.goal_pub = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=10)
        self.cmd_vel_pub = rospy.Publisher("/cmd_vel_adjusted", Twist, queue_size=10)
        
        # Initialize PWM Publishers
        self.pwm_left_pub = rospy.Publisher("/pwm_left", Int32, queue_size=10)
        self.pwm_right_pub = rospy.Publisher("/pwm_right", Int32, queue_size=10)

        # Initialize Subscribers
        rospy.Subscriber("/camera/color/image_raw", Image, self.image_callback)
        rospy.Subscriber("/imu/zeroed_data", Imu, self.imu_callback)

        print("Publishers and subscribers initialized.")

        # Initialize other variables
        self.bridge = CvBridge()
        self.image = None
        self.angular_velocity = None  # IMU angular velocity feedback
        self.linear_acceleration = None  # IMU linear acceleration feedback

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

        self.phase = "exploring"  # Initial phase: Exploring
        print(f"Initial phase set to: {self.phase}")

        # Define motor parameters for PWM conversion
        self.max_pwm = 255        # Maximum PWM value
        self.min_pwm = -255       # Minimum PWM value (for reverse)
        self.max_linear_vel = 1.0 # Maximum linear velocity (m/s)
        self.max_angular_vel = 1.0 # Maximum angular velocity (rad/s)
        self.wheel_base = 0.5     # Distance between wheels (meters)

    def image_callback(self, data):
        try:
            self.image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(f"CvBridge Error: {e}")
            return
        self.image_processing()

    def imu_callback(self, data):
        self.angular_velocity = abs(data.angular_velocity.z)
        self.linear_acceleration = abs(data.linear_acceleration.x)
        # You can uncomment the next line if you want minimal IMU feedback
        # print(f"IMU Data - Angular Velocity: {self.angular_velocity}, Linear Acceleration: {self.linear_acceleration}")

    def image_processing(self):
        ''' Process the image and detect objects '''
        if self.image is None:
            print("No image data available.")
            return

        print(f"Phase: {self.phase} - Searching for dolls.")
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
                        print(f"Doll detected with confidence {confidence*100:.2f}% at position ({center_x}, {center_y}).")

                        # New vertical percentage logic
                        if center_y < height / 2:
                            vertical_percentage = 50.0  # Cap at 50% if above the center
                        else:
                            vertical_percentage = round(
                                50 - ((center_y - height / 2) / (height / 2)) * 50, 2
                            )

                        horizontal_percentage = round((center_x / width) * 100, 2)
                        print(f"Doll Position - Horizontal: {horizontal_percentage}%, Vertical: {vertical_percentage}%")

        # Publish whether a doll was detected
        self.doll_detected_pub.publish(Bool(data=doll_detected))

        if doll_detected and self.phase == "exploring":
            print("Doll detected! Transitioning to Rotating to Doll phase.")
            self.phase = "rotating_to_doll"
            self.align_to_doll(doll_position, width)
            self.plan_to_doll(vertical_percentage)
        elif not doll_detected and self.phase in ["rotating_to_doll", "approaching"]:
            print("Doll lost from view. Maintaining current phase.")
            # Optionally, implement behavior when doll is lost
            # For example, stop movement or attempt to reacquire
        # No transition back to 'exploring'

        self.publish_image_detection()
        print("Image processing completed.")

    def draw_bounding_box(self, x, y, w, h, class_id, confidence):
        ''' Draw a bounding box around the detected object '''
        color = self.colors[class_id]
        label = f"{self.classes[class_id]}: {round(confidence, 2)}"
        cv.rectangle(self.image, (x, y), (x + w, y + h), color, 2)
        cv.putText(self.image, label, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        # Optionally, print bounding box info
        # print(f"Bounding box drawn for {self.classes[class_id]} at ({x}, {y}, {w}, {h}).")

    def align_to_doll(self, doll_position, frame_width):
        ''' Rotate the boat until the doll is near the center line '''
        print("Entering Rotating to Doll phase.")
        center_x = doll_position[0]
        tolerance = frame_width * 0.1  # 10% tolerance

        if abs(center_x - frame_width / 2) > tolerance:
            twist = Twist()
            twist.angular.z = -0.1 if center_x < frame_width / 2 else 0.1
            print(f"Rotating to align with doll. Angular Velocity set to: {twist.angular.z}")
            self.cmd_vel_pub.publish(twist)
            self.convert_and_publish_pwm(twist)  # Convert to PWM
        else:
            print("Boat aligned with the doll.")
            if self.phase == "rotating_to_doll":
                self.phase = "approaching"
                print("Transitioning to Approaching phase.")
                # Assuming alignment sets vertical_percentage to 50%
                self.plan_to_doll(vertical_percentage=50.0)

    def plan_to_doll(self, vertical_percentage):
        ''' Adjust the boat speed based on the vertical percentage '''
        if self.phase != "approaching":
            print("Not in Approaching phase. Skipping movement planning.")
            return

        print("Entering Approaching phase.")
        twist = Twist()

        if vertical_percentage > 25:
            twist.linear.x = 0.15  # Move towards the doll
            print(f"Approaching doll. Linear Velocity set to: {twist.linear.x}")
        else:
            twist.linear.x = -0.2  # Brake until the boat stops
            print(f"Braking. Linear Velocity set to: {twist.linear.x}")

        self.cmd_vel_pub.publish(twist)
        self.convert_and_publish_pwm(twist)  # Convert to PWM

        # Check if the boat has stopped using IMU linear acceleration
        if self.linear_acceleration is not None:
            if self.linear_acceleration < 0.1:
                print("Boat has stopped.")
                zero_twist = Twist()
                self.cmd_vel_pub.publish(zero_twist)
                self.convert_and_publish_pwm(zero_twist)  # Publish zero PWM
                # Optionally, transition to another phase or perform further actions
            else:
                print("Boat is still moving.")
        else:
            print("Linear acceleration data not available. Cannot verify if the boat has stopped.")

    def convert_and_publish_pwm(self, twist):
        ''' Convert Twist message to PWM signals and publish '''
        # Extract linear and angular velocities
        linear_vel = twist.linear.x
        angular_vel = twist.angular.z

        # Convert linear and angular velocities to left and right wheel velocities
        # Assuming differential drive
        v_right = linear_vel + (angular_vel * self.wheel_base) / 2
        v_left = linear_vel - (angular_vel * self.wheel_base) / 2

        # Map wheel velocities to PWM
        pwm_right = self.velocity_to_pwm(v_right)
        pwm_left = self.velocity_to_pwm(v_left)

        print(f"Converted velocities to PWM - Left: {pwm_left}, Right: {pwm_right}")

        # Publish PWM signals
        self.pwm_left_pub.publish(Int32(data=pwm_left))
        self.pwm_right_pub.publish(Int32(data=pwm_right))

    def velocity_to_pwm(self, velocity):
        ''' Map a velocity value to a PWM signal '''
        # Clamp the velocity to the max limits
        velocity = max(min(velocity, self.max_linear_vel), -self.max_linear_vel)

        # Normalize the velocity to [-1, 1]
        normalized_velocity = velocity / self.max_linear_vel

        # Map to PWM range
        pwm = int(normalized_velocity * self.max_pwm)

        # Ensure PWM is within [min_pwm, max_pwm]
        pwm = max(min(pwm, self.max_pwm), self.min_pwm)

        return pwm

    def publish_image_detection(self):
        ''' Publish the processed image to /image_detection topic '''
        if self.image is not None:
            try:
                image_msg = self.bridge.cv2_to_imgmsg(self.image, "bgr8")
                self.image_pub.publish(image_msg)
            except CvBridgeError as e:
                print(f"Failed to publish image: {e}")
        else:
            print("No image available to publish.")

    def kill_nodes(self):
        ''' Stop both exploration and PID controller nodes '''
        if self.phase == "exploring":
            print("Killing exploration and PID controller nodes...")
            try:
                subprocess.call(['rosnode', 'kill', '/jackal_explore_node'])
                print("Killed node: /jackal_explore_node")
               
                subprocess.call(['rosnode', 'kill', '/boat_pid_controller'])
                print("Killed node: /boat_pid_controller")

                # Initialize cmd_vel to zero immediately after killing nodes
                zero_twist = Twist()
                zero_twist.linear.x = 0.0
                zero_twist.angular.z = 0.0
                self.cmd_vel_pub.publish(zero_twist)
                self.convert_and_publish_pwm(zero_twist)  # Publish zero PWM
                print("Published zero Twist message to /cmd_vel_adjusted and PWM.")

            except Exception as e:
                print(f"Failed to kill nodes: {e}")
        else:
            print("kill_nodes called, but current phase is not 'exploring'.")

def main():
    rospy.init_node("instance_segmentation", log_level=rospy.WARN)  # Set higher log level to reduce ROS log output
    print("Instance Segmentation node started.")
    segmentation = Segmentation()
    rospy.spin()
    print("Instance Segmentation node has been shut down.")

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        print("Instance Segmentation node interrupted and is shutting down.")
