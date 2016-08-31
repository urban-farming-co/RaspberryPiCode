import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os
import sched
import time
import camera


s = sched.scheduler(time.time, time.sleep)
delayUntilNextPost = 10  # seconds
priority = 1


def postToServer():
    s.enter(delayUntilNextPost, priority, postToServer, ())
    camera.capt()
    url = 'http://karenmcculloch.me/urbanfarming/data'
    img = open(os.environ['HOME']+'/piCode/image.jpg', 'rb')
    multipart_data = MultipartEncoder(
        fields={'image': ('img.jpg', img, 'image/*'),
                'soilMoisture': '1',
                'relHumidity': '1',
                'temp': '1'}
    )
    r = requests.post(url,
                      data=multipart_data,
                      headers={'Content-Type': multipart_data.content_type})

    print(r.text)
s.enter(delayUntilNextPost, priority, postToServer, ())

s.run()
