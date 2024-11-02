#! /usr/bin/env python3
'''
    This is an instance segmentation code using Intel Realsense camera, OpenCV, and Yolov4-tiny
'''
import cv2 as cv
import numpy as np
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import Bool


class Segmentation:
    
    def __init__(self):
        ''' Initialize environment '''
        self.image_pub = rospy.Publisher("/image_detection", Image, queue_size=10)
        self.doll_detected_pub = rospy.Publisher("/doll_detected", Bool, queue_size=10)
        rospy.Subscriber("/camera/color/image_raw", Image, self.image_callback)
        rospy.logdebug("Initialized image publisher and subscribed to camera topic")

        ''' Conversion between ROS and OpenCV '''
        self.bridge = CvBridge()
        self.image = None

        ''' Load Yolo '''
        self.net = cv.dnn.readNet(
            "/home/lab/catkin_ws/src/autonomy_boat/config/test3.weights",
            "/home/lab/catkin_ws/src/autonomy_boat/config/test3.cfg"
        )

        self.classes = []
        with open("/home/lab/catkin_ws/src/autonomy_boat/config/test3.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        print(f"Classes loaded: {self.classes}")  # Enhanced print statement

        self.layer_names = self.net.getLayerNames()
        # Updated to handle OpenCV 4.2.0 and above where getUnconnectedOutLayers() returns 1-based indices
        try:
            self.outputlayers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers().flatten()]
        except AttributeError:
            # For older OpenCV versions
            self.outputlayers = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))

    def image_callback(self, data):
        ''' Callback function for image topic '''
        try:
            # Convert ROS Image message to OpenCV image
            self.image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(f"CvBridge Error: {e}")

        # Process the image
        self.image_processing()

    def image_processing(self):
        ''' Process the image and run YOLO detection '''
        if self.image is None:
            return

        height, width = self.image.shape[:2]

        # Detecting object
        blob = cv.dnn.blobFromImage(
            self.image, 
            0.00392, 
            (416, 416), 
            (0, 0, 0), 
            True, 
            crop=False
        )
        self.net.setInput(blob)
        outs = self.net.forward(self.outputlayers)

        class_ids = []
        confidences = []
        boxes = []
        doll_detected = False

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.25:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

                    # Check if detected object is a doll
                    if self.classes[class_id].lower() == "doll":  # Updated to match the new class
                        doll_detected = True
        
        indexes = cv.dnn.NMSBoxes(boxes, confidences, 0.4, 0.6)

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(self.classes[class_ids[i]])
                confidence = confidences[i]
                color = self.colors[class_ids[i]]
                # Label object
                cv.rectangle(self.image, (x, y), (x + w, y + h), color, 2)
                cv.putText(
                    self.image, 
                    f"{label} {confidence:.2f}", 
                    (x, y + 30), 
                    cv.FONT_HERSHEY_COMPLEX, 
                    0.8, 
                    (0, 0, 255), 
                    2
                )

        # Publish whether a doll was detected or not
        self.doll_detected_pub.publish(Bool(data=doll_detected))

        # Publish processed image
        try:
            image_out = self.bridge.cv2_to_imgmsg(self.image, "bgr8")
            self.image_pub.publish(image_out)
        except CvBridgeError as e:
            rospy.logerr(f"CvBridge Error: {e}")


def main():
    ''' The main function '''
    rospy.init_node("instance_segmentation", log_level=rospy.DEBUG)
    rospy.logdebug("Node started")
    segmentation = Segmentation()
    rospy.spin()  # Keeps the node running and listening to topics


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
