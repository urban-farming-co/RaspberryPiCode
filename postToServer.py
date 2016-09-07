import requests
import requests_toolbelt
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os
import sched
import time
import camera
from get_Temp_and_relHumidity import get_ht
from get_moisture import capt
s = sched.scheduler(time.time, time.sleep)
delayUntilNextPost = 60  # 4*60*60   seconds
priority = 1

def getStuff():
    camera.capt()
    info = get_ht() 
    r = info["relhumidity"]
    t = info["temperature"]
    soil = capt() * 100
    info["relhumidity"] = int(r) if r != None else 0 
    info["temperature"] = int(t) if t != None else 0
    info["soil"] = soil
    info["img"] = open('/home/pi/piCode/image.jpg', 'rb')
    return info

def postToServer():
    s.enter(delayUntilNextPost, priority, postToServer, ())
    url = 'http://holdingweb.eu-gb.mybluemix.net/urbanfarming/data/'
    info = getStuff()
    for k in info.keys():
        print(type(info[k]))
    multipart_data = MultipartEncoder(
        fields={'image': ('img.jpg',info["img"], 'image/*'),
                'soilMoisture': str(info["soil"]),
                'relHumidity': str(info["relhumidity"]), 
                'plantName': "Basil",
                'lightLuxLevel': '1',
                'temperature': str( info["temperature"])
                }
    )
    r = requests.post(url,
                      data=multipart_data,
                      headers={'Content-Type': multipart_data.content_type})

    print(r.text)
s.enter(delayUntilNextPost, priority, postToServer, ())

s.run()
