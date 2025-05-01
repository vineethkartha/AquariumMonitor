import time
import PinIOModule
import JSONUtilities as js
import datetime

sunsunLight= PinIOModule.PinIOModule(6)
rgbLight = PinIOModule.PinIOModule(5)

try:
    while True:
        curTime = datetime.datetime.now().time()
        [startTime_str,stopTime_str] = js.getStartAndStopTime('rgb')
        manualOverride = js.getManualOverride('rgb')
        startTime = datetime.datetime.strptime(startTime_str,"%H:%M").time()
        stopTime = datetime.datetime.strptime(stopTime_str,"%H:%M").time()

        print(startTime_str)
        if(curTime >= startTime and curTime <= stopTime):
            rgbLight.TurnOn()
        elif manualOverride == False:
            rgbLight.TurnOff()
        [startTime_str,stopTime_str] = js.getStartAndStopTime('white')
        manualOverride = js.getManualOverride('white')
        startTime = datetime.datetime.strptime(startTime_str,"%H:%M").time()
        stopTime = datetime.datetime.strptime(stopTime_str,"%H:%M").time()
    
        print(startTime_str)
        if(curTime >= startTime and curTime <= stopTime):
            sunsunLight.TurnOn()
        elif manualOverride == False:
            sunsunLight.TurnOff()
    
        time.sleep(60)        
except:
    sunsunLight.TurnOff()
    rgbLight.TurnOff()
