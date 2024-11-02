/// \file nav.hpp
/// \brief Header file for boat navigation using frontier exploration

#ifndef BOAT_SLAM_NAVIGATION_INCLUDE_GUARD_HPP
#define BOAT_SLAM_NAVIGATION_INCLUDE_GUARD_HPP

#include <ros/ros.h>
#include <ros/console.h>
#include <geometry_msgs/PoseStamped.h>
#include <geometry_msgs/Point.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>
#include <visualization_msgs/MarkerArray.h>
#include <std_msgs/String.h> // For waypoint notifications
#include <boat_slam/costmap.hpp>
#include <boat_slam/frontier_search.hpp> // Include frontier_search.hpp
#include <string>
#include <vector>
#include <tf/transform_listener.h> // Added for tf::TransformListener
#include <boost/thread/lock_guard.hpp> // For boost::lock_guard

class Navigation
{
public:
    /// \brief Default constructor
    Navigation();

    /// \brief Destructor
    ~Navigation();

    /// \brief Stop the robot's motion
    void stop();

private:
    // ROS NodeHandles
    ros::NodeHandle private_nh_;
    ros::NodeHandle relative_nh_;

    // ROS Publishers
    ros::Publisher marker_array_pub;
    ros::Publisher marker_pub;
    ros::Publisher waypoint_notification_pub_; // Publisher for waypoint notifications

    // Transform Listener
    tf::TransformListener tf_listener_;

    // Costmap and Frontier Search
    Costmap costmap_client_;
    FrontierSearch search_;

    // Action Client for move_base
    actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> move_base_client_;

    // ROS Timers
    ros::Timer explore_timer_; // Timer for planning
    ros::Timer waypoint_wait_timer_; // Timer for waiting after reaching a waypoint

    // Parameters
    double planner_freq_;
    double timeout;
    double potential_scale_;
    double gain_scale_;
    double min_frontier_size_;
    double waypoint_wait_duration_; // Duration to wait after reaching a waypoint
    double max_frontier_distance_; // Maximum distance to consider for frontiers

    // State Variables
    std::vector<geometry_msgs::Point> frontier_blacklist_; // List of blacklisted frontiers
    geometry_msgs::Point prev_goal_; // Previous goal position
    double prev_dist_; // Previous distance to a frontier
    ros::Time last_progress_; // Last time progress was made
    size_t last_markers_count_;

    bool is_waiting_; // Flag to indicate if waiting period is active

    // Member Variables (ensure these are declared)
    bool visualize_; // Visualization flag
    ros::Duration progress_timeout_; // Progress timeout duration

    /// \brief Plan the next frontier point to move to
    void makePlan();

    /// \brief Visualize the frontiers
    /// \param frontiers - Vector of frontier points
    void visualizeFrontiers(const std::vector<Frontier> &frontiers);

    /// \brief Callback when a goal is reached
    /// \param status - Status of the goal
    /// \param result - Result of the goal
    /// \param frontier_goal - The frontier point that was targeted
    void reachedGoal(const actionlib::SimpleClientGoalState &status, 
                    const move_base_msgs::MoveBaseResultConstPtr &result,
                    const geometry_msgs::Point &frontier_goal);

    /// \brief Check if a goal is on the blacklist
    /// \param goal - The goal point to check
    /// \return True if the goal is blacklisted, False otherwise
    bool goalOnBlacklist(const geometry_msgs::Point &goal);
};

#endif // BOAT_SLAM_NAVIGATION_INCLUDE_GUARD_HPP

/// end file
