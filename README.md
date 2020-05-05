# Rover
This project aims to create an mobile robot that can navigate autonomously any indoor environment.
This repo contains the core codes of the robot, and also neccessary instruction for anyone that interested in replicate or further develop this robot

**Hardware**\ 
*Version 3*\
The robot has 4 DC motors, controlled by an L298N (Motor Driver)\
The Motor Driver is controlled by an Arduino, which can generate PWM signal to control the speed of Motor.\
The CPU of the robot is a *Jetson Nano*, which performs core processing tasks, and communicate with the Arduino via Serial.

**Software**\
*Prerequisite*\
OpenCV.\
ROS.\
Intel Realsense.

**Flashing the Jetson OS**\
(https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit)
Using NVIDIA L4T32.3.1, JetPack 4.3 

**Install OpenCV**\
The JetPack (Jetson OS) comes with a built in OpenCV (installed in /usr/ folder). However, this OpenCV doesn't come with CUDA support. In order to have a more customized OpenCV, we should built it from source.
*Step 0:*
Supply Jetson with a 5V, 3A power supply. Based on my experience, using a 5V 1.5A may cause the jetson to crash in the building process, which led to me having to reflash the OS and start the process again.

*Step 1:*
Expand Swap memory. Jetson comes with only 4GB of RAM, and therefore can crash during the build process. Swap memory can be used as suppliment for RAM when needed.
```bash
sudo apt-get install zram-config
sudo gedit /usr/bin/init-zram-swapping
```
Replace this line
```bash
mem=$(((totalmem / 2 / ${NRDEVICES}) * 1024))
```
With this line
```bash
mem=$(((totalmem / ${NRDEVICES}) * 1024))
```
Reboot to apply change

*Step 2:*
```bash
$ git clone https://github.com/JetsonHacksNano/buildOpenCV
$ cd buildOpenCV
$ ./buildOpenCV.sh |& tee openCV_build.log
```
Reference: https://www.jetsonhacks.com/2019/11/22/opencv-4-cuda-on-jetson-nano/



