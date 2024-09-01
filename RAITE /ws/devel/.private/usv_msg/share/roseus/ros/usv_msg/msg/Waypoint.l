;; Auto-generated. Do not edit!


(when (boundp 'usv_msg::Waypoint)
  (if (not (find-package "USV_MSG"))
    (make-package "USV_MSG"))
  (shadow 'Waypoint (find-package "USV_MSG")))
(unless (find-package "USV_MSG::WAYPOINT")
  (make-package "USV_MSG::WAYPOINT"))

(in-package "ROS")
;;//! \htmlinclude Waypoint.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(intern "*NAV_WAYPOINT*" (find-package "USV_MSG::WAYPOINT"))
(shadow '*NAV_WAYPOINT* (find-package "USV_MSG::WAYPOINT"))
(defconstant usv_msg::Waypoint::*NAV_WAYPOINT* 0)
(intern "*NAV_STATION*" (find-package "USV_MSG::WAYPOINT"))
(shadow '*NAV_STATION* (find-package "USV_MSG::WAYPOINT"))
(defconstant usv_msg::Waypoint::*NAV_STATION* 1)

(defun usv_msg::Waypoint-to-symbol (const)
  (cond
        ((= const 0) 'usv_msg::Waypoint::*NAV_WAYPOINT*)
        ((= const 1) 'usv_msg::Waypoint::*NAV_STATION*)
        (t nil)))

(defclass usv_msg::Waypoint
  :super ros::object
  :slots (_nav_type _pose _station_duration ))

(defmethod usv_msg::Waypoint
  (:init
   (&key
    ((:nav_type __nav_type) 0)
    ((:pose __pose) (instance geometry_msgs::Pose :init))
    ((:station_duration __station_duration) 0.0)
    )
   (send-super :init)
   (setq _nav_type (round __nav_type))
   (setq _pose __pose)
   (setq _station_duration (float __station_duration))
   self)
  (:nav_type
   (&optional __nav_type)
   (if __nav_type (setq _nav_type __nav_type)) _nav_type)
  (:pose
   (&rest __pose)
   (if (keywordp (car __pose))
       (send* _pose __pose)
     (progn
       (if __pose (setq _pose (car __pose)))
       _pose)))
  (:station_duration
   (&optional __station_duration)
   (if __station_duration (setq _station_duration __station_duration)) _station_duration)
  (:serialization-length
   ()
   (+
    ;; uint8 _nav_type
    1
    ;; geometry_msgs/Pose _pose
    (send _pose :serialization-length)
    ;; float32 _station_duration
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _nav_type
       (write-byte _nav_type s)
     ;; geometry_msgs/Pose _pose
       (send _pose :serialize s)
     ;; float32 _station_duration
       (sys::poke _station_duration (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _nav_type
     (setq _nav_type (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; geometry_msgs/Pose _pose
     (send _pose :deserialize buf ptr-) (incf ptr- (send _pose :serialization-length))
   ;; float32 _station_duration
     (setq _station_duration (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get usv_msg::Waypoint :md5sum-) "68be9ca6ba586733f004f0265fb452c4")
(setf (get usv_msg::Waypoint :datatype-) "usv_msg/Waypoint")
(setf (get usv_msg::Waypoint :definition-)
      "# Constants describing different waypoint behaviours.
#   NAV_WAYPOINT: A waypoint for the vesesl to pass through on a route, position required only.
#   NAV_STATION:  A station for the vessel to reach and align a position and yaw, for a duration.

uint8 NAV_WAYPOINT=0     
uint8  NAV_STATION=1

# MANDATORY:
uint8 nav_type           # Type of waypoint, specify with NAV constants above
geometry_msgs/Pose pose  # Desired pose for waypoint/station

# IF NAV_STATION:
float32 station_duration # Time in seconds to keep station, negative is indefinite

================================================================================
MSG: geometry_msgs/Pose
# A representation of pose in free space, composed of position and orientation. 
Point position
Quaternion orientation

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w

")



(provide :usv_msg/Waypoint "68be9ca6ba586733f004f0265fb452c4")


