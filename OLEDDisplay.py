import time
import socket
import DBUtilities as dbutils
import JSONUtilities as js
from board import SCL, SDA
import busio
import datetime
# Import the SSD1306 module.
import adafruit_ssd1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    IPAddr = s.getsockname()[0]
    s.close()
    return IPAddr

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)
width = 128
height = 32
padding = -2
top = padding
bottom = height-padding

display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

#clear display
display.fill(0)
display.show()

image  = Image.new ("1",(width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()
IPAddr = getIP()
try:
    counter = 0
    while True:
        # recheck IP after every 10 mins
        if counter == 10:
            IPAddr = getIP()
            counter = 0
        counter = counter+1
        curTime = datetime.datetime.now()
        curTimeStr = curTime.strftime("%D  %H:%M")
        curDate = curTime.strftime("%D")
        try:
            curTemp,minTemp, minTempTime, maxTemp, maxTempTime,url =dbutils.getData(curDate)
            draw.rectangle((0,0, width, height), outline = 0, fill = 0)
            draw.text((0, top), "IP: "+IPAddr+":5000" ,  font=font, fill=255)
            draw.text((0, top +8), curTimeStr ,  font=font, fill=255)
            draw.text((0, top +16), "Temperature: "+str("{0:0.1f}".format(curTemp)) ,  font=font, fill=255)
            draw.text((0, top +24), "Max: "+str("{0:0.1f}".format(maxTemp))+" | Min: "+str("{0:0.1f}".format(minTemp)),  font=font, fill=255)
            # Display image.
            display.image(image)
            display.show()
            time.sleep(30)
            display.fill(0)
            display.show()
            [startTime_str,stopTime_str] = js.getStartAndStopTime('co2')
            draw.rectangle((0,0, width, height), outline = 0, fill = 0)
            draw.text((0, top), "IP: "+IPAddr+":5000" ,  font=font, fill=255)
            draw.text((0, top +8), curTimeStr ,  font=font, fill=255)
            draw.text((0, top +16), "CO2: "+startTime_str+" - "+stopTime_str ,  font=font, fill=255)

        except:
            draw.rectangle((0,0, width, height), outline = 0, fill = 0)
            draw.text((0, top), "IP: "+IPAddr+":5000" ,  font=font, fill=255)
            draw.text((0, top +8), curTimeStr ,  font=font, fill=255)
            draw.text((0, top +16), "unable to  " ,  font=font, fill=255)
            draw.text((0, top +24), "fetch data  " ,  font=font, fill=255)
            # Display image.
            display.image(image)
            display.show()
        time.sleep(60)                    
except:        
     draw.rectangle((0,0, width, height), outline = 0, fill = 0)
     draw.text((0, top), "Disconnected " ,  font=font, fill=255)    
     # Display image.
     display.image(image)
     display.show()
