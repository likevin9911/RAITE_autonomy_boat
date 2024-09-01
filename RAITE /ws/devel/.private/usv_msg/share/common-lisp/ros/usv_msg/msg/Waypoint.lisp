; Auto-generated. Do not edit!


(cl:in-package usv_msg-msg)


;//! \htmlinclude Waypoint.msg.html

(cl:defclass <Waypoint> (roslisp-msg-protocol:ros-message)
  ((nav_type
    :reader nav_type
    :initarg :nav_type
    :type cl:fixnum
    :initform 0)
   (pose
    :reader pose
    :initarg :pose
    :type geometry_msgs-msg:Pose
    :initform (cl:make-instance 'geometry_msgs-msg:Pose))
   (station_duration
    :reader station_duration
    :initarg :station_duration
    :type cl:float
    :initform 0.0))
)

(cl:defclass Waypoint (<Waypoint>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Waypoint>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Waypoint)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name usv_msg-msg:<Waypoint> is deprecated: use usv_msg-msg:Waypoint instead.")))

(cl:ensure-generic-function 'nav_type-val :lambda-list '(m))
(cl:defmethod nav_type-val ((m <Waypoint>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader usv_msg-msg:nav_type-val is deprecated.  Use usv_msg-msg:nav_type instead.")
  (nav_type m))

(cl:ensure-generic-function 'pose-val :lambda-list '(m))
(cl:defmethod pose-val ((m <Waypoint>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader usv_msg-msg:pose-val is deprecated.  Use usv_msg-msg:pose instead.")
  (pose m))

(cl:ensure-generic-function 'station_duration-val :lambda-list '(m))
(cl:defmethod station_duration-val ((m <Waypoint>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader usv_msg-msg:station_duration-val is deprecated.  Use usv_msg-msg:station_duration instead.")
  (station_duration m))
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql '<Waypoint>)))
    "Constants for message type '<Waypoint>"
  '((:NAV_WAYPOINT . 0)
    (:NAV_STATION . 1))
)
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql 'Waypoint)))
    "Constants for message type 'Waypoint"
  '((:NAV_WAYPOINT . 0)
    (:NAV_STATION . 1))
)
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Waypoint>) ostream)
  "Serializes a message object of type '<Waypoint>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'nav_type)) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'pose) ostream)
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'station_duration))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Waypoint>) istream)
  "Deserializes a message object of type '<Waypoint>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'nav_type)) (cl:read-byte istream))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'pose) istream)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'station_duration) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Waypoint>)))
  "Returns string type for a message object of type '<Waypoint>"
  "usv_msg/Waypoint")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Waypoint)))
  "Returns string type for a message object of type 'Waypoint"
  "usv_msg/Waypoint")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Waypoint>)))
  "Returns md5sum for a message object of type '<Waypoint>"
  "68be9ca6ba586733f004f0265fb452c4")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Waypoint)))
  "Returns md5sum for a message object of type 'Waypoint"
  "68be9ca6ba586733f004f0265fb452c4")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Waypoint>)))
  "Returns full string definition for message of type '<Waypoint>"
  (cl:format cl:nil "# Constants describing different waypoint behaviours.~%#   NAV_WAYPOINT: A waypoint for the vesesl to pass through on a route, position required only.~%#   NAV_STATION:  A station for the vessel to reach and align a position and yaw, for a duration.~%~%uint8 NAV_WAYPOINT=0     ~%uint8  NAV_STATION=1~%~%# MANDATORY:~%uint8 nav_type           # Type of waypoint, specify with NAV constants above~%geometry_msgs/Pose pose  # Desired pose for waypoint/station~%~%# IF NAV_STATION:~%float32 station_duration # Time in seconds to keep station, negative is indefinite~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Waypoint)))
  "Returns full string definition for message of type 'Waypoint"
  (cl:format cl:nil "# Constants describing different waypoint behaviours.~%#   NAV_WAYPOINT: A waypoint for the vesesl to pass through on a route, position required only.~%#   NAV_STATION:  A station for the vessel to reach and align a position and yaw, for a duration.~%~%uint8 NAV_WAYPOINT=0     ~%uint8  NAV_STATION=1~%~%# MANDATORY:~%uint8 nav_type           # Type of waypoint, specify with NAV constants above~%geometry_msgs/Pose pose  # Desired pose for waypoint/station~%~%# IF NAV_STATION:~%float32 station_duration # Time in seconds to keep station, negative is indefinite~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Waypoint>))
  (cl:+ 0
     1
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'pose))
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Waypoint>))
  "Converts a ROS message object to a list"
  (cl:list 'Waypoint
    (cl:cons ':nav_type (nav_type msg))
    (cl:cons ':pose (pose msg))
    (cl:cons ':station_duration (station_duration msg))
))
