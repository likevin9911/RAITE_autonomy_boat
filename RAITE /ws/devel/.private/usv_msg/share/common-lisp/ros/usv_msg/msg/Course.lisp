; Auto-generated. Do not edit!


(cl:in-package usv_msg-msg)


;//! \htmlinclude Course.msg.html

(cl:defclass <Course> (roslisp-msg-protocol:ros-message)
  ((yaw
    :reader yaw
    :initarg :yaw
    :type cl:float
    :initform 0.0)
   (speed
    :reader speed
    :initarg :speed
    :type cl:float
    :initform 0.0)
   (keep_station
    :reader keep_station
    :initarg :keep_station
    :type cl:boolean
    :initform cl:nil)
   (station_yaw
    :reader station_yaw
    :initarg :station_yaw
    :type cl:float
    :initform 0.0)
   (station_dist_x
    :reader station_dist_x
    :initarg :station_dist_x
    :type cl:float
    :initform 0.0)
   (station_dist_y
    :reader station_dist_y
    :initarg :station_dist_y
    :type cl:float
    :initform 0.0))
)

(cl:defclass Course (<Course>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Course>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Course)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name usv_msg-msg:<Course> is deprecated: use usv_msg-msg:Course instead.")))

(cl:ensure-generic-function 'yaw-val :lambda-list '(m))
(cl:defmethod yaw-val ((m <Course>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader usv_msg-msg:yaw-val is deprecated.  Use usv_msg-msg:yaw instead.")
  (yaw m))

(cl:ensure-generic-function 'speed-val :lambda-list '(m))
(cl:defmethod speed-val ((m <Course>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader usv_msg-msg:speed-val is deprecated.  Use usv_msg-msg:speed instead.")
  (speed m))

(cl:ensure-generic-function 'keep_station-val :lambda-list '(m))
(cl:defmethod keep_station-val ((m <Course>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader usv_msg-msg:keep_station-val is deprecated.  Use usv_msg-msg:keep_station instead.")
  (keep_station m))

(cl:ensure-generic-function 'station_yaw-val :lambda-list '(m))
(cl:defmethod station_yaw-val ((m <Course>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader usv_msg-msg:station_yaw-val is deprecated.  Use usv_msg-msg:station_yaw instead.")
  (station_yaw m))

(cl:ensure-generic-function 'station_dist_x-val :lambda-list '(m))
(cl:defmethod station_dist_x-val ((m <Course>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader usv_msg-msg:station_dist_x-val is deprecated.  Use usv_msg-msg:station_dist_x instead.")
  (station_dist_x m))

(cl:ensure-generic-function 'station_dist_y-val :lambda-list '(m))
(cl:defmethod station_dist_y-val ((m <Course>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader usv_msg-msg:station_dist_y-val is deprecated.  Use usv_msg-msg:station_dist_y instead.")
  (station_dist_y m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Course>) ostream)
  "Serializes a message object of type '<Course>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'yaw))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'speed))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'keep_station) 1 0)) ostream)
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'station_yaw))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'station_dist_x))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'station_dist_y))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Course>) istream)
  "Deserializes a message object of type '<Course>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'yaw) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'speed) (roslisp-utils:decode-single-float-bits bits)))
    (cl:setf (cl:slot-value msg 'keep_station) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'station_yaw) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'station_dist_x) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'station_dist_y) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Course>)))
  "Returns string type for a message object of type '<Course>"
  "usv_msg/Course")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Course)))
  "Returns string type for a message object of type 'Course"
  "usv_msg/Course")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Course>)))
  "Returns md5sum for a message object of type '<Course>"
  "0f1618d14a516cca02103ea76395704b")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Course)))
  "Returns md5sum for a message object of type 'Course"
  "0f1618d14a516cca02103ea76395704b")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Course>)))
  "Returns full string definition for message of type '<Course>"
  (cl:format cl:nil "# Command an absolute yaw and velocity.~%~%# Yaw is specified in radians counter-clockwise from true east.~%float32 yaw~%~%# Velocity is specified in meters/s. Negative values correspond to reversing.~%float32 speed~%~%# If true, vessel will maintain station (speed ignored, yaw commanded)~%bool keep_station~%~%# If station keeping, need to keep heading aligned with station_yaw ~%float32 station_yaw~%~%# Distance from vessel to station, used for stationkeeping PID~%float32 station_dist_x~%float32 station_dist_y~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Course)))
  "Returns full string definition for message of type 'Course"
  (cl:format cl:nil "# Command an absolute yaw and velocity.~%~%# Yaw is specified in radians counter-clockwise from true east.~%float32 yaw~%~%# Velocity is specified in meters/s. Negative values correspond to reversing.~%float32 speed~%~%# If true, vessel will maintain station (speed ignored, yaw commanded)~%bool keep_station~%~%# If station keeping, need to keep heading aligned with station_yaw ~%float32 station_yaw~%~%# Distance from vessel to station, used for stationkeeping PID~%float32 station_dist_x~%float32 station_dist_y~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Course>))
  (cl:+ 0
     4
     4
     1
     4
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Course>))
  "Converts a ROS message object to a list"
  (cl:list 'Course
    (cl:cons ':yaw (yaw msg))
    (cl:cons ':speed (speed msg))
    (cl:cons ':keep_station (keep_station msg))
    (cl:cons ':station_yaw (station_yaw msg))
    (cl:cons ':station_dist_x (station_dist_x msg))
    (cl:cons ':station_dist_y (station_dist_y msg))
))
