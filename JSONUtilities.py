import json
import datetime

timerFile = '/home/pi/AquariumMonitor/data/timers.json'

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
    json.dump(timings, jsonFile, indent=6)
    jsonFile.close()

def getManualOverride(device):
    jsonFile = open(timerFile,'r')
    timings = json.load(jsonFile)
    jsonFile.close()
    for item in timings['data']:
        if item['Device'] == device:
            manual = item['manual']
    return manual

def updateManualOverride(device, override):
    jsonFile = open(timerFile,'r')
    timings = json.load(jsonFile)
    jsonFile.close()
    for item in timings['data']:
        if item['Device'] == device:
            item['manual'] = override
    jsonFile = open(timerFile,'w')
    json.dump(timings, jsonFile, indent=6)
    jsonFile.close()


def getGanttChartURL():
    [co2start,co2stop] = getStartAndStopTime('co2')
    [rgbstart,rgbstop] = getStartAndStopTime('rgb')
    [whitestart,whitestop] = getStartAndStopTime('white')
    curTime = datetime.datetime.now()
    curTimeStr = curTime.strftime("%D  %H:%M")
    curDate = curTime.strftime("%D")

    gantCharOptions ="""options: {
    title: {display: true, 
    text: 'Timer Settings'},    
    legend: {
      display: false
    },
    annotation: {
      annotations: [{
        type: \'line\',
        mode: \'vertical\',
        scaleID: \'x-axis-0\',
        value: \'%s\',
        borderColor: \'red\',
        borderWidth: 1,
        label: {
          enabled: true,
          content: \'Current Time\',
          position: \'top\'
        }
      }]
    },
    scales: {
      xAxes: [{
        position: \'bottom\',
        type:\'time\',
        time: {
          unit: \'hour\'
        },
        ticks: {
          min: new Date(\'%s 08:00\'),
          max: new Date(\'%s 19:00\'),
        }
      }],
    },
    },"""%(curTimeStr, curDate, curDate)
    gantChartURL = """https://quickchart.io/chart?width=500&height=200&c= {
    type: \'horizontalBar\',
    data: {
    labels: [\'CO2\', \'RGB light\', \'White light\'],
    datasets: [{
    data: [
    [new Date(\'%s\'), new Date(\'%s\')],
    [new Date(\'%s\'), new Date(\'%s\')],
    [new Date(\'%s\'), new Date(\'%s\')],
    ],
    backgroundColor: [\'rgb(255, 99, 132)\',\'rgb(99, 255, 132)\',\'rgb(132, 99, 255)\' ],
    categoryPercentage: 0.5,
    barPercentage: 1,
    }, ],
  },%s
}"""%(curDate+" "+ co2start,curDate+" "+ co2stop, curDate+" "+ rgbstart, curDate+" "+ rgbstop, curDate+" "+ whitestart, curDate+" "+ whitestop, gantCharOptions)
    print(gantChartURL)
    return gantChartURL
