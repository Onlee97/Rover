# Rover
This project aims to create an mobile robot that can navigate autonomously any indoor environment.
This repo contains the core codes of the robot, and also neccessary instruction for anyone that interested in replicate or further develop this robot

**Hardware** 
*Version 3*
The robot has 4 DC motors, controlled by an L298N (Motor Driver)\
The Motor Driver is controlled by an Arduino, which can generate PWM signal to control the speed of Motor.\
The CPU of the robot is a *Jetson Nano*, which performs core processing tasks, and communicate with the Arduino via Serial.\

**Software**
*Prerequisite*
OpenCV.\
ROS.\
Intel Realsense.\

**Flashing the Jetson OS**
(https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit)
