import sqlite3

dbName = '/home/pi/AquariumMonitor/data/temperatureLog.db'

def getData(mDate):
    connection = sqlite3.connect(dbName)
    cursor= connection.cursor()

    queryResult= cursor.execute("select Time, Temperature from AquariumTemperature where Date= :date",{"date":mDate})
    data = queryResult.fetchall()
    curTemp = data[len(data)-1][1]
    minQuery = cursor.execute("select Time,min(Temperature) from AquariumTemperature where Date= :date",{"date":mDate})
    minData= minQuery.fetchall()
    minTemperature = minData[len(minData)-1][1]
    minTempTime = minData[len(minData)-1][0]

    maxQuery = cursor.execute("select Time,max(Temperature) from AquariumTemperature where Date= :date",{"date":mDate})
    maxData= maxQuery.fetchall()
    maxTemperature = maxData[len(maxData)-1][1]
    maxTempTime = maxData[len(maxData)-1][0]

    labels=[]
    temp=[]
    for row in data:
        labels.append(row[0])
        temp.append(row[1])
    datasetStyling = """pointRadius: 1,
			fill: false,
			borderColor: 'red',
			borderWidth: 1,
			lineTension: 0.8,"""
    options = """options: {
		title: {display: true, 
				text: 'Temperature changes during the day',},
		legend: {display: false,},
		scales: {yAxes: [{ticks: {suggestedMin: 23, suggestedMax: 26,},},],},
		},"""
    url = "https://quickchart.io/chart?c={type:\'line\' , data:{labels:%s,datasets:[{label:\'Temperature\', data:%s, %s}]},%s}" %(labels, temp, datasetStyling, options)
    return [curTemp, minTemperature, minTempTime, maxTemperature, maxTempTime, url]
