#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np

class DepthFeatureHighlighter:
    def __init__(self):
        rospy.init_node('depth_feature_highlighter', anonymous=True)

        self.bridge = CvBridge()

        # Subscriber
        rospy.Subscriber("/camera/depth/image_rect_raw", Image, self.depth_image_callback)

        # Publisher for the modified images and the depth information
        self.image_pub = rospy.Publisher("/noisy_depth", Image, queue_size=10)
        self.depth_pub = rospy.Publisher("/camera/depth/image_rect_raw_modified", Image, queue_size=10)

    def depth_image_callback(self, data):
        try:
            # Convert ROS depth image to OpenCV format
            cv_depth_image = self.bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
        except CvBridgeError as e:
            rospy.logerr(e)
            return

        # Normalize the depth image to 0-255 for processing and visualization
        normalized_depth = cv2.normalize(cv_depth_image, None, 0, 255, cv2.NORM_MINMAX)
        normalized_depth = np.uint8(normalized_depth)

        # Apply Gaussian Blur to smooth the image and reduce noise
        blurred = cv2.GaussianBlur(normalized_depth, (5, 5), 0)

        # Use adaptive thresholding to create a better binary image for contour detection
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 11, 2)

        # Dilate the thresholded image to connect nearby contours (less aggressively)
        kernel = np.ones((3,3), np.uint8)
        dilated = cv2.dilate(thresh, kernel, iterations=1)

        # Detect edges using Canny
        edges = cv2.Canny(dilated, 50, 150)

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Create an output image to draw on
        output_image = cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR)

        # Draw contours based on the average darkness
        for contour in contours:
            mask = np.zeros_like(blurred)  # Create a mask for the contour
            cv2.drawContours(mask, [contour], -1, 255, -1)  # Draw the contour on the mask
            mean_val = cv2.mean(blurred, mask=mask)[0]  # Calculate mean value within the contour

            # Determine contour color based on mean value
            if mean_val < 85:
                color = (0, 255, 0)  # Green for blackish areas
            elif mean_val < 170:
                color = (0, 255, 255)  # Yellow for grayish areas
            else:
                color = (0, 0, 255)  # Red for whiteish areas

            cv2.drawContours(output_image, [contour], -1, color, 2)  # Draw contour in determined color

        # Convert the modified image back to a ROS Image message
        try:
            ros_image = self.bridge.cv2_to_imgmsg(output_image, "bgr8")
            depth_image_ros = self.bridge.cv2_to_imgmsg(cv_depth_image, "passthrough")
        except CvBridgeError as e:
            rospy.logerr(e)
            return

        # Publish the modified image and the original depth data
        self.image_pub.publish(ros_image)
        self.depth_pub.publish(depth_image_ros)

        # Optional: Display the image for debugging
        cv2.imshow("Features Highlighted", output_image)
        cv2.waitKey(1)

    def run(self):
        try:
            rospy.spin()
        except KeyboardInterrupt:
            print("Shutting down")
        cv2.destroyAllWindows()

if __name__ == '__main__':
    feature_highlighter = DepthFeatureHighlighter()
    feature_highlighter.run()
