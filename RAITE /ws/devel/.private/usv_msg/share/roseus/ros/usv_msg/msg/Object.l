;; Auto-generated. Do not edit!


(when (boundp 'usv_msg::Object)
  (if (not (find-package "USV_MSG"))
    (make-package "USV_MSG"))
  (shadow 'Object (find-package "USV_MSG")))
(unless (find-package "USV_MSG::OBJECT")
  (make-package "USV_MSG::OBJECT"))

(in-package "ROS")
;;//! \htmlinclude Object.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(defclass usv_msg::Object
  :super ros::object
  :slots (_frame_id _name _best_guess _types _confidences _pose ))

(defmethod usv_msg::Object
  (:init
   (&key
    ((:frame_id __frame_id) "")
    ((:name __name) "")
    ((:best_guess __best_guess) "")
    ((:types __types) (let (r) (dotimes (i 0) (push "" r)) r))
    ((:confidences __confidences) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:pose __pose) (instance geometry_msgs::Pose :init))
    )
   (send-super :init)
   (setq _frame_id (string __frame_id))
   (setq _name (string __name))
   (setq _best_guess (string __best_guess))
   (setq _types __types)
   (setq _confidences __confidences)
   (setq _pose __pose)
   self)
  (:frame_id
   (&optional __frame_id)
   (if __frame_id (setq _frame_id __frame_id)) _frame_id)
  (:name
   (&optional __name)
   (if __name (setq _name __name)) _name)
  (:best_guess
   (&optional __best_guess)
   (if __best_guess (setq _best_guess __best_guess)) _best_guess)
  (:types
   (&optional __types)
   (if __types (setq _types __types)) _types)
  (:confidences
   (&optional __confidences)
   (if __confidences (setq _confidences __confidences)) _confidences)
  (:pose
   (&rest __pose)
   (if (keywordp (car __pose))
       (send* _pose __pose)
     (progn
       (if __pose (setq _pose (car __pose)))
       _pose)))
  (:serialization-length
   ()
   (+
    ;; string _frame_id
    4 (length _frame_id)
    ;; string _name
    4 (length _name)
    ;; string _best_guess
    4 (length _best_guess)
    ;; string[] _types
    (apply #'+ (mapcar #'(lambda (x) (+ 4 (length x))) _types)) 4
    ;; float64[] _confidences
    (* 8    (length _confidences)) 4
    ;; geometry_msgs/Pose _pose
    (send _pose :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _frame_id
       (write-long (length _frame_id) s) (princ _frame_id s)
     ;; string _name
       (write-long (length _name) s) (princ _name s)
     ;; string _best_guess
       (write-long (length _best_guess) s) (princ _best_guess s)
     ;; string[] _types
     (write-long (length _types) s)
     (dolist (elem _types)
       (write-long (length elem) s) (princ elem s)
       )
     ;; float64[] _confidences
     (write-long (length _confidences) s)
     (dotimes (i (length _confidences))
       (sys::poke (elt _confidences i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; geometry_msgs/Pose _pose
       (send _pose :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _frame_id
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _frame_id (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; string _name
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _name (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; string _best_guess
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _best_guess (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; string[] _types
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _types (make-list n))
     (dotimes (i n)
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setf (elt _types i) (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
     ))
   ;; float64[] _confidences
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _confidences (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _confidences i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; geometry_msgs/Pose _pose
     (send _pose :deserialize buf ptr-) (incf ptr- (send _pose :serialization-length))
   ;;
   self)
  )

(setf (get usv_msg::Object :md5sum-) "dfbbde04b5fb0ebbe12079ff27956a67")
(setf (get usv_msg::Object :datatype-) "usv_msg/Object")
(setf (get usv_msg::Object :definition-)
      "#Objects found in the world
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



(provide :usv_msg/Object "dfbbde04b5fb0ebbe12079ff27956a67")


