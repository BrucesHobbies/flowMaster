#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M")

# raspistill -o $DATE.jpg # only works with RPi camera

# For usb webcams use fswebcam:
# sudo apt-get install fswebcam
# sudo usermod -a -G video pi
# Some commonly used command line options
# -r 352x288
# -r 1280x1024
# --no-banner

# crontab -e
# */5 * * * * /home/pi/PythonProjects/flowMaster/camera.sh 2>&1

fswebcam -S 10 /home/pi/PythonProjects/flowMaster/water_meter/$DATE.jpg
