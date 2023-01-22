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
* Also refer https://ben.akrin.com/raspberry-pi-servo-jitter/ for a jitter free servo experience

To get the code to autostart I followed the systemctl instructions mentioned in https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup/all
These services need to be created once the code is downloaded onto the Raspberry pi board.
As Part of this project the following services are started by systemctl on rpi boot
aquarium_server.service
aquarium_CO2.service
aquarium_lights.service
aquarium_OLED.service
aquarium_mail.service
aquarium_Temperature.service

The Rpi GPIO pins used are
Pin 26 for CO2 relay
Pin 6 for Light1
Pin 5 for Light2
Pin 4 for 1-wire temp sensor
Pin 18 for Fish feeder servo
