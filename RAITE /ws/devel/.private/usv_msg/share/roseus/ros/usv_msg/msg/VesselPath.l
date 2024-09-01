;; Auto-generated. Do not edit!


(when (boundp 'usv_msg::VesselPath)
  (if (not (find-package "USV_MSG"))
    (make-package "USV_MSG"))
  (shadow 'VesselPath (find-package "USV_MSG")))
(unless (find-package "USV_MSG::VESSELPATH")
  (make-package "USV_MSG::VESSELPATH"))

(in-package "ROS")
;;//! \htmlinclude VesselPath.msg.html


(defclass usv_msg::VesselPath
  :super ros::object
  :slots (_waypoints ))

(defmethod usv_msg::VesselPath
  (:init
   (&key
    ((:waypoints __waypoints) ())
    )
   (send-super :init)
   (setq _waypoints __waypoints)
   self)
  (:waypoints
   (&rest __waypoints)
   (if (keywordp (car __waypoints))
       (send* _waypoints __waypoints)
     (progn
       (if __waypoints (setq _waypoints (car __waypoints)))
       _waypoints)))
  (:serialization-length
   ()
   (+
    ;; usv_msg/VesselWaypoint[] _waypoints
    (apply #'+ (send-all _waypoints :serialization-length)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; usv_msg/VesselWaypoint[] _waypoints
     (write-long (length _waypoints) s)
     (dolist (elem _waypoints)
       (send elem :serialize s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; usv_msg/VesselWaypoint[] _waypoints
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _waypoints (let (r) (dotimes (i n) (push (instance usv_msg::VesselWaypoint :init) r)) r))
     (dolist (elem- _waypoints)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;;
   self)
  )

(setf (get usv_msg::VesselPath :md5sum-) "4259dc009ec92bea4f4406b99ae80570")
(setf (get usv_msg::VesselPath :datatype-) "usv_msg/VesselPath")
(setf (get usv_msg::VesselPath :definition-)
      "usv_msg/VesselWaypoint[] waypoints

================================================================================
MSG: usv_msg/VesselWaypoint
# Desired pose of the waypoint
geometry_msgs/Pose pose
# Tolerance on the waypoint
float64 tolerance

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



(provide :usv_msg/VesselPath "4259dc009ec92bea4f4406b99ae80570")


