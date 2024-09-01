; Auto-generated. Do not edit!


(cl:in-package usv_msg-msg)


;//! \htmlinclude WaypointRoute.msg.html

(cl:defclass <WaypointRoute> (roslisp-msg-protocol:ros-message)
  ((waypoints
    :reader waypoints
    :initarg :waypoints
    :type (cl:vector usv_msg-msg:Waypoint)
   :initform (cl:make-array 0 :element-type 'usv_msg-msg:Waypoint :initial-element (cl:make-instance 'usv_msg-msg:Waypoint)))
   (speed
    :reader speed
    :initarg :speed
    :type cl:float
    :initform 0.0))
)

(cl:defclass WaypointRoute (<WaypointRoute>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <WaypointRoute>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'WaypointRoute)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name usv_msg-msg:<WaypointRoute> is deprecated: use usv_msg-msg:WaypointRoute instead.")))

(cl:ensure-generic-function 'waypoints-val :lambda-list '(m))
(cl:defmethod waypoints-val ((m <WaypointRoute>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader usv_msg-msg:waypoints-val is deprecated.  Use usv_msg-msg:waypoints instead.")
  (waypoints m))

(cl:ensure-generic-function 'speed-val :lambda-list '(m))
(cl:defmethod speed-val ((m <WaypointRoute>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader usv_msg-msg:speed-val is deprecated.  Use usv_msg-msg:speed instead.")
  (speed m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <WaypointRoute>) ostream)
  "Serializes a message object of type '<WaypointRoute>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'waypoints))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'waypoints))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'speed))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <WaypointRoute>) istream)
  "Deserializes a message object of type '<WaypointRoute>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'waypoints) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'waypoints)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'usv_msg-msg:Waypoint))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'speed) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<WaypointRoute>)))
  "Returns string type for a message object of type '<WaypointRoute>"
  "usv_msg/WaypointRoute")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'WaypointRoute)))
  "Returns string type for a message object of type 'WaypointRoute"
  "usv_msg/WaypointRoute")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<WaypointRoute>)))
  "Returns md5sum for a message object of type '<WaypointRoute>"
  "650bb71476c385be6992ca7ffe1ecd01")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'WaypointRoute)))
  "Returns md5sum for a message object of type 'WaypointRoute"
  "650bb71476c385be6992ca7ffe1ecd01")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<WaypointRoute>)))
  "Returns full string definition for message of type '<WaypointRoute>"
  (cl:format cl:nil "# List of waypoints to follow along route.~%usv_msg/Waypoint[] waypoints ~%~%# Speed for course commands, in m/s.~%float64 speed~%~%================================================================================~%MSG: usv_msg/Waypoint~%# Constants describing different waypoint behaviours.~%#   NAV_WAYPOINT: A waypoint for the vesesl to pass through on a route, position required only.~%#   NAV_STATION:  A station for the vessel to reach and align a position and yaw, for a duration.~%~%uint8 NAV_WAYPOINT=0     ~%uint8  NAV_STATION=1~%~%# MANDATORY:~%uint8 nav_type           # Type of waypoint, specify with NAV constants above~%geometry_msgs/Pose pose  # Desired pose for waypoint/station~%~%# IF NAV_STATION:~%float32 station_duration # Time in seconds to keep station, negative is indefinite~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'WaypointRoute)))
  "Returns full string definition for message of type 'WaypointRoute"
  (cl:format cl:nil "# List of waypoints to follow along route.~%usv_msg/Waypoint[] waypoints ~%~%# Speed for course commands, in m/s.~%float64 speed~%~%================================================================================~%MSG: usv_msg/Waypoint~%# Constants describing different waypoint behaviours.~%#   NAV_WAYPOINT: A waypoint for the vesesl to pass through on a route, position required only.~%#   NAV_STATION:  A station for the vessel to reach and align a position and yaw, for a duration.~%~%uint8 NAV_WAYPOINT=0     ~%uint8  NAV_STATION=1~%~%# MANDATORY:~%uint8 nav_type           # Type of waypoint, specify with NAV constants above~%geometry_msgs/Pose pose  # Desired pose for waypoint/station~%~%# IF NAV_STATION:~%float32 station_duration # Time in seconds to keep station, negative is indefinite~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <WaypointRoute>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'waypoints) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <WaypointRoute>))
  "Converts a ROS message object to a list"
  (cl:list 'WaypointRoute
    (cl:cons ':waypoints (waypoints msg))
    (cl:cons ':speed (speed msg))
))
