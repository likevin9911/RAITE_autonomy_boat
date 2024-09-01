// Auto-generated. Do not edit!

// (in-package usv_msg.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let Waypoint = require('./Waypoint.js');

//-----------------------------------------------------------

class WaypointRoute {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.waypoints = null;
      this.speed = null;
    }
    else {
      if (initObj.hasOwnProperty('waypoints')) {
        this.waypoints = initObj.waypoints
      }
      else {
        this.waypoints = [];
      }
      if (initObj.hasOwnProperty('speed')) {
        this.speed = initObj.speed
      }
      else {
        this.speed = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type WaypointRoute
    // Serialize message field [waypoints]
    // Serialize the length for message field [waypoints]
    bufferOffset = _serializer.uint32(obj.waypoints.length, buffer, bufferOffset);
    obj.waypoints.forEach((val) => {
      bufferOffset = Waypoint.serialize(val, buffer, bufferOffset);
    });
    // Serialize message field [speed]
    bufferOffset = _serializer.float64(obj.speed, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type WaypointRoute
    let len;
    let data = new WaypointRoute(null);
    // Deserialize message field [waypoints]
    // Deserialize array length for message field [waypoints]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.waypoints = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.waypoints[i] = Waypoint.deserialize(buffer, bufferOffset)
    }
    // Deserialize message field [speed]
    data.speed = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 61 * object.waypoints.length;
    return length + 12;
  }

  static datatype() {
    // Returns string type for a message object
    return 'usv_msg/WaypointRoute';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '650bb71476c385be6992ca7ffe1ecd01';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # List of waypoints to follow along route.
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
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new WaypointRoute(null);
    if (msg.waypoints !== undefined) {
      resolved.waypoints = new Array(msg.waypoints.length);
      for (let i = 0; i < resolved.waypoints.length; ++i) {
        resolved.waypoints[i] = Waypoint.Resolve(msg.waypoints[i]);
      }
    }
    else {
      resolved.waypoints = []
    }

    if (msg.speed !== undefined) {
      resolved.speed = msg.speed;
    }
    else {
      resolved.speed = 0.0
    }

    return resolved;
    }
};

module.exports = WaypointRoute;
