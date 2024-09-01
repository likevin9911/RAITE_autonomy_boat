#! /usr/bin/env python3
'''
    This is an instance segmentation code using Intel Realsense camera, OpenCV, and Yolov4-tiny
'''
import cv2 as cv
import numpy as np
import pyrealsense2.pyrealsense2 as rs
import time
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image


class Segmentation:
    
    def __init__(self):
        ''' Initialize environment '''
        self.image_pub = rospy.Publisher("/image", Image, queue_size=30)
        rospy.logdebug("Initialized image publisher")

        ''' Conversion between ROS and OpenCV '''
        self.bridge = CvBridge()
        self.image = None


    def image_processing(self):

        # Load Yolo
        net = cv.dnn.readNet("/home/sinloops/catkin_ws/src/autonomy_boat/config/yolov4-tiny.weights",
                             "/home/sinloops/catkin_ws/src/autonomy_boat/config/yolov4-tiny.cfg")

        with open("/home/sinloops/catkin_ws/src/autonomy_boat/config/coco.names", "r") as f:
            classes = [line.strip() for line in f.readlines()]

        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        colors = np.random.uniform(0, 255, size=(len(classes), 3))

        # Initialize Realsense camera
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        print("[INFO] Starting streaming...")
        pipeline.start(config)
        print("[INFO] Camera ready.")

        try:
            while not rospy.is_shutdown():
                # Get frames
                frames = pipeline.wait_for_frames()
                color_frame = frames.get_color_frame()

                # Convert color frame to numpy array
                self.image = np.asanyarray(color_frame.get_data())
                
                # Get image dimensions
                height, width = self.image.shape[:2]

                # Detecting objects
                blob = cv.dnn.blobFromImage(self.image, 1/255.0, (416, 416), (0, 0, 0), True, crop=False)
                net.setInput(blob)
                outs = net.forward(output_layers)

                class_ids = []
                confidences = []
                boxes = []

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

                # Print debugging information
                print(f"Detected {len(boxes)} objects")

                # Apply non-maxima suppression to suppress weak overlapping bounding boxes
                indexes = cv.dnn.NMSBoxes(boxes, confidences, 0.4, 0.6)

                if len(indexes) > 0:
                    for i in indexes.flatten():
                        x, y, w, h = boxes[i]
                        label = str(classes[class_ids[i]])
                        color = [int(c) for c in colors[class_ids[i]]]

                        # Draw bounding box
                        cv.rectangle(self.image, (x, y), (x + w, y + h), color, 2)
                        cv.putText(self.image, f"{label}: {confidences[i]:.2f}", (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                        print(f"Object {label} detected with confidence {confidences[i]:.2f} at [{x}, {y}, {w}, {h}]")

                # Publish the image with bounding boxes
                image_out = self.bridge.cv2_to_imgmsg(self.image, "bgr8")
                image_out.header.stamp = rospy.Time.now()
                image_out.header.frame_id = "camera_color_frame"  # Replace with your correct frame ID
                self.image_pub.publish(image_out)

        finally:
            pipeline.stop()


def main():
    ''' The main function '''
    rospy.init_node("instance_segmentation", log_level=rospy.DEBUG)
    rospy.logdebug("Node started")
    segmentation = Segmentation()
    segmentation.image_processing()
    rospy.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
