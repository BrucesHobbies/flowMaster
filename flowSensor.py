#!/usr/bin/env python

"""
Copyright(C) 2021, BrucesHobbies
All Rights Reserved

AUTHOR: BrucesHobbies
DATE: 04/17/2021
REVISION HISTORY
  DATE        AUTHOR          CHANGES
  yyyy/mm/dd  --------------- -------------------------------------

GENERAL INFO
    Captures pulses from water flow Hall Effect sensor (pulses using GPIO).
    Computes:
        - total quantity in Liters
        - flow rate in Liters/minute, averaged using a simple low pass filter

LICENSE:
    This program code and documentation are for personal private use only. 
    No commercial use of this code is allowed without prior written consent.

    This program is free for you to inspect, study, and modify for your 
    personal private use. 

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.


Tested with:
Digiten Water Flow Sensor Model: FL-S402B
Working range: 0.3 - 10L/min
Water pressure <0.8Mps
F = 23 * Q (L/minute)

SIGNAL goes to a voltage divider of 2/3 (5kOhm and 10kOhm) to convert 5 V output to 3.3 V
RPi inputs cannot be exposed to voltages less than 0 or greater than 3.3 volts.

RPI			          Flow sensor
----------------          -------
Pin  2 (5Vdc)             Vcc (Red)
Pin  6 (GND)	          GND (Black)
Pin 16 (GPIO23)           SIGNAL (0 - 3.3 Vdc) from voltage divider from yellow wire

"""

import sys
import time
import datetime
import RPi.GPIO as GPIO

import pubScribe

# FLOWSIGNAL = 18    # BCM GPIO18 RPi3/4 pin 12
# FLOWSIGNAL = 23    # BCM GPIO23 RPi3/4 pin 16
FLOWSIGNAL = 24    # BCM GPIO24 RPi3/4 pin 18


tInterval = 1    # Display / logging interval in seconds


#
# Initialize GPIO
#
def sensorInit() :
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FLOWSIGNAL,GPIO.IN)
    GPIO.add_event_detect(FLOWSIGNAL, GPIO.RISING, callback=flowCallback)  


#
# Threaded callback for flow sensor
#
pulses = 0
avgFlowRate = 0
lastPulseTime = 0
lastPulses = 0

def flowCallback(channel) :
    global pulses, avgFlowRate, lastPulseTime

    lpf = 0.8    # Low pass filter values closer to 1.0 provide more filtering,
                 # values closer to zero provide less filtering.

    pulses += 1

    pulseTime = time.time()

    if lastPulseTime :
        avgFlowRate = (avgFlowRate * lpf) + ((pulseTime - lastPulseTime) * (1.0 - lpf))

    lastPulseTime = pulseTime


#
# Close RPi GPIO
#
def sensorClose() :
    GPIO.remove_event_detect(FLOWSIGNAL)
    GPIO.cleanup()


def flowRate() :
    global lastPulses

    result = 0

    if pulses > lastPulses and avgFlowRate > .0001 :
            result = round(1.0/avgFlowRate/23.0, 3)    # L/minute

    lastPulses = pulses

    return result


def litres() :
    return round(pulses / (23.0 * 60.0), 3)


#
# Test / debug
#
if __name__ == '__main__':
    last_q = 0
    last_f = 0

    print('\nProgram started ', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S '))
    print('Press CTRL+C to exit...\n')
    pubScribe.connectPubScribe()
    sensorInit()

    try :
        while (True) :
            """
            # For debug of GPIO input pin
            if GPIO.input(FLOWSIGNAL) :
                print('Input HIGH')
            else :
                print('Input LOW')
            """

            q = litres()
            f = flowRate()

            if q != last_q or f != last_f :
                print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S '), 'Liters= ', q, ' AvgFlowRate (L/minute)= ', f)
                topic = 'flowSensor'
                dictVar = {'Qty (L)': q, 'FlowRate (L/minute)': f}
                pubScribe.pubRecord(pubScribe.CSV_FILE, topic, dictVar)
                last_q = q
                last_f = f

            time.sleep(tInterval)

    except KeyboardInterrupt :
        print(' Keyboard interrupt caught, exiting.')

    sensorClose()
    pubScribe.disconnectPubScribe()
