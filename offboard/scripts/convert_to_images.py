#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
import os

class ImageSaver:
    def __init__(self):
        # Initialize the ROS node
        rospy.init_node('image_saver_node', anonymous=True)
        
        # Create a CvBridge object for converting ROS Image messages to OpenCV images
        self.bridge = CvBridge()
        
        # Create the train_images directory if it doesn't exist
        self.image_directory = 'train_images'
        if not os.path.exists(self.image_directory):
            os.makedirs(self.image_directory)
            rospy.loginfo(f"Created directory: {self.image_directory}")
        
        # Initialize an image counter
        self.image_counter = 0
        
        # Subscribe to the /camera/color/image_raw topic
        rospy.Subscriber('/camera/color/image_raw', Image, self.image_callback)
        rospy.loginfo("Subscribed to /camera/color/image_raw topic")
        
        # Spin to keep the script for exiting
        rospy.spin()
    
    def image_callback(self, msg):
        try:
            # Convert the ROS Image message to an OpenCV image
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            
            # Generate a unique filename for each image
            image_filename = f'image_{self.image_counter:06d}.png'
            image_path = os.path.join(self.image_directory, image_filename)
            
            # Save the image in PNG format
            cv2.imwrite(image_path, cv_image)
            rospy.loginfo(f"Saved image: {image_filename}")
            
            # Increment the image counter
            self.image_counter += 1
        except Exception as e:
            rospy.logerr(f"Failed to save image: {e}")

if __name__ == '__main__':
    try:
        ImageSaver()
    except rospy.ROSInterruptException:
        pass

