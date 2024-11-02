/// \file FrontierSearch.cpp
/// \brief Implementation file for FrontierSearch.hpp

#include <ros/ros.h>
#include <boat_slam/frontier_search.hpp>
#include <costmap_2d/costmap_2d.h>
#include <costmap_2d/cost_values.h>
#include <geometry_msgs/Point.h>
#include <queue>
#include <limits>
#include <cmath>
#include <mutex>
#include <boost/thread/lock_guard.hpp> // For boost::lock_guard

using costmap_2d::FREE_SPACE;
using costmap_2d::NO_INFORMATION;

// Constructor implementations
FrontierSearch::FrontierSearch()
    : costmap_(nullptr),
      map_(nullptr),
      size_x_(0),
      size_y_(0),
      potential_scale_(1.0),
      gain_scale_(1.0),
      min_frontier_size_(1.0)
{
}

FrontierSearch::FrontierSearch(costmap_2d::Costmap2D *costmap, double potential_scale, double gain_scale, double min_frontier_size)
                          : costmap_(costmap),
                            map_(nullptr),
                            size_x_(0),
                            size_y_(0),
                            potential_scale_(potential_scale),
                            gain_scale_(gain_scale),
                            min_frontier_size_(min_frontier_size)
{
}

// Implement FrontierSearch methods here

std::vector<Frontier> FrontierSearch::searchFrom(const geometry_msgs::Point& pose)
{
    std::vector<Frontier> frontier_list;

    // Check if the robot is inside the costmap
    unsigned int mx, my;
    if(!costmap_->worldToMap(pose.x, pose.y, mx, my))
    {
        ROS_ERROR("Robot is out of the costmap bounds, cannot search for the frontier");
        return frontier_list;
    }

    // Lock the map while searching for new frontiers
    boost::lock_guard<costmap_2d::Costmap2D::mutex_t> lock(*(costmap_->getMutex()));

    map_ = costmap_->getCharMap();
    size_x_ = costmap_->getSizeInCellsX();
    size_y_ = costmap_->getSizeInCellsY();

    // Initialize flags to track visited cells and frontier cells
    std::vector<bool> frontier_flag(size_x_ * size_y_, false);
    std::vector<bool> visited_flag(size_x_ * size_y_, false);

    // BFS search
    std::queue<unsigned int> bfs;

    // Find the closest clear cell to start search
    unsigned int clear, pos = costmap_->getIndex(mx, my);
    if (nearestCell(clear, pos, FREE_SPACE, *costmap_))
    {
        bfs.push(clear);
    }
    else
    {
        bfs.push(pos);
        ROS_WARN("Could not find nearby clear cell to start search");
    }
    visited_flag[bfs.front()] = true;

    while(!bfs.empty())
    {
        unsigned int idx = bfs.front();
        bfs.pop();

        // Iterate over 4-connected neighborhood
        for (unsigned int nbr : nhood4(idx, *costmap_))
        {
            // Add free, unvisited cell in a descending search
            if(map_[nbr] <= map_[idx] && !visited_flag[nbr])
            {
                visited_flag[nbr] = true;
                bfs.push(nbr);
            }
            // Check if cell is a new frontier cell (unvisited, no information, free) 
            else if (isNewFrontierCell(nbr, frontier_flag))
            {
                frontier_flag[nbr] = true;
                Frontier new_frontier = buildNewFrontier(nbr, pos, frontier_flag);

                // Check the frontier size
                if (new_frontier.size * costmap_->getResolution() >= min_frontier_size_)
                {
                    frontier_list.push_back(new_frontier);
                }
            }
        }
    }

    // Compute cost for each frontier
    for (auto &frontier : frontier_list)
    {
        frontier.cost = frontierCost(frontier);
    }

    // Sort the frontiers based on cost (ascending)
    std::sort(frontier_list.begin(), frontier_list.end(),
             [](const Frontier &f1, const Frontier &f2) -> bool
             { return f1.cost < f2.cost; });

    return frontier_list; 
}

Frontier FrontierSearch::buildNewFrontier(unsigned int init_cell, unsigned int ref, std::vector<bool> &frontier_flag)
{
    Frontier res;
    res.centroid.x = 0.0;
    res.centroid.y = 0.0;
    res.size = 1;
    res.min_dist = std::numeric_limits<double>::infinity();

    // Record initial contact point for frontier
    unsigned int ix, iy;
    costmap_->indexToCells(init_cell, ix, iy);
    costmap_->mapToWorld(ix, iy, res.initial.x, res.initial.y); 

    // Push initial cell to the queue
    std::queue<unsigned int> bfs;
    bfs.push(init_cell);

    // Reference position in world frame
    unsigned int rx, ry;
    double ref_x_, ref_y_;
    costmap_->indexToCells(ref, rx, ry);
    costmap_->mapToWorld(rx, ry, ref_x_, ref_y_);

    while (!bfs.empty())
    {
        unsigned int idx = bfs.front();
        bfs.pop();

        // Try to add cell in 8-connected neighborhood frontier
        for (unsigned int nbr : nhood8(idx, *costmap_))
        {
            // Check if neighbor is a potential frontier cell
            if (isNewFrontierCell(nbr, frontier_flag))
            {
                // Mark neighbor point as frontier point
                frontier_flag[nbr] = true;

                // Get world coordinates for neighbor
                unsigned int mx, my;
                double wx, wy;
                costmap_->indexToCells(nbr, mx, my);
                costmap_->mapToWorld(mx, my, wx, wy);

                geometry_msgs::Point pt;
                pt.x = wx;
                pt.y = wy;
                // Add point to point_list
                res.points.push_back(pt);

                // Update frontier size
                res.size++;

                // Update centroid of the frontier
                res.centroid.x += wx;
                res.centroid.y += wy;

                // Determine frontier's distance from reference point (robot)
                double distance = std::hypot(ref_x_ - wx, ref_y_ - wy);

                // Update frontier info
                if (distance < res.min_dist)
                {
                    res.min_dist = distance;
                    res.middle.x = wx;
                    res.middle.y = wy;
                }

                // Add to queue for BFS search
                bfs.push(nbr);
            }
        }
    }

    // Average frontier centroid
    res.centroid.x /= res.size;
    res.centroid.y /= res.size;
    return res;
}   

bool FrontierSearch::isNewFrontierCell(unsigned int idx, const std::vector<bool> &frontier_flag)
{
    // Check if the cell is unknown and not already marked as a frontier
    if(map_[idx] != NO_INFORMATION || frontier_flag[idx])
    {
        return false;
    }

    // A frontier cell should have at least one free space neighbor
    for (unsigned int nbr : nhood4(idx, *costmap_))
    {
        if(map_[nbr] == FREE_SPACE)
        {
            return true;
        }
    }
    return false; 
}

std::vector<unsigned int> FrontierSearch::nhood4(unsigned int idx, const costmap_2d::Costmap2D &costmap)
{
    // Get 4-connected neighborhood indices and check the edges of the map
    std::vector<unsigned int> res;

    unsigned int size_x_ = costmap.getSizeInCellsX();
    unsigned int size_y_ = costmap.getSizeInCellsY();

    if (idx >= size_x_ * size_y_)
    {
        ROS_WARN("Index out of map bounds!");
        return res;
    }

    // West
    if (idx % size_x_ > 0)
    {
        res.push_back(idx - 1);
    }
    // East
    if (idx % size_x_ < size_x_ - 1)
    {
        res.push_back(idx + 1);
    }
    // South
    if (idx >= size_x_)
    {
        res.push_back(idx - size_x_);
    }
    // North
    if (idx < size_x_ * (size_y_ - 1))
    {
        res.push_back(idx + size_x_);
    }
    return res;
}

std::vector<unsigned int> FrontierSearch::nhood8(unsigned int idx, const costmap_2d::Costmap2D &costmap)
{
    // Initialize with 4-connected neighbors
    std::vector<unsigned int> res = nhood4(idx, costmap);

    unsigned int size_x_ = costmap.getSizeInCellsX();
    unsigned int size_y_ = costmap.getSizeInCellsY();

    if (idx >= size_x_ * size_y_)
    {
        ROS_WARN("Index out of map bounds!");
        return res;
    }

    // Northwest
    if (idx % size_x_ > 0 && idx >= size_x_)
    {
        res.push_back(idx - 1 - size_x_);
    }
    // Southwest
    if (idx % size_x_ > 0 && idx < size_x_ * (size_y_ - 1))
    {
        res.push_back(idx - 1 + size_x_);
    }
    // Northeast
    if (idx % size_x_ < size_x_ - 1 && idx >= size_x_)
    {
        res.push_back(idx + 1 - size_x_);
    }
    // Southeast
    if (idx % size_x_ < size_x_ - 1 && idx < size_x_ * (size_y_ - 1))
    {
        res.push_back(idx + 1 + size_x_);
    }
    return res;
}

bool FrontierSearch::nearestCell(unsigned int &result, unsigned int start, unsigned char val, const costmap_2d::Costmap2D &costmap)
{
    // Get map parameters
    const unsigned char *map = costmap.getCharMap();
    const unsigned int size_x_ = costmap.getSizeInCellsX();
    const unsigned int size_y_ = costmap.getSizeInCellsY();

    // Check if the start position is inside the costmap
    if (start >= size_x_ * size_y_)
    {
        return false;
    }

    // Implement BFS to find the nearest cell with the desired value
    std::queue<unsigned int> bfs;
    std::vector<bool> visited_flag(size_x_ * size_y_, false);

    // Push initial cell
    bfs.push(start);
    visited_flag[start] = true;

    // Search for neighborhood cells
    while(!bfs.empty())
    {
        unsigned int idx = bfs.front();
        bfs.pop();

        // Return if the correct value is found
        if(map[idx] == val)
        {
            result = idx;
            return true;
        }

        // Search for neighborhood cells
        std::vector<unsigned int> nh = nhood8(idx, costmap); 
        for(unsigned int neighbor : nh)
        {
            if(!visited_flag[neighbor])
            {
                bfs.push(neighbor);
                visited_flag[neighbor] = true;
            }
        }
    }
    return false;
}

double FrontierSearch::frontierCost(const Frontier &frontier)
{
    // Compute cost based on potential and gain
    return (potential_scale_ * frontier.min_dist * costmap_->getResolution()) -
           (gain_scale_ * frontier.size * costmap_->getResolution());
}
