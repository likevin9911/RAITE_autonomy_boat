;; Auto-generated. Do not edit!


(when (boundp 'usv_msg::WaypointRoute)
  (if (not (find-package "USV_MSG"))
    (make-package "USV_MSG"))
  (shadow 'WaypointRoute (find-package "USV_MSG")))
(unless (find-package "USV_MSG::WAYPOINTROUTE")
  (make-package "USV_MSG::WAYPOINTROUTE"))

(in-package "ROS")
;;//! \htmlinclude WaypointRoute.msg.html


(defclass usv_msg::WaypointRoute
  :super ros::object
  :slots (_waypoints _speed ))

(defmethod usv_msg::WaypointRoute
  (:init
   (&key
    ((:waypoints __waypoints) ())
    ((:speed __speed) 0.0)
    )
   (send-super :init)
   (setq _waypoints __waypoints)
   (setq _speed (float __speed))
   self)
  (:waypoints
   (&rest __waypoints)
   (if (keywordp (car __waypoints))
       (send* _waypoints __waypoints)
     (progn
       (if __waypoints (setq _waypoints (car __waypoints)))
       _waypoints)))
  (:speed
   (&optional __speed)
   (if __speed (setq _speed __speed)) _speed)
  (:serialization-length
   ()
   (+
    ;; usv_msg/Waypoint[] _waypoints
    (apply #'+ (send-all _waypoints :serialization-length)) 4
    ;; float64 _speed
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; usv_msg/Waypoint[] _waypoints
     (write-long (length _waypoints) s)
     (dolist (elem _waypoints)
       (send elem :serialize s)
       )
     ;; float64 _speed
       (sys::poke _speed (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; usv_msg/Waypoint[] _waypoints
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _waypoints (let (r) (dotimes (i n) (push (instance usv_msg::Waypoint :init) r)) r))
     (dolist (elem- _waypoints)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;; float64 _speed
     (setq _speed (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get usv_msg::WaypointRoute :md5sum-) "650bb71476c385be6992ca7ffe1ecd01")
(setf (get usv_msg::WaypointRoute :datatype-) "usv_msg/WaypointRoute")
(setf (get usv_msg::WaypointRoute :definition-)
      "# List of waypoints to follow along route.
usv_msg/Waypoint[] waypoints 

# Speed for course commands, in m/s.
float64 speed

================================================================================
MSG: usv_msg/Waypoint
# Constants describing different waypoint behaviours.
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



(provide :usv_msg/WaypointRoute "650bb71476c385be6992ca7ffe1ecd01")


