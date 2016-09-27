import requests
import requests_toolbelt
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os
import time

global path
path = '/home/pi/piCode/image.jpg'
global lastImageUpdate # the last time that the image was modified
lastImageUpdate =  os.path.getmtime(path)
print(lastImageUpdate)

def getStuff():
    global lastImageUpdate
    c = open("color.txt", "r")
    color = c.readline()
    c.close()
    s = open("moisture.txt", "r")
    soil = s.readline()
    s.close()
    print(soil)
    l = open("lux.txt", "r")
    lux = l.readline()
    l.close()
    h = open("humidity.txt", "r")
    r = h.readline()
    h.close()
    print(r)
    info = {}
    info["relhumidity"] = float(r) if r != None else 0 
    h = open("temperature.txt", "r")
    t = h.readline()
    h.close()
    print(t)
    info["temperature"] = float(t) if t != None else 0
    info["color"] = color
    info["soil"] = soil
    info["lightLuxLevel"] = lux
    lastmod =  os.path.getmtime(path)
    print(str(lastmod ) + "    " + str(lastImageUpdate))
    if lastmod>lastImageUpdate:
        info["img"] = open(path, 'rb')
        lastImageUpdate = lastmod
    else:
        info["img"] = None
    info["light"] = "1"
    for k in info.keys():
	print (info[k])
    return info

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
                      headers={'Content-Type': multipart_data.content_type})

    print(r.text)

