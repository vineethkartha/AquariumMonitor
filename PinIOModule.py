import RPi.GPIO as gpio

class PinIOModule:
    anode=0;
    def __init__(self, anode):
        self.anode = anode;
        gpio.setwarnings(True)           
        gpio.setmode(gpio.BCM)
        gpio.setup(anode,gpio.OUT)

    def __del__(self):
        gpio.output(self.anode, False)
        gpio.setup(self.anode,gpio.IN)
                
    def TurnOn(self):
        gpio.output(self.anode, True)

    def TurnOff(self):
        gpio.output(self.anode, False)

