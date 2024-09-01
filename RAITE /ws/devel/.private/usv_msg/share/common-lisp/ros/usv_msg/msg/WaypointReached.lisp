; Auto-generated. Do not edit!


(cl:in-package usv_msg-msg)


;//! \htmlinclude WaypointReached.msg.html

(cl:defclass <WaypointReached> (roslisp-msg-protocol:ros-message)
  ((reached
    :reader reached
    :initarg :reached
    :type cl:boolean
    :initform cl:nil)
   (waypoint_id
    :reader waypoint_id
    :initarg :waypoint_id
    :type cl:integer
    :initform 0))
)

(cl:defclass WaypointReached (<WaypointReached>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <WaypointReached>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'WaypointReached)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name usv_msg-msg:<WaypointReached> is deprecated: use usv_msg-msg:WaypointReached instead.")))

(cl:ensure-generic-function 'reached-val :lambda-list '(m))
(cl:defmethod reached-val ((m <WaypointReached>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader usv_msg-msg:reached-val is deprecated.  Use usv_msg-msg:reached instead.")
  (reached m))

(cl:ensure-generic-function 'waypoint_id-val :lambda-list '(m))
(cl:defmethod waypoint_id-val ((m <WaypointReached>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader usv_msg-msg:waypoint_id-val is deprecated.  Use usv_msg-msg:waypoint_id instead.")
  (waypoint_id m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <WaypointReached>) ostream)
  "Serializes a message object of type '<WaypointReached>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'reached) 1 0)) ostream)
  (cl:let* ((signed (cl:slot-value msg 'waypoint_id)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <WaypointReached>) istream)
  "Deserializes a message object of type '<WaypointReached>"
    (cl:setf (cl:slot-value msg 'reached) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'waypoint_id) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<WaypointReached>)))
  "Returns string type for a message object of type '<WaypointReached>"
  "usv_msg/WaypointReached")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'WaypointReached)))
  "Returns string type for a message object of type 'WaypointReached"
  "usv_msg/WaypointReached")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<WaypointReached>)))
  "Returns md5sum for a message object of type '<WaypointReached>"
  "b886e6b1bcee335c42ff82d1ed3658f4")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'WaypointReached)))
  "Returns md5sum for a message object of type 'WaypointReached"
  "b886e6b1bcee335c42ff82d1ed3658f4")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<WaypointReached>)))
  "Returns full string definition for message of type '<WaypointReached>"
  (cl:format cl:nil "bool reached~%int32 waypoint_id~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'WaypointReached)))
  "Returns full string definition for message of type 'WaypointReached"
  (cl:format cl:nil "bool reached~%int32 waypoint_id~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <WaypointReached>))
  (cl:+ 0
     1
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <WaypointReached>))
  "Converts a ROS message object to a list"
  (cl:list 'WaypointReached
    (cl:cons ':reached (reached msg))
    (cl:cons ':waypoint_id (waypoint_id msg))
))
