import os
import glob
from datetime import datetime

class DS18b20:
    def __init__(self):
        os.system('sudo modprobe w1-gpio')
        os.system('sudo modprobe w1-therm')
        self.deviceFile = glob.glob('/sys/bus/w1/devices/' + '28*')[0]+ '/temperature'
 
    def readTemperature(self):
        sensorFile = open(self.deviceFile, 'r')
        lines = sensorFile.readlines()
        while not lines:
            lines = sensorFile.readlines()
        temperatureString = lines[0]
        temperatureInCelsius = float(temperatureString) / 1000.0
        return temperatureInCelsius
