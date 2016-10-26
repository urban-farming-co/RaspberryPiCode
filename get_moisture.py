#!/usr/bin/python
# pins:VCC got s to pin 1
# GND to pin 9
# and DO to pin 11 (GPIO 17)

import Adafruit_ADS1x15
import RPi.GPIO as GPIO
import time

adc = Adafruit_ADS1x15.ADS1015()

def save(s):
    # s is a string
    # save file is called moisture.txt
    f = open("moisture.txt", "w")
    f.write(s)
    f.close()

def callback(channel):  
	if GPIO.input(channel):
		print "LED off, the plant is thirsty"
		
	else:
		print "LED on, the plant is fine and also dandy."

        save(str(GPIO.input(channel)))
		
# Set our GPIO numbering to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin that we have our digital output from our sensor connected to
channel = 17
# Set the GPIO pin to an input
GPIO.setup(channel, GPIO.IN)

# This line tells our script to keep an eye on our gpio pin and let us know when the pin goes HIGH or LOW
#GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
# This line asigns a function to the GPIO pin so that when the above line tells us there is a change on the pin, run this function
#GPIO.add_event_callback(channel, callback)
GAIN = 1

def capt():
#    1C1A
#   save(str(GPIO.input(channel)))
#  return GPIO.input(channel)

   adc = Adafruit_ADS1x15.ADS1015()
   v = adc.read_adc(0, gain=GAIN )
   print(str(v))
   v = v -1652
   print(str(v))
   v = v* 5  
   print(str(v))
   v = v / 2  
   print(str(v))

   v = v if v<=100 else 100 
   v = v if v>=0 else 0 

   print(str(v))
   save(str(v))
   print(str(v))
   return v

capt()
