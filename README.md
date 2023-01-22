# Requirements
* sqlite
* python3
This is a project to monitor an Aquarium
There are three parts to this project
1) The temperature monitor that keeps track of the temperature throughout the day
2) The CO2 control system that turns on/off the valve based on specified times
3) The Flask Web interface


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