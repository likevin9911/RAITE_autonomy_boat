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

class Object {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.frame_id = null;
      this.name = null;
      this.best_guess = null;
      this.types = null;
      this.confidences = null;
      this.pose = null;
    }
    else {
      if (initObj.hasOwnProperty('frame_id')) {
        this.frame_id = initObj.frame_id
      }
      else {
        this.frame_id = '';
      }
      if (initObj.hasOwnProperty('name')) {
        this.name = initObj.name
      }
      else {
        this.name = '';
      }
      if (initObj.hasOwnProperty('best_guess')) {
        this.best_guess = initObj.best_guess
      }
      else {
        this.best_guess = '';
      }
      if (initObj.hasOwnProperty('types')) {
        this.types = initObj.types
      }
      else {
        this.types = [];
      }
      if (initObj.hasOwnProperty('confidences')) {
        this.confidences = initObj.confidences
      }
      else {
        this.confidences = [];
      }
      if (initObj.hasOwnProperty('pose')) {
        this.pose = initObj.pose
      }
      else {
        this.pose = new geometry_msgs.msg.Pose();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Object
    // Serialize message field [frame_id]
    bufferOffset = _serializer.string(obj.frame_id, buffer, bufferOffset);
    // Serialize message field [name]
    bufferOffset = _serializer.string(obj.name, buffer, bufferOffset);
    // Serialize message field [best_guess]
    bufferOffset = _serializer.string(obj.best_guess, buffer, bufferOffset);
    // Serialize message field [types]
    bufferOffset = _arraySerializer.string(obj.types, buffer, bufferOffset, null);
    // Serialize message field [confidences]
    bufferOffset = _arraySerializer.float64(obj.confidences, buffer, bufferOffset, null);
    // Serialize message field [pose]
    bufferOffset = geometry_msgs.msg.Pose.serialize(obj.pose, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Object
    let len;
    let data = new Object(null);
    // Deserialize message field [frame_id]
    data.frame_id = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [name]
    data.name = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [best_guess]
    data.best_guess = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [types]
    data.types = _arrayDeserializer.string(buffer, bufferOffset, null)
    // Deserialize message field [confidences]
    data.confidences = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [pose]
    data.pose = geometry_msgs.msg.Pose.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += _getByteLength(object.frame_id);
    length += _getByteLength(object.name);
    length += _getByteLength(object.best_guess);
    object.types.forEach((val) => {
      length += 4 + _getByteLength(val);
    });
    length += 8 * object.confidences.length;
    return length + 76;
  }

  static datatype() {
    // Returns string type for a message object
    return 'usv_msg/Object';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'dfbbde04b5fb0ebbe12079ff27956a67';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
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
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Object(null);
    if (msg.frame_id !== undefined) {
      resolved.frame_id = msg.frame_id;
    }
    else {
      resolved.frame_id = ''
    }

    if (msg.name !== undefined) {
      resolved.name = msg.name;
    }
    else {
      resolved.name = ''
    }

    if (msg.best_guess !== undefined) {
      resolved.best_guess = msg.best_guess;
    }
    else {
      resolved.best_guess = ''
    }

    if (msg.types !== undefined) {
      resolved.types = msg.types;
    }
    else {
      resolved.types = []
    }

    if (msg.confidences !== undefined) {
      resolved.confidences = msg.confidences;
    }
    else {
      resolved.confidences = []
    }

    if (msg.pose !== undefined) {
      resolved.pose = geometry_msgs.msg.Pose.Resolve(msg.pose)
    }
    else {
      resolved.pose = new geometry_msgs.msg.Pose()
    }

    return resolved;
    }
};

module.exports = Object;
