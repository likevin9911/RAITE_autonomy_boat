import rospy
from sensor_msgs.msg import Image as msg_Image
from cv_bridge import CvBridge, CvBridgeError
import sys
import os

class ImageListener:
    def __init__(self, topic):
        self.topic = topic
        self.bridge = CvBridge()
        self.sub = rospy.Subscriber(topic, msg_Image, self.imageDepthCallback)

    def imageDepthCallback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, data.encoding)
            # Ensure the pixel indices are integers
            pix = (int(data.width/2), int(data.height/2))
            sys.stdout.write('%s: Depth at center(%d, %d): %f(mm)\r' % (self.topic, pix[0], pix[1], cv_image[pix[1], pix[0]]))
            sys.stdout.flush()
        except CvBridgeError as e:
            print(e)
            return

if __name__ == '__main__':
    rospy.init_node("depth_image_processor")
    topic = '/camera/depth/image_rect_raw'  # Check the depth image topic in your Gazebo environment and replace this if necessary
    listener = ImageListener(topic)
    rospy.spin()
