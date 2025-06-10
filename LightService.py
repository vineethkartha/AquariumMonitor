import time
import gpio_client
import datetime
import JSONUtilities as js

gpio_client.register("white", 6)
gpio_client.register("rgb", 5)

try:
    while True:
        curTime = datetime.datetime.now().time()
        [startTime_str,stopTime_str] = js.getStartAndStopTime('rgb')
        manualOverride = js.getManualOverride('rgb')
        startTime = datetime.datetime.strptime(startTime_str,"%H:%M").time()
        stopTime = datetime.datetime.strptime(stopTime_str,"%H:%M").time()

        print(startTime_str)
        if(curTime >= startTime and curTime <= stopTime):
            gpio_client.set_gpio("rgb", True)
        elif manualOverride == False:
            gpio_client.set_gpio("rgb", False)

        [startTime_str,stopTime_str] = js.getStartAndStopTime('white')
        manualOverride = js.getManualOverride('white')
        startTime = datetime.datetime.strptime(startTime_str,"%H:%M").time()
        stopTime = datetime.datetime.strptime(stopTime_str,"%H:%M").time()
    
        print(startTime_str)
        if(curTime >= startTime and curTime <= stopTime):
            gpio_client.set_gpio("white", True)
        elif manualOverride == False:
            gpio_client.set_gpio("white", False)
    
        time.sleep(60)        
except:
    gpio_client.set_gpio("white", False)
    gpio_client.set_gpio("rgb", False)

