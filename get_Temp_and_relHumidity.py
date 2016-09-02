# see /home/pi/Adafruit_python_DHT/ for more information

#red wire to pin1
# black wire to pin 6
# yellow wire to pin 7, GPIO 4
import sys
import Adafruit_DHT

sensor = Adafruit_DHT.AM2302
pin = 4

def get_ht():
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        info = {"temperature" : temperature, "relhumidity":humidity}
	return  info

print(get_ht())

