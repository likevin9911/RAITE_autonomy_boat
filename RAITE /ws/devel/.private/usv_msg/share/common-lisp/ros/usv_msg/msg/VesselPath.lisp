; Auto-generated. Do not edit!


(cl:in-package usv_msg-msg)


;//! \htmlinclude VesselPath.msg.html

(cl:defclass <VesselPath> (roslisp-msg-protocol:ros-message)
  ((waypoints
    :reader waypoints
    :initarg :waypoints
    :type (cl:vector usv_msg-msg:VesselWaypoint)
   :initform (cl:make-array 0 :element-type 'usv_msg-msg:VesselWaypoint :initial-element (cl:make-instance 'usv_msg-msg:VesselWaypoint))))
)

(cl:defclass VesselPath (<VesselPath>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <VesselPath>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'VesselPath)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name usv_msg-msg:<VesselPath> is deprecated: use usv_msg-msg:VesselPath instead.")))

(cl:ensure-generic-function 'waypoints-val :lambda-list '(m))
(cl:defmethod waypoints-val ((m <VesselPath>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader usv_msg-msg:waypoints-val is deprecated.  Use usv_msg-msg:waypoints instead.")
  (waypoints m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <VesselPath>) ostream)
  "Serializes a message object of type '<VesselPath>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'waypoints))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'waypoints))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <VesselPath>) istream)
  "Deserializes a message object of type '<VesselPath>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'waypoints) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'waypoints)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'usv_msg-msg:VesselWaypoint))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<VesselPath>)))
  "Returns string type for a message object of type '<VesselPath>"
  "usv_msg/VesselPath")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'VesselPath)))
  "Returns string type for a message object of type 'VesselPath"
  "usv_msg/VesselPath")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<VesselPath>)))
  "Returns md5sum for a message object of type '<VesselPath>"
  "4259dc009ec92bea4f4406b99ae80570")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'VesselPath)))
  "Returns md5sum for a message object of type 'VesselPath"
  "4259dc009ec92bea4f4406b99ae80570")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<VesselPath>)))
  "Returns full string definition for message of type '<VesselPath>"
  (cl:format cl:nil "usv_msg/VesselWaypoint[] waypoints~%~%================================================================================~%MSG: usv_msg/VesselWaypoint~%# Desired pose of the waypoint~%geometry_msgs/Pose pose~%# Tolerance on the waypoint~%float64 tolerance~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'VesselPath)))
  "Returns full string definition for message of type 'VesselPath"
  (cl:format cl:nil "usv_msg/VesselWaypoint[] waypoints~%~%================================================================================~%MSG: usv_msg/VesselWaypoint~%# Desired pose of the waypoint~%geometry_msgs/Pose pose~%# Tolerance on the waypoint~%float64 tolerance~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <VesselPath>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'waypoints) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <VesselPath>))
  "Converts a ROS message object to a list"
  (cl:list 'VesselPath
    (cl:cons ':waypoints (waypoints msg))
))
