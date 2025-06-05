import sqlite3

dbName = '/home/vineeth/AquariumMonitor/data/temperatureLog.db'

def getMaxMinAndCurrentTempData(mDate):
    connection = sqlite3.connect(dbName)
    cursor= connection.cursor()
    queryResult= cursor.execute("select Time, Temperature from AquariumTemperature ORDER BY id DESC LIMIT 1")
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
    
    return [curTemp, minTemperature, minTempTime, maxTemperature, maxTempTime]

def getDataForChart(start_date, end_date):
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Date, Time, Temperature FROM AquariumTemperature
        WHERE Date BETWEEN ? AND ?
        ORDER BY Date ASC, Time ASC
    """, (start_date.strftime('%D'), end_date.strftime('%D')))
    rows = cursor.fetchall()
    conn.close()

    print(start_date.strftime('%D'))
    chart_data = [
        {
            'timestamp': f"{date} {time}",
            'temperature': round(temp, 1)
        } for date, time, temp in rows
    ]

    return chart_data

