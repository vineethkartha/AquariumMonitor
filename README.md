# Introduction
This project was made to monitor my aquarium
There are three parts to this project
1) The temperature monitor that keeps track of the temperature throughout the day using the DS18B20 temperature sensor
2) A relay which can is triggered for a set duration of time to turn on the CO2 system
3) Two relays which can be triggered to control the lights of the aquarium
4) A servo motor to feed fish during a set time during the day
5) The Flask Web interface to control all the above via a web page
The webpage is accessible only in the local network and has not been exposed to the outside world

# Requirements
To run this project we need a Raspberry Pi board which has a wireless connection to the wifi and internet
Install the following packages
* sqlite
* python3
* sudo apt-get install python3-pigpio  #Also refer https://ben.akrin.com/raspberry-pi-servo-jitter/ for a jitter free servo experience
* sudo apt-get install python3-pil
* sudo pip3 install adafruit-circuitpython-ssd1306
* sudo pip3 install flask
* sudo pip3 install picamera


To get the code to autostart I followed the systemctl instructions mentioned in 

https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup/all


These services need to be created once the code is downloaded onto the Raspberry pi board.


As Part of this project the following services are started by systemctl on rpi boot
1. aquarium_server.service
2. aquarium_CO2.service
3. aquarium_lights.service
4. aquarium_OLED.service
5. aquarium_mail.service
6. aquarium_Temperature.service

These files are present in the ServiceFiles folder. Copy them over to /lib/systemd/system
Then run the following command
 sudo systemctl daemon-reload
 sudo systemctl enable aquarium_*.service
The Rpi GPIO pins used are
* Pin 26 for CO2 relay
* Pin 6 for Light1
* Pin 5 for Light2
* Pin 4 for 1-wire temp sensor
* Pin 18 for Fish feeder servo
