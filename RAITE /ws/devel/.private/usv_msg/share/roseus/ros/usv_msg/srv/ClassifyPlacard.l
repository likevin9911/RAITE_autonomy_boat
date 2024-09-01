;; Auto-generated. Do not edit!


(when (boundp 'usv_msg::ClassifyPlacard)
  (if (not (find-package "USV_MSG"))
    (make-package "USV_MSG"))
  (shadow 'ClassifyPlacard (find-package "USV_MSG")))
(unless (find-package "USV_MSG::CLASSIFYPLACARD")
  (make-package "USV_MSG::CLASSIFYPLACARD"))
(unless (find-package "USV_MSG::CLASSIFYPLACARDREQUEST")
  (make-package "USV_MSG::CLASSIFYPLACARDREQUEST"))
(unless (find-package "USV_MSG::CLASSIFYPLACARDRESPONSE")
  (make-package "USV_MSG::CLASSIFYPLACARDRESPONSE"))

(in-package "ROS")

(if (not (find-package "SENSOR_MSGS"))
  (ros::roseus-add-msgs "sensor_msgs"))




(defclass usv_msg::ClassifyPlacardRequest
  :super ros::object
  :slots (_image ))

(defmethod usv_msg::ClassifyPlacardRequest
  (:init
   (&key
    ((:image __image) (instance sensor_msgs::Image :init))
    )
   (send-super :init)
   (setq _image __image)
   self)
  (:image
   (&rest __image)
   (if (keywordp (car __image))
       (send* _image __image)
     (progn
       (if __image (setq _image (car __image)))
       _image)))
  (:serialization-length
   ()
   (+
    ;; sensor_msgs/Image _image
    (send _image :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; sensor_msgs/Image _image
       (send _image :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; sensor_msgs/Image _image
     (send _image :deserialize buf ptr-) (incf ptr- (send _image :serialization-length))
   ;;
   self)
  )

(defclass usv_msg::ClassifyPlacardResponse
  :super ros::object
  :slots (_label _confidence _centre_x _success ))

(defmethod usv_msg::ClassifyPlacardResponse
  (:init
   (&key
    ((:label __label) "")
    ((:confidence __confidence) 0.0)
    ((:centre_x __centre_x) 0)
    ((:success __success) nil)
    )
   (send-super :init)
   (setq _label (string __label))
   (setq _confidence (float __confidence))
   (setq _centre_x (round __centre_x))
   (setq _success __success)
   self)
  (:label
   (&optional __label)
   (if __label (setq _label __label)) _label)
  (:confidence
   (&optional __confidence)
   (if __confidence (setq _confidence __confidence)) _confidence)
  (:centre_x
   (&optional __centre_x)
   (if __centre_x (setq _centre_x __centre_x)) _centre_x)
  (:success
   (&optional (__success :null))
   (if (not (eq __success :null)) (setq _success __success)) _success)
  (:serialization-length
   ()
   (+
    ;; string _label
    4 (length _label)
    ;; float32 _confidence
    4
    ;; int32 _centre_x
    4
    ;; bool _success
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _label
       (write-long (length _label) s) (princ _label s)
     ;; float32 _confidence
       (sys::poke _confidence (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; int32 _centre_x
       (write-long _centre_x s)
     ;; bool _success
       (if _success (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _label
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _label (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; float32 _confidence
     (setq _confidence (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; int32 _centre_x
     (setq _centre_x (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; bool _success
     (setq _success (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(defclass usv_msg::ClassifyPlacard
  :super ros::object
  :slots ())

(setf (get usv_msg::ClassifyPlacard :md5sum-) "564d8bb3409ecd03e36c23a70ebc1990")
(setf (get usv_msg::ClassifyPlacard :datatype-) "usv_msg/ClassifyPlacard")
(setf (get usv_msg::ClassifyPlacard :request) usv_msg::ClassifyPlacardRequest)
(setf (get usv_msg::ClassifyPlacard :response) usv_msg::ClassifyPlacardResponse)

(defmethod usv_msg::ClassifyPlacardRequest
  (:response () (instance usv_msg::ClassifyPlacardResponse :init)))

(setf (get usv_msg::ClassifyPlacardRequest :md5sum-) "564d8bb3409ecd03e36c23a70ebc1990")
(setf (get usv_msg::ClassifyPlacardRequest :datatype-) "usv_msg/ClassifyPlacardRequest")
(setf (get usv_msg::ClassifyPlacardRequest :definition-)
      "sensor_msgs/Image image

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
string label
float32 confidence
int32 centre_x
bool success

")

(setf (get usv_msg::ClassifyPlacardResponse :md5sum-) "564d8bb3409ecd03e36c23a70ebc1990")
(setf (get usv_msg::ClassifyPlacardResponse :datatype-) "usv_msg/ClassifyPlacardResponse")
(setf (get usv_msg::ClassifyPlacardResponse :definition-)
      "sensor_msgs/Image image

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
string label
float32 confidence
int32 centre_x
bool success

")



(provide :usv_msg/ClassifyPlacard "564d8bb3409ecd03e36c23a70ebc1990")


