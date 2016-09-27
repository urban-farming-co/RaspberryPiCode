from picamera import PiCamera
from time import sleep
import sched
import time


camera = PiCamera()
camera.resolution=(100,100)
def prev10():
    camera.start_preview()
    sleep(10)
    camera.stop_preview()

def capt():
    camera.start_preview()
    sleep(5)
    camera.capture('image.jpg')
    camera.stop_preview()



