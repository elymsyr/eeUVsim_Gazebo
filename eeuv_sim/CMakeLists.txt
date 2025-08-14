cmake_minimum_required(VERSION 3.5.0)
project(eeuv_sim)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()
# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(control_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(std_msgs REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(eeuv_sim_interfaces)

# This installs the scripts directory as a proper Python package
# so that imports like "from dynamics.wingDynamics" will work.
ament_python_install_package(scripts)

install(DIRECTORY
  launch
  data
  urdf
  worlds
  models
  DESTINATION share/${PROJECT_NAME}/
)

# This installs your nodes as executables so ROS can find and run them.
file(GLOB_RECURSE SCRIPT_FILES
    "scripts/*.py"
    "scripts/actuator/*.py"
    "scripts/dynamics/*.py"
    "scripts/RL/*.py"
)

install(PROGRAMS ${SCRIPT_FILES}
    DESTINATION lib/${PROJECT_NAME}
)

ament_package()