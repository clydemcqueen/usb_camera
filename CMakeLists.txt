cmake_minimum_required(VERSION 2.8.3)
project(usb_camera)

## Find catkin and everything we need in ROS
find_package(catkin REQUIRED COMPONENTS
  cv_bridge
  roscpp
  rospy
  sensor_msgs
)

## Declare a catkin package and export dependencies
catkin_package(
  CATKIN_DEPENDS
  cv_bridge
  roscpp
  rospy
  sensor_msgs
)
