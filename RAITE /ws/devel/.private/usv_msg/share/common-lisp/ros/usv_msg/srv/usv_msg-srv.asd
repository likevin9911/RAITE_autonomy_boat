
(cl:in-package :asdf)

(defsystem "usv_msg-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :sensor_msgs-msg
)
  :components ((:file "_package")
    (:file "ClassifyBuoy" :depends-on ("_package_ClassifyBuoy"))
    (:file "_package_ClassifyBuoy" :depends-on ("_package"))
    (:file "ClassifyPlacard" :depends-on ("_package_ClassifyPlacard"))
    (:file "_package_ClassifyPlacard" :depends-on ("_package"))
    (:file "ClassifyShape" :depends-on ("_package_ClassifyShape"))
    (:file "_package_ClassifyShape" :depends-on ("_package"))
  ))