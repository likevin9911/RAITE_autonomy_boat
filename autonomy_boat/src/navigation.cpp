/// \file  navigation.cpp 
/// \brief Implementation file for header file navigation.hpp

#include <ros/ros.h>
#include <ros/console.h>
#include <boat_slam/navigation.hpp>
#include <std_msgs/String.h> // For waypoint notifications
#include <algorithm> // For sorting frontiers
#include <cmath> // For std::hypot
#include <boost/thread/lock_guard.hpp> // For boost::lock_guard

/// \brief Check if two Points have almost identical poses
inline static bool operator==(const geometry_msgs::Point& a,
                              const geometry_msgs::Point& b)
{
    double dx = a.x - b.x;
    double dy = a.y - b.y;
    double dist = std::hypot(dx, dy);
    return dist < 0.01;
}

Navigation::Navigation()
    : private_nh_("~"),
      tf_listener_(ros::Duration(10.0)),
      costmap_client_(private_nh_, relative_nh_, &tf_listener_),
      move_base_client_("move_base"),
      prev_dist_(0.0),
      last_markers_count_(0),
      is_waiting_(false)
{
    // Initialize parameters with default values
    private_nh_.param("planner_frequency", planner_freq_, 0.1);
    private_nh_.param("progress_timeout", timeout, 5.0);
    private_nh_.param("visualize", visualize_, true);
    private_nh_.param("potential_scale", potential_scale_, 2.0);
    private_nh_.param("gain_scale", gain_scale_, 2.0);
    private_nh_.param("min_frontier_size", min_frontier_size_, 1.5);

    // New parameters for waiting duration and max frontier distance
    private_nh_.param("waypoint_wait_duration", waypoint_wait_duration_, 10.0); // 10 seconds
    private_nh_.param("max_frontier_distance", max_frontier_distance_, 8.0); // 5 meters

    progress_timeout_ = ros::Duration(timeout);
    search_ = FrontierSearch(costmap_client_.getCostmap(),
                             potential_scale_, gain_scale_, min_frontier_size_);

    if (visualize_)
    {
        marker_array_pub = private_nh_.advertise<visualization_msgs::MarkerArray>("frontiers", 10);
        marker_pub = private_nh_.advertise<visualization_msgs::Marker>("target", 10);
    }

    // Initialize the waypoint notification publisher
    waypoint_notification_pub_ = private_nh_.advertise<std_msgs::String>("waypoint_notifications", 10);

    ROS_INFO("Waiting to connect to move base server");
    move_base_client_.waitForServer();
    ROS_INFO("Connected to move_base server");

    // Initialize the explore timer based on planner frequency
    explore_timer_ = relative_nh_.createTimer(ros::Duration(1.0 / planner_freq_),
                        [this](const ros::TimerEvent&) { makePlan(); });
}

Navigation::~Navigation()
{
    stop();
}

void Navigation::visualizeFrontiers(const std::vector<Frontier> &frontiers)
{
    // Set colors for markers
    std_msgs::ColorRGBA red;
    red.r = 1.0;
    red.g = 0.0;
    red.b = 0.0;
    red.a = 1.0; 

    std_msgs::ColorRGBA blue;
    blue.r = 0.0;
    blue.g = 0.0;
    blue.b = 1.0;
    blue.a = 1.0; 

    ROS_DEBUG("Visualizing %lu frontiers", frontiers.size());

    visualization_msgs::MarkerArray markers_msg;
    std::vector<visualization_msgs::Marker> &markers = markers_msg.markers; 
    visualization_msgs::Marker m;

    m.header.frame_id = costmap_client_.getGlobalFrameID();
    m.header.stamp = ros::Time::now();
    m.ns = "frontiers";
    m.type = visualization_msgs::Marker::POINTS;
    m.scale.x = 0.1;                                                         
    m.scale.y = 0.1;
    m.lifetime = ros::Duration(0);
    m.frame_locked = true;
    m.action = visualization_msgs::Marker::ADD;

    size_t id = 0;

    for (const auto &frontier : frontiers)
    {
        m.id = static_cast<int>(id);
        m.pose.position = geometry_msgs::Point(); // Reset position

        // Assign color based on blacklist status
        if (goalOnBlacklist(frontier.centroid))
        {
            m.color = red;
        }
        else
        {
            m.color = blue; 
        }

        m.points = frontier.points;
        markers.push_back(m);
        ++id;
    }

    size_t cur_marker_count = markers.size();

    // Delete previous unused markers
    m.action = visualization_msgs::Marker::DELETE;
    for (; id < last_markers_count_; ++id)
    {
        m.id = static_cast<int>(id);
        markers.push_back(m);
    }

    last_markers_count_ = cur_marker_count;
    marker_array_pub.publish(markers_msg);
}

void Navigation::makePlan()
{
    if (is_waiting_)
    {
        ROS_DEBUG("Waiting period active. Skipping makePlan.");
        return;
    }

    // Get the current robot pose
    auto pose = costmap_client_.getRobotPose();

    // Find frontiers from the current pose
    auto frontiers = search_.searchFrom(pose.position);
    ROS_DEBUG("Found %lu frontiers", frontiers.size());

    for (size_t i = 0; i < frontiers.size(); ++i)
    {
        ROS_DEBUG("Frontier %zu cost: %f", i, frontiers[i].cost);
    }

    if (frontiers.empty())
    {
        ROS_WARN("No frontiers found. Stopping navigation.");
        stop();
        return;
    }

    // Publish frontiers as visualization markers
    if (visualize_)
    {
        visualizeFrontiers(frontiers);
    }

    // Sort frontiers based on distance from current pose
    std::sort(frontiers.begin(), frontiers.end(),
        [&](const Frontier &a, const Frontier &b) -> bool {
            double dist_a = std::hypot(a.centroid.x - pose.position.x,
                                      a.centroid.y - pose.position.y);
            double dist_b = std::hypot(b.centroid.x - pose.position.x,
                                      b.centroid.y - pose.position.y);
            return dist_a < dist_b;
        });

    // Select the nearest non-blacklisted frontier within the maximum distance
    auto frontier = std::find_if_not(frontiers.begin(), frontiers.end(),
        [&](const Frontier &f) -> bool {
            double dist = std::hypot(f.centroid.x - pose.position.x,
                                     f.centroid.y - pose.position.y);
            return (dist > max_frontier_distance_) || goalOnBlacklist(f.centroid);
        });

    if (frontier == frontiers.end())
    {
        ROS_WARN("No suitable frontiers found within %.2f meters. Stopping navigation.", max_frontier_distance_);
        stop();
        return;
    }

    // Choose the centroid of the selected frontier as the target point
    geometry_msgs::Point target_pose = frontier->centroid;

    // Check if the new goal is the same as the previous one
    bool same_goal = (prev_goal_ == target_pose);

    prev_goal_ = target_pose;

    // Update progress metrics
    if (!same_goal || prev_dist_ > frontier->min_dist)
    {
        last_progress_ = ros::Time::now();
        prev_dist_ = frontier->min_dist;
    }

    // Blacklist the goal if no progress has been made within the timeout
    if (ros::Time::now() - last_progress_ > progress_timeout_)
    {
        frontier_blacklist_.push_back(target_pose);
        ROS_INFO("Marked goal at (%.2f, %.2f) as unreachable.", target_pose.x, target_pose.y);

        // Attempt to select a new goal
        makePlan();
        return;
    }

    if (same_goal)
    {
        ROS_DEBUG("Same goal as previous. Skipping sending a new goal.");
        return;
    }

    // Send the goal to move_base
    move_base_msgs::MoveBaseGoal goal;
    goal.target_pose.pose.position = target_pose;
    goal.target_pose.pose.orientation.w = 1.0; // Facing forward
    goal.target_pose.header.frame_id = costmap_client_.getGlobalFrameID();
    goal.target_pose.header.stamp = ros::Time::now();

    // Initialize and publish a visualization marker for the target pose
    visualization_msgs::Marker marker;
    marker.header.frame_id = costmap_client_.getGlobalFrameID();
    marker.header.stamp = ros::Time::now();
    marker.ns = "target_pose";
    marker.id = 0;
    marker.type = visualization_msgs::Marker::ARROW;
    marker.action = visualization_msgs::Marker::ADD;
    marker.pose.position = target_pose;
    marker.pose.orientation.w = 1.0;
    marker.scale.x = 1.0;
    marker.scale.y = 0.1;
    marker.scale.z = 0.1;
    marker.color.r = 1.0;
    marker.color.g = 0.0;
    marker.color.b = 0.0;
    marker.color.a = 1.0;

    marker_pub.publish(marker);

    ROS_INFO("Moving to goal at (%.2f, %.2f)", target_pose.x, target_pose.y);

    // Send the goal asynchronously with a callback
    move_base_client_.sendGoal(goal, 
        [this, target_pose](const actionlib::SimpleClientGoalState &status, 
                           const move_base_msgs::MoveBaseResultConstPtr &result){
            reachedGoal(status, result, target_pose);
        });

    // Removed blocking sleep to ensure responsiveness
}

bool Navigation::goalOnBlacklist(const geometry_msgs::Point &goal)
{
    constexpr static size_t tolerance = 5;
    costmap_2d::Costmap2D *costmap2d = costmap_client_.getCostmap();

    // Check if the goal is within tolerance of any blacklisted frontier
    for (const auto &frontier_goal : frontier_blacklist_)
    {
        double x_diff = std::fabs(goal.x - frontier_goal.x);
        double y_diff = std::fabs(goal.y - frontier_goal.y);

        if (x_diff < tolerance * costmap2d->getResolution() && 
            y_diff < tolerance * costmap2d->getResolution())
        {
            return true;
        }
    }
    return false;
}

void Navigation::reachedGoal(const actionlib::SimpleClientGoalState &status,
                             const move_base_msgs::MoveBaseResultConstPtr &result,
                             const geometry_msgs::Point &frontier_goal)
{
    ROS_INFO("Reached goal with status: %s", status.toString().c_str());

    if (status == actionlib::SimpleClientGoalState::SUCCEEDED)
    {
        // Publish a notification that the waypoint has been reached
        std_msgs::String notification_msg;
        notification_msg.data = "Waypoint reached... setting up next waypoint!";
        waypoint_notification_pub_.publish(notification_msg);
        ROS_INFO("%s", notification_msg.data.c_str());

        // Start a one-shot timer for the 10-second wait before planning the next waypoint
        is_waiting_ = true;
        waypoint_wait_timer_ = relative_nh_.createTimer(ros::Duration(waypoint_wait_duration_),
            [this](const ros::TimerEvent&) {
                is_waiting_ = false;
                makePlan();
            }, true); // One-shot timer

        return; // Exit the callback to prevent immediate re-planning
    }

    // If the goal was aborted, add it to the blacklist
    if (status == actionlib::SimpleClientGoalState::ABORTED)
    {
        frontier_blacklist_.push_back(frontier_goal);
        ROS_DEBUG("Adding current goal to blacklist.");
    }

    // Schedule immediate re-planning after a short delay
    explore_timer_.stop(); // Ensure the explore timer isn't concurrently running
    explore_timer_ = relative_nh_.createTimer(ros::Duration(1.0), 
        [this](const ros::TimerEvent&) { makePlan(); });
}

void Navigation::stop()
{
    move_base_client_.cancelAllGoals();
    explore_timer_.stop();
    waypoint_wait_timer_.stop();
    ROS_INFO("Finished mapping!");
}

int main(int argc, char** argv)
{
    ros::init(argc, argv, "jackal_slam");
    Navigation navigation;
    ros::spin();
    return 0;
}

/// end file
