;; Auto-generated. Do not edit!


(when (boundp 'usv_msg::VesselWaypoint)
  (if (not (find-package "USV_MSG"))
    (make-package "USV_MSG"))
  (shadow 'VesselWaypoint (find-package "USV_MSG")))
(unless (find-package "USV_MSG::VESSELWAYPOINT")
  (make-package "USV_MSG::VESSELWAYPOINT"))

(in-package "ROS")
;;//! \htmlinclude VesselWaypoint.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(defclass usv_msg::VesselWaypoint
  :super ros::object
  :slots (_pose _tolerance ))

(defmethod usv_msg::VesselWaypoint
  (:init
   (&key
    ((:pose __pose) (instance geometry_msgs::Pose :init))
    ((:tolerance __tolerance) 0.0)
    )
   (send-super :init)
   (setq _pose __pose)
   (setq _tolerance (float __tolerance))
   self)
  (:pose
   (&rest __pose)
   (if (keywordp (car __pose))
       (send* _pose __pose)
     (progn
       (if __pose (setq _pose (car __pose)))
       _pose)))
  (:tolerance
   (&optional __tolerance)
   (if __tolerance (setq _tolerance __tolerance)) _tolerance)
  (:serialization-length
   ()
   (+
    ;; geometry_msgs/Pose _pose
    (send _pose :serialization-length)
    ;; float64 _tolerance
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; geometry_msgs/Pose _pose
       (send _pose :serialize s)
     ;; float64 _tolerance
       (sys::poke _tolerance (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; geometry_msgs/Pose _pose
     (send _pose :deserialize buf ptr-) (incf ptr- (send _pose :serialization-length))
   ;; float64 _tolerance
     (setq _tolerance (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get usv_msg::VesselWaypoint :md5sum-) "a86a362d03a0b4e7c7a4ba71dd826bc6")
(setf (get usv_msg::VesselWaypoint :datatype-) "usv_msg/VesselWaypoint")
(setf (get usv_msg::VesselWaypoint :definition-)
      "# Desired pose of the waypoint
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



(provide :usv_msg/VesselWaypoint "a86a362d03a0b4e7c7a4ba71dd826bc6")


