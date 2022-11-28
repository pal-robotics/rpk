cmake_minimum_required(VERSION 3.0.2)
project(pal_create_app)

find_package(catkin REQUIRED
    actionlib
    hri_actions_msgs
    )

catkin_python_setup()
catkin_package()

