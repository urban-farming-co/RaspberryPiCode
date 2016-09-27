import get_Temp_and_relHumidity as th
import get_moisture as m
import camera as c
import postToServer as p
import colorSensor as l
import sched
import time


s = sched.scheduler(time.time, time.sleep)




# get temp, humidity and camera will save every x minutes
global delay1
delay1 = 40
global delay2 
delay2 = 55
global delay3 
delay3 = 60
global delay4 
delay4 = 0
print (delay4)
priority = 1

def takePicture():
    global delay4
    print(delay4)
    if (delay4 == 0):
	    print("scheduling c")
	    s.enter(delay1 +5, priority, c.capt, ())
            delay4 = 21600 
    else:
            delay4-=60

def schedul():
    print("scheduling l")
    s.enter(delay1,    priority, l.capt, ())

    print("scheduling m")
    s.enter(delay1 +2, priority, m.capt, ())

    print("scheduling h")
    s.enter(delay1 + 4, priority, th.get_ht, ())

    print("checking camera timer")
    takePicture()

    print("scheduling p")
    s.enter(delay2, priority, p.postToServer, ())
    print("scheduling self")
    s.enter(delay3, priority, schedul, ())
    return


print("running")
schedul()
s.run()
