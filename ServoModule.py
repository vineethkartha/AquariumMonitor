import RPi.GPIO as gpio
import pigpio
import time

class Servo:
       servoPin=18
       delay=0.1
       freq = 50
       servoMotor='';
       minDutyCycle = 600;
       maxDutyCycle = 2300;
       def __init__(self,servoPin,delay=0.01, freq=50, minDutyCycle=2, maxDutyCycle=11):
              self.servoPin = servoPin
              self.delay = delay
              self.freq = freq
              self.minDutyCycle=minDutyCycle
              self.maxDutyCycle=maxDutyCycle              
              self.servoMotor=pigpio.pi()
              self.servoMotor.set_mode(self.servoPin, pigpio.OUTPUT)
              self.servoMotor.set_PWM_frequency(self.servoPin, self.freq)

       def findDutyCycleForAngle(self,angle):
              dutyCycle = (self.maxDutyCycle-self.minDutyCycle)/180.0 *angle
              print(dutyCycle)
              return dutyCycle
       def start(self,angle):
              self.servoMotor.set_PWM_frequency(self.servoPin,self.freq)
       def stop(self):
              self.servoMotor.set_PWM_dutycycle(self.servoPin,0)
              self.servoMotor.set_PWM_frequency(self.servoPin,0)
       def moveToAngle(self,angle):
              #self.servoMotor.set_servo_pulsewidth(self.servoPin,self.findDutyCycleForAngle(angle))
              self.servoMotor.set_servo_pulsewidth(self.servoPin,angle)
              time.sleep(self.delay)
              
