;; Auto-generated. Do not edit!


(when (boundp 'usv_msg::WaypointReached)
  (if (not (find-package "USV_MSG"))
    (make-package "USV_MSG"))
  (shadow 'WaypointReached (find-package "USV_MSG")))
(unless (find-package "USV_MSG::WAYPOINTREACHED")
  (make-package "USV_MSG::WAYPOINTREACHED"))

(in-package "ROS")
;;//! \htmlinclude WaypointReached.msg.html


(defclass usv_msg::WaypointReached
  :super ros::object
  :slots (_reached _waypoint_id ))

(defmethod usv_msg::WaypointReached
  (:init
   (&key
    ((:reached __reached) nil)
    ((:waypoint_id __waypoint_id) 0)
    )
   (send-super :init)
   (setq _reached __reached)
   (setq _waypoint_id (round __waypoint_id))
   self)
  (:reached
   (&optional (__reached :null))
   (if (not (eq __reached :null)) (setq _reached __reached)) _reached)
  (:waypoint_id
   (&optional __waypoint_id)
   (if __waypoint_id (setq _waypoint_id __waypoint_id)) _waypoint_id)
  (:serialization-length
   ()
   (+
    ;; bool _reached
    1
    ;; int32 _waypoint_id
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _reached
       (if _reached (write-byte -1 s) (write-byte 0 s))
     ;; int32 _waypoint_id
       (write-long _waypoint_id s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _reached
     (setq _reached (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; int32 _waypoint_id
     (setq _waypoint_id (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get usv_msg::WaypointReached :md5sum-) "b886e6b1bcee335c42ff82d1ed3658f4")
(setf (get usv_msg::WaypointReached :datatype-) "usv_msg/WaypointReached")
(setf (get usv_msg::WaypointReached :definition-)
      "bool reached
int32 waypoint_id


")



(provide :usv_msg/WaypointReached "b886e6b1bcee335c42ff82d1ed3658f4")


