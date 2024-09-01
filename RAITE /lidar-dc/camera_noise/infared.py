#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np

class ImageFlashInjector:
    def __init__(self):
        rospy.init_node('image_flash_injector', anonymous=True)
        self.bridge = CvBridge()

        # Subscriber for the camera topic
        rospy.Subscriber("/camera/color/image_raw", Image, self.image_callback, queue_size=20)

        # Publisher for the modified image
        self.image_pub = rospy.Publisher("/camera/color/noise", Image, queue_size=30)

    def image_callback(self, data):
        try:
            # Convert ROS image to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")

            # Inject flashes of light with a pink tint
            flashed_image = self.add_pink_flashes(cv_image)

            # Prepare the ROS message, copying the header from input to output
            output_msg = self.bridge.cv2_to_imgmsg(flashed_image, "bgr8")
            output_msg.header = data.header  # Ensuring the header information is preserved

            # Publish the modified image
            self.image_pub.publish(output_msg)
        except CvBridgeError as e:
            rospy.logerr(e)

    def add_pink_flashes(self, image):
        # Number of flashes per frame
        num_flashes = np.random.randint(1, 3)  # Random number of flashes between 1 and 2

        for _ in range(num_flashes):
            # Select random location for the flash
            x, y = np.random.randint(0, image.shape[1]), np.random.randint(0, image.shape[0])
            radius = np.random.randint(50, 100)  # Radius of the flash

            # Create a mask to apply the pink flash
            mask = np.zeros_like(image)
            cv2.circle(mask, (x, y), radius, (147, 20, 255), -1)  # Pink tint in BGR format

            # Apply a fixed Gaussian blur to create a gradient effect
            blurred_mask = cv2.GaussianBlur(mask, (51, 51), sigmaX=25, sigmaY=25)

            # Blend the original image with the mask
            image = cv2.addWeighted(image, 1, blurred_mask, 0.6, 0)

        return image

    def run(self):
        try:
            rospy.spin()
        except KeyboardInterrupt:
            print("Shutting down")
        cv2.destroyAllWindows()

if __name__ == '__main__':
    flash_injector = ImageFlashInjector()
    flash_injector.run()
