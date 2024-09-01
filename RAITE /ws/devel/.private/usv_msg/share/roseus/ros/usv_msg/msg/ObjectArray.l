;; Auto-generated. Do not edit!


(when (boundp 'usv_msg::ObjectArray)
  (if (not (find-package "USV_MSG"))
    (make-package "USV_MSG"))
  (shadow 'ObjectArray (find-package "USV_MSG")))
(unless (find-package "USV_MSG::OBJECTARRAY")
  (make-package "USV_MSG::OBJECTARRAY"))

(in-package "ROS")
;;//! \htmlinclude ObjectArray.msg.html


(defclass usv_msg::ObjectArray
  :super ros::object
  :slots (_objects ))

(defmethod usv_msg::ObjectArray
  (:init
   (&key
    ((:objects __objects) ())
    )
   (send-super :init)
   (setq _objects __objects)
   self)
  (:objects
   (&rest __objects)
   (if (keywordp (car __objects))
       (send* _objects __objects)
     (progn
       (if __objects (setq _objects (car __objects)))
       _objects)))
  (:serialization-length
   ()
   (+
    ;; usv_msg/Object[] _objects
    (apply #'+ (send-all _objects :serialization-length)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; usv_msg/Object[] _objects
     (write-long (length _objects) s)
     (dolist (elem _objects)
       (send elem :serialize s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; usv_msg/Object[] _objects
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _objects (let (r) (dotimes (i n) (push (instance usv_msg::Object :init) r)) r))
     (dolist (elem- _objects)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;;
   self)
  )

(setf (get usv_msg::ObjectArray :md5sum-) "6186a21550e812e683ae3a92e0dc0ab4")
(setf (get usv_msg::ObjectArray :datatype-) "usv_msg/ObjectArray")
(setf (get usv_msg::ObjectArray :definition-)
      "#List of objects
Object[] objects 

================================================================================
MSG: usv_msg/Object
#Objects found in the world
string frame_id
string name
string best_guess
string[] types
float64[] confidences
geometry_msgs/Pose pose

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



(provide :usv_msg/ObjectArray "6186a21550e812e683ae3a92e0dc0ab4")


