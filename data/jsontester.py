import json
timerFile = '/home/vineeth/AquariumMonitor/data/timers.json'

def getStartAndStopTime(device):
    jsonFile = open(timerFile,'r')
    timings = json.load(jsonFile)
    jsonFile.close()
    for item in timings['data']:
        if item['Device'] == device:
            startTime = item['start']
            stopTime = item['stop']
    return [startTime, stopTime]


def updateTimers(device, startTime, stopTime):
    jsonFile = open(timerFile,'r')
    timings = json.load(jsonFile)
    jsonFile.close()
    for item in timings['data']:
        if item['Device'] == device:
            item['start'] = startTime
            item['stop']= stopTime
    jsonFile = open(timerFile,'w')
    json.dump(timings, jsonFile)
    jsonFile.close()

jsonFile = open(timerFile,'r')
timings = json.load(jsonFile)
jsonFile.close()

for item in timings['data']:
    print(item)

print(getStartAndStopTime("co2"))
