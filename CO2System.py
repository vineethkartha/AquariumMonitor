import time
import gpio_client
import JSONUtilities as js
import datetime

gpio_client.register("co2", 26)

try:
    while True:
        [startTime_str,stopTime_str] = js.getStartAndStopTime('co2')
        #print(startTime_str)
        curTime = datetime.datetime.now().time()
        startTime = datetime.datetime.strptime(startTime_str,"%H:%M").time()
        stopTime = datetime.datetime.strptime(stopTime_str,"%H:%M").time()
        if(curTime >= startTime and curTime <= stopTime):
            gpio_client.set_gpio("co2", True)
        else:
            gpio_client.set_gpio("co2", False)
        time.sleep(60)
except:
    gpio_client.set_gpio("co2", False)


