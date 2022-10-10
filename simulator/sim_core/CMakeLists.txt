cmake_minimum_required(VERSION 3.0.2)
project(sim_core)
find_package(catkin REQUIRED)
catkin_package()
include_directories()

foreach (dir launch)
    install(DIRECTORY ${dir}/
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir}/)
endforeach(dir)

