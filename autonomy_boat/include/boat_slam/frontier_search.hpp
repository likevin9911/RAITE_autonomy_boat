/// \file FrontierSearch.hpp
/// \brief Header file for FrontierSearch class

#ifndef BOAT_SLAM_FRONTIER_SEARCH_INCLUDE_GUARD_HPP
#define BOAT_SLAM_FRONTIER_SEARCH_INCLUDE_GUARD_HPP

#include <ros/ros.h>
#include <costmap_2d/costmap_2d.h>
#include <geometry_msgs/Point.h>
#include <geometry_msgs/PointStamped.h>
#include <vector>
#include <mutex>

// Forward declare if necessary

/// \brief Struct to store frontier information
struct Frontier
{
    unsigned int size;                        ///< Frontier size (number of cells)
    double min_dist;                          ///< Minimum distance of frontier from the reference point
    double cost;                              ///< Cost associated with the frontier
    geometry_msgs::Point initial;             ///< Initial point of the frontier
    geometry_msgs::Point centroid;            ///< Centroid of the frontier
    geometry_msgs::Point middle;              ///< Middle point of the frontier
    std::vector<geometry_msgs::Point> points; ///< Vector of points constituting the frontier
};

/// \brief Class for frontier search within a costmap
class FrontierSearch
{
public:
    FrontierSearch();
    
    /// \brief Constructor for FrontierSearch
    /// \param costmap - Pointer to the costmap
    /// \param potential_scale - Scaling factor for potential-based cost
    /// \param gain_scale - Scaling factor for gain-based cost
    /// \param min_frontier_size - Minimum size of a frontier to be considered valid
    FrontierSearch(costmap_2d::Costmap2D *costmap, double potential_scale, double gain_scale, double min_frontier_size);

    /// \brief Search for frontiers starting from a given pose
    /// \param pose - Position of the robot
    /// \return Vector of identified frontiers
    std::vector<Frontier> searchFrom(const geometry_msgs::Point& pose);

private:
    /// \brief Builds a new frontier from an initial cell
    /// \param init_cell - Starting cell index
    /// \param ref - Reference cell index
    /// \param frontier_flag - Flag to track visited cells
    /// \return Frontier structure
    Frontier buildNewFrontier(unsigned int init_cell, unsigned int ref, std::vector<bool> &frontier_flag);

    /// \brief Evaluates if a cell is a valid candidate for a new frontier
    /// \param idx - Cell index
    /// \param frontier_flag - Flag to check if the cell is unvisited
    /// \return True if valid, False otherwise
    bool isNewFrontierCell(unsigned int idx, const std::vector<bool> &frontier_flag);

    /// \brief Computes the cost of a frontier
    /// \param frontier - Frontier structure
    /// \return Computed cost
    double frontierCost(const Frontier &frontier);

    /// \brief Determines 4-connected neighborhood of an input cell
    /// \param idx - Cell index
    /// \param costmap - Reference to the costmap
    /// \return Vector of 4-connected neighbor cell indices
    std::vector<unsigned int> nhood4(unsigned int idx, const costmap_2d::Costmap2D &costmap);

    /// \brief Determines 8-connected neighborhood of an input cell
    /// \param idx - Cell index
    /// \param costmap - Reference to the costmap
    /// \return Vector of 8-connected neighbor cell indices
    std::vector<unsigned int> nhood8(unsigned int idx, const costmap_2d::Costmap2D &costmap);

    /// \brief Finds the nearest cell with a specific value using BFS
    /// \param result - Reference to store the found cell index
    /// \param start - Starting cell index
    /// \param val - Desired cell value
    /// \param costmap - Reference to the costmap
    /// \return True if found, False otherwise
    bool nearestCell(unsigned int &result, unsigned int start, unsigned char val, const costmap_2d::Costmap2D &costmap);

    /// \brief Finds a new frontier in the costmap
    /// \param start - Starting point
    /// \return Vector of frontiers found
    std::vector<Frontier> findFrontiers(unsigned int start, const costmap_2d::Costmap2D &costmap);

    costmap_2d::Costmap2D *costmap_; ///< Pointer to the costmap

    unsigned char *map_;               ///< Pointer to the costmap data

    unsigned int size_x_;              ///< Size of the costmap in X
    unsigned int size_y_;              ///< Size of the costmap in Y

    double potential_scale_;           ///< Scaling factor for potential-based cost
    double gain_scale_;                ///< Scaling factor for gain-based cost
    double min_frontier_size_;         ///< Minimum size of a frontier to be considered valid
};

#endif // BOAT_SLAM_FRONTIER_SEARCH_INCLUDE_GUARD_HPP

/// end file
