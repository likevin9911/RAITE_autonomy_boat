;; Auto-generated. Do not edit!


(when (boundp 'usv_msg::ClassifyBuoy)
  (if (not (find-package "USV_MSG"))
    (make-package "USV_MSG"))
  (shadow 'ClassifyBuoy (find-package "USV_MSG")))
(unless (find-package "USV_MSG::CLASSIFYBUOY")
  (make-package "USV_MSG::CLASSIFYBUOY"))
(unless (find-package "USV_MSG::CLASSIFYBUOYREQUEST")
  (make-package "USV_MSG::CLASSIFYBUOYREQUEST"))
(unless (find-package "USV_MSG::CLASSIFYBUOYRESPONSE")
  (make-package "USV_MSG::CLASSIFYBUOYRESPONSE"))

(in-package "ROS")

(if (not (find-package "SENSOR_MSGS"))
  (ros::roseus-add-msgs "sensor_msgs"))




(defclass usv_msg::ClassifyBuoyRequest
  :super ros::object
  :slots (_image _distance ))

(defmethod usv_msg::ClassifyBuoyRequest
  (:init
   (&key
    ((:image __image) (instance sensor_msgs::Image :init))
    ((:distance __distance) 0.0)
    )
   (send-super :init)
   (setq _image __image)
   (setq _distance (float __distance))
   self)
  (:image
   (&rest __image)
   (if (keywordp (car __image))
       (send* _image __image)
     (progn
       (if __image (setq _image (car __image)))
       _image)))
  (:distance
   (&optional __distance)
   (if __distance (setq _distance __distance)) _distance)
  (:serialization-length
   ()
   (+
    ;; sensor_msgs/Image _image
    (send _image :serialization-length)
    ;; float32 _distance
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; sensor_msgs/Image _image
       (send _image :serialize s)
     ;; float32 _distance
       (sys::poke _distance (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; sensor_msgs/Image _image
     (send _image :deserialize buf ptr-) (incf ptr- (send _image :serialization-length))
   ;; float32 _distance
     (setq _distance (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(defclass usv_msg::ClassifyBuoyResponse
  :super ros::object
  :slots (_type _confidence _success ))

(defmethod usv_msg::ClassifyBuoyResponse
  (:init
   (&key
    ((:type __type) "")
    ((:confidence __confidence) 0.0)
    ((:success __success) nil)
    )
   (send-super :init)
   (setq _type (string __type))
   (setq _confidence (float __confidence))
   (setq _success __success)
   self)
  (:type
   (&optional __type)
   (if __type (setq _type __type)) _type)
  (:confidence
   (&optional __confidence)
   (if __confidence (setq _confidence __confidence)) _confidence)
  (:success
   (&optional (__success :null))
   (if (not (eq __success :null)) (setq _success __success)) _success)
  (:serialization-length
   ()
   (+
    ;; string _type
    4 (length _type)
    ;; float32 _confidence
    4
    ;; bool _success
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _type
       (write-long (length _type) s) (princ _type s)
     ;; float32 _confidence
       (sys::poke _confidence (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; bool _success
       (if _success (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _type
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _type (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; float32 _confidence
     (setq _confidence (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; bool _success
     (setq _success (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(defclass usv_msg::ClassifyBuoy
  :super ros::object
  :slots ())

(setf (get usv_msg::ClassifyBuoy :md5sum-) "c33e4e3dce31d590391aa868e5718794")
(setf (get usv_msg::ClassifyBuoy :datatype-) "usv_msg/ClassifyBuoy")
(setf (get usv_msg::ClassifyBuoy :request) usv_msg::ClassifyBuoyRequest)
(setf (get usv_msg::ClassifyBuoy :response) usv_msg::ClassifyBuoyResponse)

(defmethod usv_msg::ClassifyBuoyRequest
  (:response () (instance usv_msg::ClassifyBuoyResponse :init)))

(setf (get usv_msg::ClassifyBuoyRequest :md5sum-) "c33e4e3dce31d590391aa868e5718794")
(setf (get usv_msg::ClassifyBuoyRequest :datatype-) "usv_msg/ClassifyBuoyRequest")
(setf (get usv_msg::ClassifyBuoyRequest :definition-)
      "sensor_msgs/Image image
float32 distance

================================================================================
MSG: sensor_msgs/Image
# This message contains an uncompressed image
# (0, 0) is at top-left corner of image
#

Header header        # Header timestamp should be acquisition time of image
                     # Header frame_id should be optical frame of camera
                     # origin of frame should be optical center of camera
                     # +x should point to the right in the image
                     # +y should point down in the image
                     # +z should point into to plane of the image
                     # If the frame_id here and the frame_id of the CameraInfo
                     # message associated with the image conflict
                     # the behavior is undefined

uint32 height         # image height, that is, number of rows
uint32 width          # image width, that is, number of columns

# The legal values for encoding are in file src/image_encodings.cpp
# If you want to standardize a new string format, join
# ros-users@lists.sourceforge.net and send an email proposing a new encoding.

string encoding       # Encoding of pixels -- channel meaning, ordering, size
                      # taken from the list of strings in include/sensor_msgs/image_encodings.h

uint8 is_bigendian    # is this data bigendian?
uint32 step           # Full row length in bytes
uint8[] data          # actual matrix data, size is (step * rows)

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id
---
string type
float32 confidence
bool success

")

(setf (get usv_msg::ClassifyBuoyResponse :md5sum-) "c33e4e3dce31d590391aa868e5718794")
(setf (get usv_msg::ClassifyBuoyResponse :datatype-) "usv_msg/ClassifyBuoyResponse")
(setf (get usv_msg::ClassifyBuoyResponse :definition-)
      "sensor_msgs/Image image
float32 distance

================================================================================
MSG: sensor_msgs/Image
# This message contains an uncompressed image
# (0, 0) is at top-left corner of image
#

Header header        # Header timestamp should be acquisition time of image
                     # Header frame_id should be optical frame of camera
                     # origin of frame should be optical center of camera
                     # +x should point to the right in the image
                     # +y should point down in the image
                     # +z should point into to plane of the image
                     # If the frame_id here and the frame_id of the CameraInfo
                     # message associated with the image conflict
                     # the behavior is undefined

uint32 height         # image height, that is, number of rows
uint32 width          # image width, that is, number of columns

# The legal values for encoding are in file src/image_encodings.cpp
# If you want to standardize a new string format, join
# ros-users@lists.sourceforge.net and send an email proposing a new encoding.

string encoding       # Encoding of pixels -- channel meaning, ordering, size
                      # taken from the list of strings in include/sensor_msgs/image_encodings.h

uint8 is_bigendian    # is this data bigendian?
uint32 step           # Full row length in bytes
uint8[] data          # actual matrix data, size is (step * rows)

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id
---
string type
float32 confidence
bool success

")



(provide :usv_msg/ClassifyBuoy "c33e4e3dce31d590391aa868e5718794")


