// Auto-generated. Do not edit!

// (in-package usv_msg.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class WaypointReached {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.reached = null;
      this.waypoint_id = null;
    }
    else {
      if (initObj.hasOwnProperty('reached')) {
        this.reached = initObj.reached
      }
      else {
        this.reached = false;
      }
      if (initObj.hasOwnProperty('waypoint_id')) {
        this.waypoint_id = initObj.waypoint_id
      }
      else {
        this.waypoint_id = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type WaypointReached
    // Serialize message field [reached]
    bufferOffset = _serializer.bool(obj.reached, buffer, bufferOffset);
    // Serialize message field [waypoint_id]
    bufferOffset = _serializer.int32(obj.waypoint_id, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type WaypointReached
    let len;
    let data = new WaypointReached(null);
    // Deserialize message field [reached]
    data.reached = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [waypoint_id]
    data.waypoint_id = _deserializer.int32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 5;
  }

  static datatype() {
    // Returns string type for a message object
    return 'usv_msg/WaypointReached';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'b886e6b1bcee335c42ff82d1ed3658f4';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    bool reached
    int32 waypoint_id
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new WaypointReached(null);
    if (msg.reached !== undefined) {
      resolved.reached = msg.reached;
    }
    else {
      resolved.reached = false
    }

    if (msg.waypoint_id !== undefined) {
      resolved.waypoint_id = msg.waypoint_id;
    }
    else {
      resolved.waypoint_id = 0
    }

    return resolved;
    }
};

module.exports = WaypointReached;
