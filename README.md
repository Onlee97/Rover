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
Using NVIDIA L4T32.3.1, JetPack 4.3\
Reference: https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit

**Install OpenCV**\
The JetPack (Jetson OS) comes with a built in OpenCV (installed in /usr/ folder). However, this OpenCV doesn't come with CUDA support. In order to have a more customized OpenCV, we should built it from source. The building process can take about 2.5 hours

*Step 0:*
Supply Jetson with a 5V, 3A power supply. Based on my experience, using a 5V 1.5A may cause the jetson to crash in the building process, which led to me having to reflash the OS and start the process again.

*Step 1:*
Expand Swap memory. Jetson comes with only 4GB of RAM, and therefore can crash during the build process. Swap memory can be used as suppliment for RAM when needed.
```bash
$ sudo apt-get install zram-config
$ sudo gedit /usr/bin/init-zram-swapping
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

**Install Intel Realsense SDK**\
The SDK are neccessary for the jetson to interact with the Depth Camera. The Depth Camera provide a 3D point cloud data which is very beneficial in multiple application. There are convienient way to install the SDK. However, if we want the library to support **Python**, then we have to build from source.

```bash
$ git clone https://github.com/IntelRealSense/librealsense.git
$ mkdir build
$ cd build
$ cmake ../ -DBUILD_PYTHON_BINDINGS:bool=true -DCMAKE_BUILD_TYPE=Release
$ sudo make uninstall && make clean && make -j4 && sudo make install
```
The library will be installed to */usr/local*, Therefore to use the pyrealsense2 library, run the following line to add to .bashrc file
```bash
$ export PYTHONPATH=$PYTHONPATH:/usr/local/lib
```
Reference: 
https://github.com/IntelRealSense/librealsense/blob/master/doc/installation.md
https://github.com/IntelRealSense/librealsense/tree/master/wrappers/python

**Install Aduino IDE**
```bash
$ git clone https://github.com/JetsonHacksNano/installArduinoIDE
$ cd installArduinoIDE
$ ./installArduinoIDE.sh
```



