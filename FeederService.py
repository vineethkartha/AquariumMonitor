import time
import ServoModule
import JSONUtilities as js
import datetime
import json

feedingTimeFile = '/home/pi/AquariumMonitor/data/feedTime.json'
def getStartTime(device):
    jsonFile = open(feedingTimeFile,'r')
    timings = json.load(jsonFile)
    jsonFile.close()
    for item in timings['data']:
        if item['Device'] == device:
            startTime = item['start']
            fedTime = item['fed']
    return [startTime, fedTime]

def updateFedStatus(device,fed):
    jsonFile = open(feedingTimeFile,'r')
    timings = json.load(jsonFile)
    jsonFile.close()
    for item in timings['data']:
        if item['Device'] == device:
            item['fed']= fed
    jsonFile = open(feedingTimeFile,'w')
    json.dump(timings, jsonFile, indent=6)
    jsonFile.close()



servo = ServoModule.Servo(18)
servo.start(0)
time.sleep(1)
time.sleep(1)
servo.moveToAngle(600)
time.sleep(1)
servo.moveToAngle(1500)
time.sleep(1)
#servo.moveToAngle(2300)
time.sleep(1)
servo.stop()
try:
    while True:
        curTime = datetime.datetime.now().time()
        [startTime_str,fed] = getStartTime('feeder1') 
        #startTime_str = "10:57"
        startTime = datetime.datetime.strptime(startTime_str,"%H:%M").time()
        if(curTime < startTime and fed):
            print("updating feed status")
            updateFedStatus('feeder1',False)
        print(startTime_str)
        print(curTime)
        if(curTime >= startTime and fed==False):        
            servo.start(0)
            time.sleep(1)
            servo.moveToAngle(1500)
            time.sleep(2)
            servo.moveToAngle(2300)
            time.sleep(2)
            servo.moveToAngle(1500)
            time.sleep(1)
            servo.stop()
            updateFedStatus('feeder1',True)
        time.sleep(60)
except:
    servo.stop()

