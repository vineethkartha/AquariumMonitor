import DS18b20_Module
from datetime import datetime
import time
import sqlite3
import DBUtilities as dbutils
temperatureSensor = DS18b20_Module.DS18b20()

connection = sqlite3.connect(dbutils.dbName)
cursor= connection.cursor()

def createTable():
    cursor.execute("create table if not exists AquariumTemperature(id INTEGER PRIMARY KEY AUTOINCREMENT, Date DATE, Time TIME, Temperature Numeric)")

def enterRecord():
    dateEntry,timeEntry, temperatureEntry = getTemperatureRecord()
    cursor.execute("insert into AquariumTemperature (Date, Time, Temperature) values (?,?,?)",(dateEntry, timeEntry,  temperatureEntry))
    connection.commit()
    
def getTemperatureRecord():
    temperature = temperatureSensor.readTemperature()
    time = datetime.now().strftime("%H:%M")
    date = datetime.now().strftime("%D")
    print(date,time,temperature)
    return [date,time, temperature]

createTable()
while True:
    enterRecord()
    #print(getTemperatureRecord())
    time.sleep(600)
