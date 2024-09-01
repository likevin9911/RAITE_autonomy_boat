#!/usr/bin/env python3
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

        # Publisher for the modified images
        self.image_pub = rospy.Publisher("/noisy_depth", Image, queue_size=10)

    def depth_image_callback(self, data):
        try:
            # Convert ROS depth image to OpenCV format
            cv_depth_image = self.bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
        except CvBridgeError as e:
            rospy.logerr(e)
            return

        # Normalize the depth image to 0-255 for processing
        normalized_depth = cv2.normalize(cv_depth_image, None, 0, 255, cv2.NORM_MINMAX)
        normalized_depth = np.uint8(normalized_depth)

        # Detect edges to define features
        edges = cv2.Canny(normalized_depth, 50, 150)

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw colored minimal enclosing circles based on the average darkness
        for contour in contours:
            if cv2.contourArea(contour) > 10:  # Filter out tiny contours
                mask = np.zeros_like(normalized_depth)  # Create a mask for the contour
                cv2.drawContours(mask, [contour], -1, 255, -1)  # Draw the contour on the mask
                mean_val = cv2.mean(normalized_depth, mask=mask)[0]  # Calculate mean value within the contour

                # Determine circle color based on mean value
                if mean_val < 85:
                    color = (0, 255, 0)  # Green for dark areas
                elif mean_val < 170:
                    color = (0, 255, 255)  # Yellow for medium darkness
                else:
                    color = (0, 0, 255)  # Red for light areas

                (x, y), radius = cv2.minEnclosingCircle(contour)
                center = (int(x), int(y))
                radius = int(radius)
                cv2.circle(normalized_depth, center, radius, color, 2)  # Draw circle in determined color

        # Convert the modified OpenCV image back to a ROS Image message
        try:
            ros_image = self.bridge.cv2_to_imgmsg(normalized_depth, "mono8")
        except CvBridgeError as e:
            rospy.logerr(e)
            return

        # Publish the modified image
        self.image_pub.publish(ros_image)

        # Optional: Display the image for debugging
        cv2.imshow("Features Highlighted", normalized_depth)
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
