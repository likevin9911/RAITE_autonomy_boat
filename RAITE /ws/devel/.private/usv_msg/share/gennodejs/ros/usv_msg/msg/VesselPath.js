// Auto-generated. Do not edit!

// (in-package usv_msg.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let VesselWaypoint = require('./VesselWaypoint.js');

//-----------------------------------------------------------

class VesselPath {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.waypoints = null;
    }
    else {
      if (initObj.hasOwnProperty('waypoints')) {
        this.waypoints = initObj.waypoints
      }
      else {
        this.waypoints = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type VesselPath
    // Serialize message field [waypoints]
    // Serialize the length for message field [waypoints]
    bufferOffset = _serializer.uint32(obj.waypoints.length, buffer, bufferOffset);
    obj.waypoints.forEach((val) => {
      bufferOffset = VesselWaypoint.serialize(val, buffer, bufferOffset);
    });
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type VesselPath
    let len;
    let data = new VesselPath(null);
    // Deserialize message field [waypoints]
    // Deserialize array length for message field [waypoints]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.waypoints = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.waypoints[i] = VesselWaypoint.deserialize(buffer, bufferOffset)
    }
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 64 * object.waypoints.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'usv_msg/VesselPath';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '4259dc009ec92bea4f4406b99ae80570';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    usv_msg/VesselWaypoint[] waypoints
    
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
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new VesselPath(null);
    if (msg.waypoints !== undefined) {
      resolved.waypoints = new Array(msg.waypoints.length);
      for (let i = 0; i < resolved.waypoints.length; ++i) {
        resolved.waypoints[i] = VesselWaypoint.Resolve(msg.waypoints[i]);
      }
    }
    else {
      resolved.waypoints = []
    }

    return resolved;
    }
};

module.exports = VesselPath;
