;; Auto-generated. Do not edit!


(when (boundp 'usv_msg::Course)
  (if (not (find-package "USV_MSG"))
    (make-package "USV_MSG"))
  (shadow 'Course (find-package "USV_MSG")))
(unless (find-package "USV_MSG::COURSE")
  (make-package "USV_MSG::COURSE"))

(in-package "ROS")
;;//! \htmlinclude Course.msg.html


(defclass usv_msg::Course
  :super ros::object
  :slots (_yaw _speed _keep_station _station_yaw _station_dist_x _station_dist_y ))

(defmethod usv_msg::Course
  (:init
   (&key
    ((:yaw __yaw) 0.0)
    ((:speed __speed) 0.0)
    ((:keep_station __keep_station) nil)
    ((:station_yaw __station_yaw) 0.0)
    ((:station_dist_x __station_dist_x) 0.0)
    ((:station_dist_y __station_dist_y) 0.0)
    )
   (send-super :init)
   (setq _yaw (float __yaw))
   (setq _speed (float __speed))
   (setq _keep_station __keep_station)
   (setq _station_yaw (float __station_yaw))
   (setq _station_dist_x (float __station_dist_x))
   (setq _station_dist_y (float __station_dist_y))
   self)
  (:yaw
   (&optional __yaw)
   (if __yaw (setq _yaw __yaw)) _yaw)
  (:speed
   (&optional __speed)
   (if __speed (setq _speed __speed)) _speed)
  (:keep_station
   (&optional (__keep_station :null))
   (if (not (eq __keep_station :null)) (setq _keep_station __keep_station)) _keep_station)
  (:station_yaw
   (&optional __station_yaw)
   (if __station_yaw (setq _station_yaw __station_yaw)) _station_yaw)
  (:station_dist_x
   (&optional __station_dist_x)
   (if __station_dist_x (setq _station_dist_x __station_dist_x)) _station_dist_x)
  (:station_dist_y
   (&optional __station_dist_y)
   (if __station_dist_y (setq _station_dist_y __station_dist_y)) _station_dist_y)
  (:serialization-length
   ()
   (+
    ;; float32 _yaw
    4
    ;; float32 _speed
    4
    ;; bool _keep_station
    1
    ;; float32 _station_yaw
    4
    ;; float32 _station_dist_x
    4
    ;; float32 _station_dist_y
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _yaw
       (sys::poke _yaw (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _speed
       (sys::poke _speed (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; bool _keep_station
       (if _keep_station (write-byte -1 s) (write-byte 0 s))
     ;; float32 _station_yaw
       (sys::poke _station_yaw (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _station_dist_x
       (sys::poke _station_dist_x (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _station_dist_y
       (sys::poke _station_dist_y (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _yaw
     (setq _yaw (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _speed
     (setq _speed (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; bool _keep_station
     (setq _keep_station (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; float32 _station_yaw
     (setq _station_yaw (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _station_dist_x
     (setq _station_dist_x (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _station_dist_y
     (setq _station_dist_y (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get usv_msg::Course :md5sum-) "0f1618d14a516cca02103ea76395704b")
(setf (get usv_msg::Course :datatype-) "usv_msg/Course")
(setf (get usv_msg::Course :definition-)
      "# Command an absolute yaw and velocity.

# Yaw is specified in radians counter-clockwise from true east.
float32 yaw

# Velocity is specified in meters/s. Negative values correspond to reversing.
float32 speed

# If true, vessel will maintain station (speed ignored, yaw commanded)
bool keep_station

# If station keeping, need to keep heading aligned with station_yaw 
float32 station_yaw

# Distance from vessel to station, used for stationkeeping PID
float32 station_dist_x
float32 station_dist_y
")



(provide :usv_msg/Course "0f1618d14a516cca02103ea76395704b")


