import time
import PinIOModule
import JSONUtilities as js
import datetime

valve = PinIOModule.PinIOSModule(26)
try:
    while True:
        [startTime_str,stopTime_str] = js.getStartAndStopTime('co2')
        #print(startTime_str)
        curTime = datetime.datetime.now().time()
        startTime = datetime.datetime.strptime(startTime_str,"%H:%M").time()
        stopTime = datetime.datetime.strptime(stopTime_str,"%H:%M").time()
        if(curTime >= startTime and curTime <= stopTime):
            valve.TurnOn()
        else:
            valve.TurnOff()
        time.sleep(60)
except:
    valve.TurnOff()

