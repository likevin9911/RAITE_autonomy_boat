; Auto-generated. Do not edit!


(cl:in-package usv_msg-srv)


;//! \htmlinclude ClassifyBuoy-request.msg.html

(cl:defclass <ClassifyBuoy-request> (roslisp-msg-protocol:ros-message)
  ((image
    :reader image
    :initarg :image
    :type sensor_msgs-msg:Image
    :initform (cl:make-instance 'sensor_msgs-msg:Image))
   (distance
    :reader distance
    :initarg :distance
    :type cl:float
    :initform 0.0))
)

(cl:defclass ClassifyBuoy-request (<ClassifyBuoy-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ClassifyBuoy-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ClassifyBuoy-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name usv_msg-srv:<ClassifyBuoy-request> is deprecated: use usv_msg-srv:ClassifyBuoy-request instead.")))

(cl:ensure-generic-function 'image-val :lambda-list '(m))
(cl:defmethod image-val ((m <ClassifyBuoy-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader usv_msg-srv:image-val is deprecated.  Use usv_msg-srv:image instead.")
  (image m))

(cl:ensure-generic-function 'distance-val :lambda-list '(m))
(cl:defmethod distance-val ((m <ClassifyBuoy-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader usv_msg-srv:distance-val is deprecated.  Use usv_msg-srv:distance instead.")
  (distance m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ClassifyBuoy-request>) ostream)
  "Serializes a message object of type '<ClassifyBuoy-request>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'image) ostream)
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'distance))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ClassifyBuoy-request>) istream)
  "Deserializes a message object of type '<ClassifyBuoy-request>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'image) istream)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'distance) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ClassifyBuoy-request>)))
  "Returns string type for a service object of type '<ClassifyBuoy-request>"
  "usv_msg/ClassifyBuoyRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ClassifyBuoy-request)))
  "Returns string type for a service object of type 'ClassifyBuoy-request"
  "usv_msg/ClassifyBuoyRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ClassifyBuoy-request>)))
  "Returns md5sum for a message object of type '<ClassifyBuoy-request>"
  "c33e4e3dce31d590391aa868e5718794")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ClassifyBuoy-request)))
  "Returns md5sum for a message object of type 'ClassifyBuoy-request"
  "c33e4e3dce31d590391aa868e5718794")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ClassifyBuoy-request>)))
  "Returns full string definition for message of type '<ClassifyBuoy-request>"
  (cl:format cl:nil "sensor_msgs/Image image~%float32 distance~%~%================================================================================~%MSG: sensor_msgs/Image~%# This message contains an uncompressed image~%# (0, 0) is at top-left corner of image~%#~%~%Header header        # Header timestamp should be acquisition time of image~%                     # Header frame_id should be optical frame of camera~%                     # origin of frame should be optical center of camera~%                     # +x should point to the right in the image~%                     # +y should point down in the image~%                     # +z should point into to plane of the image~%                     # If the frame_id here and the frame_id of the CameraInfo~%                     # message associated with the image conflict~%                     # the behavior is undefined~%~%uint32 height         # image height, that is, number of rows~%uint32 width          # image width, that is, number of columns~%~%# The legal values for encoding are in file src/image_encodings.cpp~%# If you want to standardize a new string format, join~%# ros-users@lists.sourceforge.net and send an email proposing a new encoding.~%~%string encoding       # Encoding of pixels -- channel meaning, ordering, size~%                      # taken from the list of strings in include/sensor_msgs/image_encodings.h~%~%uint8 is_bigendian    # is this data bigendian?~%uint32 step           # Full row length in bytes~%uint8[] data          # actual matrix data, size is (step * rows)~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ClassifyBuoy-request)))
  "Returns full string definition for message of type 'ClassifyBuoy-request"
  (cl:format cl:nil "sensor_msgs/Image image~%float32 distance~%~%================================================================================~%MSG: sensor_msgs/Image~%# This message contains an uncompressed image~%# (0, 0) is at top-left corner of image~%#~%~%Header header        # Header timestamp should be acquisition time of image~%                     # Header frame_id should be optical frame of camera~%                     # origin of frame should be optical center of camera~%                     # +x should point to the right in the image~%                     # +y should point down in the image~%                     # +z should point into to plane of the image~%                     # If the frame_id here and the frame_id of the CameraInfo~%                     # message associated with the image conflict~%                     # the behavior is undefined~%~%uint32 height         # image height, that is, number of rows~%uint32 width          # image width, that is, number of columns~%~%# The legal values for encoding are in file src/image_encodings.cpp~%# If you want to standardize a new string format, join~%# ros-users@lists.sourceforge.net and send an email proposing a new encoding.~%~%string encoding       # Encoding of pixels -- channel meaning, ordering, size~%                      # taken from the list of strings in include/sensor_msgs/image_encodings.h~%~%uint8 is_bigendian    # is this data bigendian?~%uint32 step           # Full row length in bytes~%uint8[] data          # actual matrix data, size is (step * rows)~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ClassifyBuoy-request>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'image))
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ClassifyBuoy-request>))
  "Converts a ROS message object to a list"
  (cl:list 'ClassifyBuoy-request
    (cl:cons ':image (image msg))
    (cl:cons ':distance (distance msg))
))
;//! \htmlinclude ClassifyBuoy-response.msg.html

(cl:defclass <ClassifyBuoy-response> (roslisp-msg-protocol:ros-message)
  ((type
    :reader type
    :initarg :type
    :type cl:string
    :initform "")
   (confidence
    :reader confidence
    :initarg :confidence
    :type cl:float
    :initform 0.0)
   (success
    :reader success
    :initarg :success
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass ClassifyBuoy-response (<ClassifyBuoy-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ClassifyBuoy-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ClassifyBuoy-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name usv_msg-srv:<ClassifyBuoy-response> is deprecated: use usv_msg-srv:ClassifyBuoy-response instead.")))

(cl:ensure-generic-function 'type-val :lambda-list '(m))
(cl:defmethod type-val ((m <ClassifyBuoy-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader usv_msg-srv:type-val is deprecated.  Use usv_msg-srv:type instead.")
  (type m))

(cl:ensure-generic-function 'confidence-val :lambda-list '(m))
(cl:defmethod confidence-val ((m <ClassifyBuoy-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader usv_msg-srv:confidence-val is deprecated.  Use usv_msg-srv:confidence instead.")
  (confidence m))

(cl:ensure-generic-function 'success-val :lambda-list '(m))
(cl:defmethod success-val ((m <ClassifyBuoy-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader usv_msg-srv:success-val is deprecated.  Use usv_msg-srv:success instead.")
  (success m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ClassifyBuoy-response>) ostream)
  "Serializes a message object of type '<ClassifyBuoy-response>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'type))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'type))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'confidence))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'success) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ClassifyBuoy-response>) istream)
  "Deserializes a message object of type '<ClassifyBuoy-response>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'type) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'type) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'confidence) (roslisp-utils:decode-single-float-bits bits)))
    (cl:setf (cl:slot-value msg 'success) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ClassifyBuoy-response>)))
  "Returns string type for a service object of type '<ClassifyBuoy-response>"
  "usv_msg/ClassifyBuoyResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ClassifyBuoy-response)))
  "Returns string type for a service object of type 'ClassifyBuoy-response"
  "usv_msg/ClassifyBuoyResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ClassifyBuoy-response>)))
  "Returns md5sum for a message object of type '<ClassifyBuoy-response>"
  "c33e4e3dce31d590391aa868e5718794")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ClassifyBuoy-response)))
  "Returns md5sum for a message object of type 'ClassifyBuoy-response"
  "c33e4e3dce31d590391aa868e5718794")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ClassifyBuoy-response>)))
  "Returns full string definition for message of type '<ClassifyBuoy-response>"
  (cl:format cl:nil "string type~%float32 confidence~%bool success~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ClassifyBuoy-response)))
  "Returns full string definition for message of type 'ClassifyBuoy-response"
  (cl:format cl:nil "string type~%float32 confidence~%bool success~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ClassifyBuoy-response>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'type))
     4
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ClassifyBuoy-response>))
  "Converts a ROS message object to a list"
  (cl:list 'ClassifyBuoy-response
    (cl:cons ':type (type msg))
    (cl:cons ':confidence (confidence msg))
    (cl:cons ':success (success msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'ClassifyBuoy)))
  'ClassifyBuoy-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'ClassifyBuoy)))
  'ClassifyBuoy-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ClassifyBuoy)))
  "Returns string type for a service object of type '<ClassifyBuoy>"
  "usv_msg/ClassifyBuoy")