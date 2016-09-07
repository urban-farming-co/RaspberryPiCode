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
delayUntilNextPost = 10  # seconds
priority = 1


def postToServer():
    s.enter(delayUntilNextPost, priority, postToServer, ())
    camera.capt()
    url = 'http://holdingweb.eu-gb.mybluemix.net/urbanfarming/data/'
    info = get_ht() 
    soil = capt() * 100
    img = open('/home/pi/piCode/image.jpg', 'rb')
    multipart_data = MultipartEncoder(
        fields={'image': ('img.jpg', img, 'image/*'),
                'soilMoisture': str(soil),
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
