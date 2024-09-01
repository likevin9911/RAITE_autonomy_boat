; Auto-generated. Do not edit!


(cl:in-package usv_msg-msg)


;//! \htmlinclude VesselWaypoint.msg.html

(cl:defclass <VesselWaypoint> (roslisp-msg-protocol:ros-message)
  ((pose
    :reader pose
    :initarg :pose
    :type geometry_msgs-msg:Pose
    :initform (cl:make-instance 'geometry_msgs-msg:Pose))
   (tolerance
    :reader tolerance
    :initarg :tolerance
    :type cl:float
    :initform 0.0))
)

(cl:defclass VesselWaypoint (<VesselWaypoint>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <VesselWaypoint>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'VesselWaypoint)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name usv_msg-msg:<VesselWaypoint> is deprecated: use usv_msg-msg:VesselWaypoint instead.")))

(cl:ensure-generic-function 'pose-val :lambda-list '(m))
(cl:defmethod pose-val ((m <VesselWaypoint>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader usv_msg-msg:pose-val is deprecated.  Use usv_msg-msg:pose instead.")
  (pose m))

(cl:ensure-generic-function 'tolerance-val :lambda-list '(m))
(cl:defmethod tolerance-val ((m <VesselWaypoint>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader usv_msg-msg:tolerance-val is deprecated.  Use usv_msg-msg:tolerance instead.")
  (tolerance m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <VesselWaypoint>) ostream)
  "Serializes a message object of type '<VesselWaypoint>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'pose) ostream)
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'tolerance))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <VesselWaypoint>) istream)
  "Deserializes a message object of type '<VesselWaypoint>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'pose) istream)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'tolerance) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<VesselWaypoint>)))
  "Returns string type for a message object of type '<VesselWaypoint>"
  "usv_msg/VesselWaypoint")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'VesselWaypoint)))
  "Returns string type for a message object of type 'VesselWaypoint"
  "usv_msg/VesselWaypoint")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<VesselWaypoint>)))
  "Returns md5sum for a message object of type '<VesselWaypoint>"
  "a86a362d03a0b4e7c7a4ba71dd826bc6")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'VesselWaypoint)))
  "Returns md5sum for a message object of type 'VesselWaypoint"
  "a86a362d03a0b4e7c7a4ba71dd826bc6")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<VesselWaypoint>)))
  "Returns full string definition for message of type '<VesselWaypoint>"
  (cl:format cl:nil "# Desired pose of the waypoint~%geometry_msgs/Pose pose~%# Tolerance on the waypoint~%float64 tolerance~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'VesselWaypoint)))
  "Returns full string definition for message of type 'VesselWaypoint"
  (cl:format cl:nil "# Desired pose of the waypoint~%geometry_msgs/Pose pose~%# Tolerance on the waypoint~%float64 tolerance~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <VesselWaypoint>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'pose))
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <VesselWaypoint>))
  "Converts a ROS message object to a list"
  (cl:list 'VesselWaypoint
    (cl:cons ':pose (pose msg))
    (cl:cons ':tolerance (tolerance msg))
))
