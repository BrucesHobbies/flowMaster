# flowMaster
Hall Effect Water Flow Sensor for Raspberry Pi
Copyright(C) 2021, BrucesHobbies,
All Rights Reserved

Flow meter monitoring for homes and buildings - This is a DIY open source project for the Raspberry Pi or similar system using an inexpensive hell effect flow meter sensor. The software is written in Python and runs under Linux.

# Preface
Flow meters are useful to monitor and track well water, water softener operation, water filter operation, and irrigation watering systems usage, answering basic questions such as:

- How many gallons / liters have been used?
- What is the flow rate?
- Usage based instead of time based change for water filters?
- Normal reverse osmosis filter cycling?
- Normal operation of reverse osmosis automatic shut off valve (low water pressure or failed components)?
- Normal operation of water softener?
- Normal operation of irrigation system (line burst or blockage)?

# FlowMaster™ Project Overview
The Raspberry Pi is an ideal platform to monitor water flow using Hall Effect sensors. This project uses a small inexpensive flow meter (~$10 USD) with a Raspberry Pi to monitor flow rate and quantity of water consumed.

flowMaster™ logs usage and flow rate to a Comma Separated Variable (CSV) file that can be plotted using MatPlobLib or in a spreadsheet. 
- Time (UNIX seconds and date/time stamp)
- Quantity consumed (Gallons / Liters)
- Flow rate (Gallons per minute / Liters per minute)

# Required Hardware 
As an Amazon Associate I earn a small commission from qualifying purchases. I appreciate your support, if you purchase using the links below.

## Flow meter
- [Hall Effect Flow Meter](https://amzn.to/3dCtZLm)
- 5k ohm and 10k ohm resistors to convert 5 volt output signal to 3.3 volt input to RPi

## Raspberry Pi system (if you don’t already own one)
- Raspberry Pi (any of the following)
  - [RPI-Zero]( https://amzn.to/3ly0mM0)
  - [RPI 3B+]( https://amzn.to/3lyPBJe)
  - [RPI 4B]( https://amzn.to/2Vwulto)
- Power adapter for your Raspberry Pi
- Heatsinks (optional)
- SD-Card

For installing the Raspberry Pi operating system, you may want a USB keyboard and USB mouse along with an HDMI cable and monitor. If using the RPI4, a Micro-HDMI to HDMI adapter may be needed. Once installed and configured you may want to switch to SSH or remote desktop so that you can remove the monitor, mouse, and keyboard.

## Flow Sensor Wiring

RPI|Flow Sensor
----------------:|-------|
Pin  4 (5Vdc)|Red Vcc|
Pin  6 (GND)|Blk GND|
Pin 16 (GPIO23)|Resistor tap|

RPi inputs cannot be exposed to voltages less than 0 nor greater than 3.3 volts. The signal out of the sensor is 5 volts. One approach of converting it to 3.3 volts is to feed the output to a resistive voltage divider. This can be made from 5K ohm and 10K ohm resistors in series with the 5K ohm to the Yellow SIGNAL and the 10K ohm to ground. The RPi pin 16 (GPIO23) goes to the resistors center tap as shown below.

      SIGNAL >--+
                |      
              5K ohm
                |
                +---> RPi GPIO23 pin 16 
                |
             10K ohm
                |
        GND ----+---- RPi GND pin 6


# Software Installation
## Step 1: Install the Raspberry Pi Operating System.
Here are the instructions to install the Raspberry Pi Operating System.
[Raspberry Software Install Procedure](https://www.raspberrypi.org/software/operating-systems/)

Before continuing make sure your operating system has been updated with the latest updates.

    sudo apt-get update
    sudo apt-get upgrade
    sudo reboot now

## Step 2: Download flowMaster software source code
To get a copy of the source files type in the following git command assuming you have already installed git:

    git clone https://github.com/BrucesHobbies/flowMaster

# Run The Program From A Terminal Window 
From LXTerminal type:

    python3 flowMaster.py

# Validation
To verify that flowMaster was working correctly, I used the city water meter to my house. Since the water filter runs at unpredictable times, I set up a USB webcam above my city water meter to take a time lapse series of photos of the water meter using the script camera.sh which was called from crontab every 5 minutes. The water meter was in close agreement with the flow meter. This was multiple comparisons but not at wide range of flow rates, nor did I sample a statistically large number of units. I was pleased with the results that the flow meter more than met my expectations.

# Plotting the Log File
flowMaster.csv is the log file for the water quantity consumed and flow rate. Comma Separated Variable (CSV) files that can be plotted in a spreadsheet. 

# Auto Start at Boot
Type the following command:

    sudo crontab –e
    
Select the type of editor you are familiar with. I used nano. Add the following line at the end of the file and then press ctrl+O to write the file and ctrl+X to exit the nano editor.

    @reboot sleep 60 && cd flowMaster && python3 flowMaster.py

# Feedback
Let us know what you think of this project and any suggestions for improvements. Feel free to contribute to this open source project.
