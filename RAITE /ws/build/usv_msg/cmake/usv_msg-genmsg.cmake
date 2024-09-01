# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "usv_msg: 16 messages, 2 services")

set(MSG_I_FLAGS "-Iusv_msg:/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg;-Iusv_msg:/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg;-Istd_msgs:/opt/ros/noetic/share/std_msgs/cmake/../msg;-Igeometry_msgs:/opt/ros/noetic/share/geometry_msgs/cmake/../msg;-Isensor_msgs:/opt/ros/noetic/share/sensor_msgs/cmake/../msg;-Iactionlib_msgs:/opt/ros/noetic/share/actionlib_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(usv_msg_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Course.msg" NAME_WE)
add_custom_target(_usv_msg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "usv_msg" "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Course.msg" ""
)

get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselWaypoint.msg" NAME_WE)
add_custom_target(_usv_msg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "usv_msg" "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselWaypoint.msg" "geometry_msgs/Pose:geometry_msgs/Quaternion:geometry_msgs/Point"
)

get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselPath.msg" NAME_WE)
add_custom_target(_usv_msg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "usv_msg" "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselPath.msg" "usv_msg/VesselWaypoint:geometry_msgs/Pose:geometry_msgs/Quaternion:geometry_msgs/Point"
)

get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Object.msg" NAME_WE)
add_custom_target(_usv_msg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "usv_msg" "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Object.msg" "geometry_msgs/Pose:geometry_msgs/Quaternion:geometry_msgs/Point"
)

get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/ObjectArray.msg" NAME_WE)
add_custom_target(_usv_msg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "usv_msg" "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/ObjectArray.msg" "usv_msg/Object:geometry_msgs/Pose:geometry_msgs/Quaternion:geometry_msgs/Point"
)

get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Waypoint.msg" NAME_WE)
add_custom_target(_usv_msg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "usv_msg" "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Waypoint.msg" "geometry_msgs/Pose:geometry_msgs/Quaternion:geometry_msgs/Point"
)

get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/WaypointRoute.msg" NAME_WE)
add_custom_target(_usv_msg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "usv_msg" "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/WaypointRoute.msg" "geometry_msgs/Pose:geometry_msgs/Quaternion:usv_msg/Waypoint:geometry_msgs/Point"
)

get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Task.msg" NAME_WE)
add_custom_target(_usv_msg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "usv_msg" "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Task.msg" ""
)

get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/WaypointReached.msg" NAME_WE)
add_custom_target(_usv_msg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "usv_msg" "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/WaypointReached.msg" ""
)

get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockAction.msg" NAME_WE)
add_custom_target(_usv_msg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "usv_msg" "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockAction.msg" "actionlib_msgs/GoalID:usv_msg/DockActionResult:usv_msg/DockActionFeedback:usv_msg/DockFeedback:std_msgs/Header:geometry_msgs/Pose:geometry_msgs/Quaternion:usv_msg/DockGoal:usv_msg/DockActionGoal:usv_msg/DockResult:actionlib_msgs/GoalStatus:geometry_msgs/Point"
)

get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionGoal.msg" NAME_WE)
add_custom_target(_usv_msg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "usv_msg" "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionGoal.msg" "actionlib_msgs/GoalID:std_msgs/Header:geometry_msgs/Pose:geometry_msgs/Quaternion:usv_msg/DockGoal:geometry_msgs/Point"
)

get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionResult.msg" NAME_WE)
add_custom_target(_usv_msg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "usv_msg" "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionResult.msg" "actionlib_msgs/GoalID:actionlib_msgs/GoalStatus:usv_msg/DockResult:std_msgs/Header"
)

get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionFeedback.msg" NAME_WE)
add_custom_target(_usv_msg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "usv_msg" "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionFeedback.msg" "actionlib_msgs/GoalID:usv_msg/DockFeedback:actionlib_msgs/GoalStatus:std_msgs/Header"
)

get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockGoal.msg" NAME_WE)
add_custom_target(_usv_msg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "usv_msg" "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockGoal.msg" "geometry_msgs/Pose:geometry_msgs/Quaternion:geometry_msgs/Point"
)

get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockResult.msg" NAME_WE)
add_custom_target(_usv_msg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "usv_msg" "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockResult.msg" ""
)

get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockFeedback.msg" NAME_WE)
add_custom_target(_usv_msg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "usv_msg" "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockFeedback.msg" ""
)

get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/srv/ClassifyBuoy.srv" NAME_WE)
add_custom_target(_usv_msg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "usv_msg" "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/srv/ClassifyBuoy.srv" "sensor_msgs/Image:std_msgs/Header"
)

get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/srv/ClassifyPlacard.srv" NAME_WE)
add_custom_target(_usv_msg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "usv_msg" "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/srv/ClassifyPlacard.srv" "sensor_msgs/Image:std_msgs/Header"
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Course.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/usv_msg
)
_generate_msg_cpp(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselWaypoint.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/usv_msg
)
_generate_msg_cpp(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselPath.msg"
  "${MSG_I_FLAGS}"
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselWaypoint.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/usv_msg
)
_generate_msg_cpp(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Object.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/usv_msg
)
_generate_msg_cpp(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/ObjectArray.msg"
  "${MSG_I_FLAGS}"
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Object.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/usv_msg
)
_generate_msg_cpp(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Waypoint.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/usv_msg
)
_generate_msg_cpp(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/WaypointRoute.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Waypoint.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/usv_msg
)
_generate_msg_cpp(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Task.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/usv_msg
)
_generate_msg_cpp(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/WaypointReached.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/usv_msg
)
_generate_msg_cpp(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionResult.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionFeedback.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockFeedback.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockGoal.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionGoal.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockResult.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/usv_msg
)
_generate_msg_cpp(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockGoal.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/usv_msg
)
_generate_msg_cpp(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockResult.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/usv_msg
)
_generate_msg_cpp(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockFeedback.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/usv_msg
)
_generate_msg_cpp(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/usv_msg
)
_generate_msg_cpp(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/usv_msg
)
_generate_msg_cpp(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockFeedback.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/usv_msg
)

### Generating Services
_generate_srv_cpp(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/srv/ClassifyBuoy.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/sensor_msgs/cmake/../msg/Image.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/usv_msg
)
_generate_srv_cpp(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/srv/ClassifyPlacard.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/sensor_msgs/cmake/../msg/Image.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/usv_msg
)

### Generating Module File
_generate_module_cpp(usv_msg
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/usv_msg
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(usv_msg_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(usv_msg_generate_messages usv_msg_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Course.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_cpp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselWaypoint.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_cpp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselPath.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_cpp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Object.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_cpp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/ObjectArray.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_cpp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Waypoint.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_cpp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/WaypointRoute.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_cpp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Task.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_cpp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/WaypointReached.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_cpp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockAction.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_cpp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionGoal.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_cpp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionResult.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_cpp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionFeedback.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_cpp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockGoal.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_cpp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockResult.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_cpp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockFeedback.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_cpp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/srv/ClassifyBuoy.srv" NAME_WE)
add_dependencies(usv_msg_generate_messages_cpp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/srv/ClassifyPlacard.srv" NAME_WE)
add_dependencies(usv_msg_generate_messages_cpp _usv_msg_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(usv_msg_gencpp)
add_dependencies(usv_msg_gencpp usv_msg_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS usv_msg_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Course.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/usv_msg
)
_generate_msg_eus(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselWaypoint.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/usv_msg
)
_generate_msg_eus(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselPath.msg"
  "${MSG_I_FLAGS}"
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselWaypoint.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/usv_msg
)
_generate_msg_eus(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Object.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/usv_msg
)
_generate_msg_eus(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/ObjectArray.msg"
  "${MSG_I_FLAGS}"
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Object.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/usv_msg
)
_generate_msg_eus(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Waypoint.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/usv_msg
)
_generate_msg_eus(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/WaypointRoute.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Waypoint.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/usv_msg
)
_generate_msg_eus(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Task.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/usv_msg
)
_generate_msg_eus(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/WaypointReached.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/usv_msg
)
_generate_msg_eus(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionResult.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionFeedback.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockFeedback.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockGoal.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionGoal.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockResult.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/usv_msg
)
_generate_msg_eus(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockGoal.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/usv_msg
)
_generate_msg_eus(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockResult.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/usv_msg
)
_generate_msg_eus(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockFeedback.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/usv_msg
)
_generate_msg_eus(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/usv_msg
)
_generate_msg_eus(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/usv_msg
)
_generate_msg_eus(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockFeedback.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/usv_msg
)

### Generating Services
_generate_srv_eus(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/srv/ClassifyBuoy.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/sensor_msgs/cmake/../msg/Image.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/usv_msg
)
_generate_srv_eus(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/srv/ClassifyPlacard.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/sensor_msgs/cmake/../msg/Image.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/usv_msg
)

### Generating Module File
_generate_module_eus(usv_msg
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/usv_msg
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(usv_msg_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(usv_msg_generate_messages usv_msg_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Course.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_eus _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselWaypoint.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_eus _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselPath.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_eus _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Object.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_eus _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/ObjectArray.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_eus _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Waypoint.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_eus _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/WaypointRoute.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_eus _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Task.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_eus _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/WaypointReached.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_eus _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockAction.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_eus _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionGoal.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_eus _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionResult.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_eus _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionFeedback.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_eus _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockGoal.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_eus _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockResult.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_eus _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockFeedback.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_eus _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/srv/ClassifyBuoy.srv" NAME_WE)
add_dependencies(usv_msg_generate_messages_eus _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/srv/ClassifyPlacard.srv" NAME_WE)
add_dependencies(usv_msg_generate_messages_eus _usv_msg_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(usv_msg_geneus)
add_dependencies(usv_msg_geneus usv_msg_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS usv_msg_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Course.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/usv_msg
)
_generate_msg_lisp(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselWaypoint.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/usv_msg
)
_generate_msg_lisp(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselPath.msg"
  "${MSG_I_FLAGS}"
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselWaypoint.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/usv_msg
)
_generate_msg_lisp(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Object.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/usv_msg
)
_generate_msg_lisp(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/ObjectArray.msg"
  "${MSG_I_FLAGS}"
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Object.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/usv_msg
)
_generate_msg_lisp(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Waypoint.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/usv_msg
)
_generate_msg_lisp(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/WaypointRoute.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Waypoint.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/usv_msg
)
_generate_msg_lisp(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Task.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/usv_msg
)
_generate_msg_lisp(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/WaypointReached.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/usv_msg
)
_generate_msg_lisp(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionResult.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionFeedback.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockFeedback.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockGoal.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionGoal.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockResult.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/usv_msg
)
_generate_msg_lisp(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockGoal.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/usv_msg
)
_generate_msg_lisp(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockResult.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/usv_msg
)
_generate_msg_lisp(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockFeedback.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/usv_msg
)
_generate_msg_lisp(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/usv_msg
)
_generate_msg_lisp(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/usv_msg
)
_generate_msg_lisp(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockFeedback.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/usv_msg
)

### Generating Services
_generate_srv_lisp(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/srv/ClassifyBuoy.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/sensor_msgs/cmake/../msg/Image.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/usv_msg
)
_generate_srv_lisp(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/srv/ClassifyPlacard.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/sensor_msgs/cmake/../msg/Image.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/usv_msg
)

### Generating Module File
_generate_module_lisp(usv_msg
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/usv_msg
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(usv_msg_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(usv_msg_generate_messages usv_msg_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Course.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_lisp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselWaypoint.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_lisp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselPath.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_lisp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Object.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_lisp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/ObjectArray.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_lisp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Waypoint.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_lisp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/WaypointRoute.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_lisp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Task.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_lisp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/WaypointReached.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_lisp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockAction.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_lisp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionGoal.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_lisp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionResult.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_lisp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionFeedback.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_lisp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockGoal.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_lisp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockResult.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_lisp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockFeedback.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_lisp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/srv/ClassifyBuoy.srv" NAME_WE)
add_dependencies(usv_msg_generate_messages_lisp _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/srv/ClassifyPlacard.srv" NAME_WE)
add_dependencies(usv_msg_generate_messages_lisp _usv_msg_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(usv_msg_genlisp)
add_dependencies(usv_msg_genlisp usv_msg_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS usv_msg_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Course.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/usv_msg
)
_generate_msg_nodejs(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselWaypoint.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/usv_msg
)
_generate_msg_nodejs(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselPath.msg"
  "${MSG_I_FLAGS}"
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselWaypoint.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/usv_msg
)
_generate_msg_nodejs(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Object.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/usv_msg
)
_generate_msg_nodejs(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/ObjectArray.msg"
  "${MSG_I_FLAGS}"
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Object.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/usv_msg
)
_generate_msg_nodejs(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Waypoint.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/usv_msg
)
_generate_msg_nodejs(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/WaypointRoute.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Waypoint.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/usv_msg
)
_generate_msg_nodejs(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Task.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/usv_msg
)
_generate_msg_nodejs(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/WaypointReached.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/usv_msg
)
_generate_msg_nodejs(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionResult.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionFeedback.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockFeedback.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockGoal.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionGoal.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockResult.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/usv_msg
)
_generate_msg_nodejs(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockGoal.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/usv_msg
)
_generate_msg_nodejs(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockResult.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/usv_msg
)
_generate_msg_nodejs(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockFeedback.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/usv_msg
)
_generate_msg_nodejs(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/usv_msg
)
_generate_msg_nodejs(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/usv_msg
)
_generate_msg_nodejs(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockFeedback.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/usv_msg
)

### Generating Services
_generate_srv_nodejs(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/srv/ClassifyBuoy.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/sensor_msgs/cmake/../msg/Image.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/usv_msg
)
_generate_srv_nodejs(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/srv/ClassifyPlacard.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/sensor_msgs/cmake/../msg/Image.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/usv_msg
)

### Generating Module File
_generate_module_nodejs(usv_msg
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/usv_msg
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(usv_msg_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(usv_msg_generate_messages usv_msg_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Course.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_nodejs _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselWaypoint.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_nodejs _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselPath.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_nodejs _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Object.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_nodejs _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/ObjectArray.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_nodejs _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Waypoint.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_nodejs _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/WaypointRoute.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_nodejs _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Task.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_nodejs _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/WaypointReached.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_nodejs _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockAction.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_nodejs _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionGoal.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_nodejs _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionResult.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_nodejs _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionFeedback.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_nodejs _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockGoal.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_nodejs _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockResult.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_nodejs _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockFeedback.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_nodejs _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/srv/ClassifyBuoy.srv" NAME_WE)
add_dependencies(usv_msg_generate_messages_nodejs _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/srv/ClassifyPlacard.srv" NAME_WE)
add_dependencies(usv_msg_generate_messages_nodejs _usv_msg_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(usv_msg_gennodejs)
add_dependencies(usv_msg_gennodejs usv_msg_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS usv_msg_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Course.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/usv_msg
)
_generate_msg_py(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselWaypoint.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/usv_msg
)
_generate_msg_py(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselPath.msg"
  "${MSG_I_FLAGS}"
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselWaypoint.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/usv_msg
)
_generate_msg_py(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Object.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/usv_msg
)
_generate_msg_py(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/ObjectArray.msg"
  "${MSG_I_FLAGS}"
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Object.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/usv_msg
)
_generate_msg_py(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Waypoint.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/usv_msg
)
_generate_msg_py(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/WaypointRoute.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Waypoint.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/usv_msg
)
_generate_msg_py(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Task.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/usv_msg
)
_generate_msg_py(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/WaypointReached.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/usv_msg
)
_generate_msg_py(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionResult.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionFeedback.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockFeedback.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockGoal.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionGoal.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockResult.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/usv_msg
)
_generate_msg_py(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockGoal.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/usv_msg
)
_generate_msg_py(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockResult.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/usv_msg
)
_generate_msg_py(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockFeedback.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/usv_msg
)
_generate_msg_py(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/usv_msg
)
_generate_msg_py(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/usv_msg
)
_generate_msg_py(usv_msg
  "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockFeedback.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/usv_msg
)

### Generating Services
_generate_srv_py(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/srv/ClassifyBuoy.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/sensor_msgs/cmake/../msg/Image.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/usv_msg
)
_generate_srv_py(usv_msg
  "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/srv/ClassifyPlacard.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/sensor_msgs/cmake/../msg/Image.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/usv_msg
)

### Generating Module File
_generate_module_py(usv_msg
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/usv_msg
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(usv_msg_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(usv_msg_generate_messages usv_msg_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Course.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_py _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselWaypoint.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_py _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/VesselPath.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_py _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Object.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_py _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/ObjectArray.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_py _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Waypoint.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_py _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/WaypointRoute.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_py _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/Task.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_py _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/msg/WaypointReached.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_py _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockAction.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_py _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionGoal.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_py _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionResult.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_py _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockActionFeedback.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_py _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockGoal.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_py _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockResult.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_py _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/devel/.private/usv_msg/share/usv_msg/msg/DockFeedback.msg" NAME_WE)
add_dependencies(usv_msg_generate_messages_py _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/srv/ClassifyBuoy.srv" NAME_WE)
add_dependencies(usv_msg_generate_messages_py _usv_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sinloops/catkin_ws/src/autonomy_boat_sim/usv_vrx/usv_msg/srv/ClassifyPlacard.srv" NAME_WE)
add_dependencies(usv_msg_generate_messages_py _usv_msg_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(usv_msg_genpy)
add_dependencies(usv_msg_genpy usv_msg_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS usv_msg_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/usv_msg)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/usv_msg
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(usv_msg_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()
if(TARGET geometry_msgs_generate_messages_cpp)
  add_dependencies(usv_msg_generate_messages_cpp geometry_msgs_generate_messages_cpp)
endif()
if(TARGET sensor_msgs_generate_messages_cpp)
  add_dependencies(usv_msg_generate_messages_cpp sensor_msgs_generate_messages_cpp)
endif()
if(TARGET actionlib_msgs_generate_messages_cpp)
  add_dependencies(usv_msg_generate_messages_cpp actionlib_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/usv_msg)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/usv_msg
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(usv_msg_generate_messages_eus std_msgs_generate_messages_eus)
endif()
if(TARGET geometry_msgs_generate_messages_eus)
  add_dependencies(usv_msg_generate_messages_eus geometry_msgs_generate_messages_eus)
endif()
if(TARGET sensor_msgs_generate_messages_eus)
  add_dependencies(usv_msg_generate_messages_eus sensor_msgs_generate_messages_eus)
endif()
if(TARGET actionlib_msgs_generate_messages_eus)
  add_dependencies(usv_msg_generate_messages_eus actionlib_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/usv_msg)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/usv_msg
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(usv_msg_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()
if(TARGET geometry_msgs_generate_messages_lisp)
  add_dependencies(usv_msg_generate_messages_lisp geometry_msgs_generate_messages_lisp)
endif()
if(TARGET sensor_msgs_generate_messages_lisp)
  add_dependencies(usv_msg_generate_messages_lisp sensor_msgs_generate_messages_lisp)
endif()
if(TARGET actionlib_msgs_generate_messages_lisp)
  add_dependencies(usv_msg_generate_messages_lisp actionlib_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/usv_msg)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/usv_msg
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(usv_msg_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()
if(TARGET geometry_msgs_generate_messages_nodejs)
  add_dependencies(usv_msg_generate_messages_nodejs geometry_msgs_generate_messages_nodejs)
endif()
if(TARGET sensor_msgs_generate_messages_nodejs)
  add_dependencies(usv_msg_generate_messages_nodejs sensor_msgs_generate_messages_nodejs)
endif()
if(TARGET actionlib_msgs_generate_messages_nodejs)
  add_dependencies(usv_msg_generate_messages_nodejs actionlib_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/usv_msg)
  install(CODE "execute_process(COMMAND \"/usr/bin/python3\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/usv_msg\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/usv_msg
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(usv_msg_generate_messages_py std_msgs_generate_messages_py)
endif()
if(TARGET geometry_msgs_generate_messages_py)
  add_dependencies(usv_msg_generate_messages_py geometry_msgs_generate_messages_py)
endif()
if(TARGET sensor_msgs_generate_messages_py)
  add_dependencies(usv_msg_generate_messages_py sensor_msgs_generate_messages_py)
endif()
if(TARGET actionlib_msgs_generate_messages_py)
  add_dependencies(usv_msg_generate_messages_py actionlib_msgs_generate_messages_py)
endif()
