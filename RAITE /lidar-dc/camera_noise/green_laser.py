#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np

class ImageModifier:
    def __init__(self):
        rospy.init_node('image_modifier', anonymous=True)
        self.bridge = CvBridge()

        # Subscriber for the camera topic
        rospy.Subscriber("/camera/color/image_raw", Image, self.color_image_callback)

        # Publisher for the modified image
        self.image_pub = rospy.Publisher("/camera/color/noise", Image, queue_size=10)

    def color_image_callback(self, data):
        try:
            # Convert ROS image to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")

            # Generate translucent green blobs and blend them
            modified_image = self.add_green_blobs(cv_image)

            # Prepare the ROS message, copying the header from the input to output
            output_msg = self.bridge.cv2_to_imgmsg(modified_image, "bgr8")
            output_msg.header = data.header  # Ensure the header information is preserved

            # Publish the modified image
            self.image_pub.publish(output_msg)
        except CvBridgeError as e:
            rospy.logerr(e)

    def add_green_blobs(self, image):
        num_blobs = 25
        max_radius = 100
        strength = 1  # Transparency of the blobs

        # Create an image to draw blobs on
        blob_image = np.zeros_like(image)

        for _ in range(num_blobs):
            # Choose a random type of blob, either two circles or two ellipses
            blob_type = np.random.choice(['circle_pair', 'ellipse_pair'])

            if blob_type == 'circle_pair':
                # Generate two close circles to form a complex shape
                x1, y1 = np.random.randint(0, image.shape[1]), np.random.randint(0, image.shape[0])
                x2, y2 = x1 + np.random.randint(-20, 20), y1 + np.random.randint(-20, 20)
                radius1, radius2 = np.random.randint(10, max_radius), np.random.randint(10, max_radius)

                # Draw two overlapping green circles
                cv2.circle(blob_image, (x1, y1), radius1, (0, 255, 0), -1)
                cv2.circle(blob_image, (x2, y2), radius2, (0, 255, 0), -1)

            elif blob_type == 'ellipse_pair':
                # Generate two green ellipses
                for _ in range(2):  # Draw two ellipses
                    center = (np.random.randint(0, image.shape[1]), np.random.randint(0, image.shape[0]))
                    axes = (np.random.randint(10, max_radius), np.random.randint(10, max_radius))
                    angle = np.random.randint(0, 180)
                    cv2.ellipse(blob_image, center, axes, angle, 0, 360, (0, 255, 0), -1)

        # Blend the blob image with the original image
        return cv2.addWeighted(image, 1, blob_image, strength, 0)

    def run(self):
        try:
            rospy.spin()
        except KeyboardInterrupt:
            print("Shutting down")
        cv2.destroyAllWindows()

if __name__ == '__main__':
    img_mod = ImageModifier()
    img_mod.run()
