// Auto-generated. Do not edit!

// (in-package usv_msg.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let geometry_msgs = _finder('geometry_msgs');

//-----------------------------------------------------------

class Waypoint {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.nav_type = null;
      this.pose = null;
      this.station_duration = null;
    }
    else {
      if (initObj.hasOwnProperty('nav_type')) {
        this.nav_type = initObj.nav_type
      }
      else {
        this.nav_type = 0;
      }
      if (initObj.hasOwnProperty('pose')) {
        this.pose = initObj.pose
      }
      else {
        this.pose = new geometry_msgs.msg.Pose();
      }
      if (initObj.hasOwnProperty('station_duration')) {
        this.station_duration = initObj.station_duration
      }
      else {
        this.station_duration = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Waypoint
    // Serialize message field [nav_type]
    bufferOffset = _serializer.uint8(obj.nav_type, buffer, bufferOffset);
    // Serialize message field [pose]
    bufferOffset = geometry_msgs.msg.Pose.serialize(obj.pose, buffer, bufferOffset);
    // Serialize message field [station_duration]
    bufferOffset = _serializer.float32(obj.station_duration, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Waypoint
    let len;
    let data = new Waypoint(null);
    // Deserialize message field [nav_type]
    data.nav_type = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [pose]
    data.pose = geometry_msgs.msg.Pose.deserialize(buffer, bufferOffset);
    // Deserialize message field [station_duration]
    data.station_duration = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 61;
  }

  static datatype() {
    // Returns string type for a message object
    return 'usv_msg/Waypoint';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '68be9ca6ba586733f004f0265fb452c4';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
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
    const resolved = new Waypoint(null);
    if (msg.nav_type !== undefined) {
      resolved.nav_type = msg.nav_type;
    }
    else {
      resolved.nav_type = 0
    }

    if (msg.pose !== undefined) {
      resolved.pose = geometry_msgs.msg.Pose.Resolve(msg.pose)
    }
    else {
      resolved.pose = new geometry_msgs.msg.Pose()
    }

    if (msg.station_duration !== undefined) {
      resolved.station_duration = msg.station_duration;
    }
    else {
      resolved.station_duration = 0.0
    }

    return resolved;
    }
};

// Constants for message
Waypoint.Constants = {
  NAV_WAYPOINT: 0,
  NAV_STATION: 1,
}

module.exports = Waypoint;
