import requests
import requests_toolbelt
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os
import time

global path
path = '/home/pi/piCode/image.jpg'
global lastImageUpdate # the last time that the image was modified
lastImageUpdate = 0
print(lastImageUpdate)


def updateLastImageVariable(v):
    # I may want to update the global variable lastImageUpdate
    global lastImageUpdate
    lastImageUpdate = v
    return

def getStuff():
    # Get the current colour
    c = open("color.txt", "r")
    color = c.readline()
    c.close()
    # get the current moisture level
    s = open("moisture.txt", "r")
    soil = s.readline()
    s.close()
    print(soil)
    # get the current lux level
    l = open("lux.txt", "r")
    lux = l.readline()
    l.close()
    # get the current humidity level
    h = open("humidity.txt", "r")
    r = h.readline()
    h.close()
    print(r)
    # Get the current temperature level
    h = open("temperature.txt", "r")
    t = h.readline()
    h.close()
    print(t)
    # Create a dictionary to store the variables in.
    info = {}
    # If the humidity level is none, ie. the sensor broke, return 0
    info["relhumidity"] = float(r) if r != None else 0 
    # If the humidity level is none, ie. the sensor broke, return 0
    info["temperature"] = float(t) if t != None else 0
    info["color"] = color
    info["soil"] = soil
    info["lightLuxLevel"] = lux
    # decide if we need to send the image. is it too dark?
    # has a new image been taken?
    lastmod =  os.path.getmtime(path)
    print(str(lastmod ) + "    " + str(lastImageUpdate))
    if lastmod>lastImageUpdate and int(lux)>15:
        print("Sending IMAGE")
        info["img"] = open(path, 'rb')
        updateLastImageVariable( lastmod)
    else:
        info["img"] = None
    # print out the values.
    for k in info.keys():
	print (info[k])
    return info

getStuff()

def postToServer():
    url = 'http://holdingweb.eu-gb.mybluemix.net/urbanfarming/data/'
    info = getStuff()
    for k in info.keys():
        print(type(info[k]))
    multipart_data = MultipartEncoder(
        fields={'image': ('img.jpg',info["img"], 'image/*'),
                'soilMoisture': str(info["soil"]),
                'relHumidity': str(info["relhumidity"]), 
                'plantName': "Minty MacMintface",
                'lightLuxLevel': str(info["lightLuxLevel"]),
                'temperature': str( info["temperature"]),
                'colour'     : str(info["color"]),
                'uniqueId'   : '1'  
                }
    )
    r = requests.post(url,
                      data=multipart_data,
                      headers={
                          'Content-Type': multipart_data.content_type
                          }
                      )

    print(r.text)

