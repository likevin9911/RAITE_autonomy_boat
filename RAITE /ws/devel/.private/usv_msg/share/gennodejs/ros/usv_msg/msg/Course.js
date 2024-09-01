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

class Course {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.yaw = null;
      this.speed = null;
      this.keep_station = null;
      this.station_yaw = null;
      this.station_dist_x = null;
      this.station_dist_y = null;
    }
    else {
      if (initObj.hasOwnProperty('yaw')) {
        this.yaw = initObj.yaw
      }
      else {
        this.yaw = 0.0;
      }
      if (initObj.hasOwnProperty('speed')) {
        this.speed = initObj.speed
      }
      else {
        this.speed = 0.0;
      }
      if (initObj.hasOwnProperty('keep_station')) {
        this.keep_station = initObj.keep_station
      }
      else {
        this.keep_station = false;
      }
      if (initObj.hasOwnProperty('station_yaw')) {
        this.station_yaw = initObj.station_yaw
      }
      else {
        this.station_yaw = 0.0;
      }
      if (initObj.hasOwnProperty('station_dist_x')) {
        this.station_dist_x = initObj.station_dist_x
      }
      else {
        this.station_dist_x = 0.0;
      }
      if (initObj.hasOwnProperty('station_dist_y')) {
        this.station_dist_y = initObj.station_dist_y
      }
      else {
        this.station_dist_y = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Course
    // Serialize message field [yaw]
    bufferOffset = _serializer.float32(obj.yaw, buffer, bufferOffset);
    // Serialize message field [speed]
    bufferOffset = _serializer.float32(obj.speed, buffer, bufferOffset);
    // Serialize message field [keep_station]
    bufferOffset = _serializer.bool(obj.keep_station, buffer, bufferOffset);
    // Serialize message field [station_yaw]
    bufferOffset = _serializer.float32(obj.station_yaw, buffer, bufferOffset);
    // Serialize message field [station_dist_x]
    bufferOffset = _serializer.float32(obj.station_dist_x, buffer, bufferOffset);
    // Serialize message field [station_dist_y]
    bufferOffset = _serializer.float32(obj.station_dist_y, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Course
    let len;
    let data = new Course(null);
    // Deserialize message field [yaw]
    data.yaw = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [speed]
    data.speed = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [keep_station]
    data.keep_station = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [station_yaw]
    data.station_yaw = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [station_dist_x]
    data.station_dist_x = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [station_dist_y]
    data.station_dist_y = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 21;
  }

  static datatype() {
    // Returns string type for a message object
    return 'usv_msg/Course';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '0f1618d14a516cca02103ea76395704b';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # Command an absolute yaw and velocity.
    
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
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Course(null);
    if (msg.yaw !== undefined) {
      resolved.yaw = msg.yaw;
    }
    else {
      resolved.yaw = 0.0
    }

    if (msg.speed !== undefined) {
      resolved.speed = msg.speed;
    }
    else {
      resolved.speed = 0.0
    }

    if (msg.keep_station !== undefined) {
      resolved.keep_station = msg.keep_station;
    }
    else {
      resolved.keep_station = false
    }

    if (msg.station_yaw !== undefined) {
      resolved.station_yaw = msg.station_yaw;
    }
    else {
      resolved.station_yaw = 0.0
    }

    if (msg.station_dist_x !== undefined) {
      resolved.station_dist_x = msg.station_dist_x;
    }
    else {
      resolved.station_dist_x = 0.0
    }

    if (msg.station_dist_y !== undefined) {
      resolved.station_dist_y = msg.station_dist_y;
    }
    else {
      resolved.station_dist_y = 0.0
    }

    return resolved;
    }
};

module.exports = Course;
