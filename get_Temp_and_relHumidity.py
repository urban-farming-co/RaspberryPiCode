# see /home/pi/Adafruit_python_DHT/ for more information

#red wire to pin1
# black wire to pin 6
# yellow wire to pin 7, GPIO 4
import sys
import Adafruit_DHT
import time
import sched


sensor = Adafruit_DHT.AM2302
pin = 4

def save(t, h):
	print(str(t) +"  "+ str(h))
	f = open("temperature.txt", "w")
        f.write(str(t))
        f.close()
	f = open("humidity.txt", "w")
        f.write(str(h))
        f.close()

def get_ht():
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        save(temperature, humidity)
