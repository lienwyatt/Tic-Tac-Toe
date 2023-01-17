#basic I/O setup code for the MCP23017 used from manufacurer example found here:
#https://github.com/adafruit/Adafruit_CircuitPython_MCP230xx/blob/main/examples/mcp230xx_simpletest.py

import RPi.GPIO as GPIO
import time

import board
import busio
import digitalio

from adafruit_mcp230xx.mcp23017 import MCP23017

i2c = busio.I2C(board.SCL, board.SDA)

mcp = MCP23017(i2c)


 
'''
Tic-Tac-Toe board positions:

1|2|3
-|-|-
4|5|6
-|-|-
7|8|9
'''
#store LED position value of board positions
boardPositions = \
    [[0, 1, 2],
     [3, 4, 5],
     [6, 7, 8]]

#X and O outputs have different implementations because X outputs are wired from an I2C GPIO expander

#map X pins to layout positions
#positions are keys, MCP GPIO numbers are values
X_Pin_Position = {}
X_Pin_Position[0] = 1
X_Pin_Position[1] = 0
X_Pin_Position[2] = 8
X_Pin_Position[3] = 4
X_Pin_Position[4] = 3
X_Pin_Position[5] = 2
X_Pin_Position[6] = 7
X_Pin_Position[7] = 6
X_Pin_Position[8] = 5

#map O pins to layout locations
#positions are keys, Pi BCM numbers are values
O_Pin_Position = {}
O_Pin_Position[0] = 13
O_Pin_Position[1] = 19
O_Pin_Position[2] = 26
O_Pin_Position[3] = 11
O_Pin_Position[4] = 5
O_Pin_Position[5] = 6
O_Pin_Position[6] = 22
O_Pin_Position[7] = 10
O_Pin_Position[8] = 9

#switch posions are from left to right. 0-9 correspond to board positions. 10 is "game select"
#maps GPIO pins to switch numbers
#positions are keys, Pi BCM numbers are values
Switch_Position = {}
Switch_Position[0] = 20
Switch_Position[1] = 16
Switch_Position[2] = 12
Switch_Position[3] = 7
Switch_Position[4] = 8
Switch_Position[5] = 25
Switch_Position[6] = 24
Switch_Position[7] = 23
Switch_Position[8] = 18
#this last one is an extra switch to be used for choosing game mode
#Switch_Position[9] = 21



#set up GPIO expander outputs (X)
X_pins = {}
for pin in range(9):
    newPin = mcp.get_pin(X_Pin_Position[pin])
    newPin.switch_to_output(value=True)
    X_pins[X_Pin_Position[pin]] = newPin

#set up board outputs (O)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
for location in O_Pin_Position.values():
    GPIO.setup(location, GPIO.OUT)

#set up board inputs
for location in Switch_Position.values():
    GPIO.setup(location, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)#this one gets special treatment

#functions for toggling outputs
def turnOnX(position):
    X_pins[X_Pin_Position[position]].value = True
   
def turnOnO(position):
    GPIO.output(O_Pin_Position[position], True)

def turnOffX(position):
    X_pins[X_Pin_Position[position]].value = False

def turnOffO(position):
    GPIO.output(O_Pin_Position[position], False)

#switch callback functions
def sw_callback(pin):
    print("calling back")
    #callback gives us the pin value. We need the key from the dictionary
    for key, value in Switch_Position.items():
        if value == pin:
            location = key
           
#setup function for the extra switch to execute callback function
def setupExtraGPIO(function):
    GPIO.remove_event_detect(21)
    GPIO.add_event_detect(21, GPIO.FALLING, function, bouncetime=150)

#setup standard switches to execute callback function
def setupGPIO(function):
    for switch in Switch_Position.keys():
        GPIO.remove_event_detect(Switch_Position[switch])
    for switch in Switch_Position.keys():
        #print("switch:"+str(switch))
        GPIO.add_event_detect(Switch_Position[switch], GPIO.RISING, function, bouncetime=300)
       
def GPIO_Init():
    for location in range(9):
        turnOffO(location)
        turnOffX(location)
   
   
   
#test code. Shouldnt be called since this is meant to be an imported module
if (__name__ == "main"):
    for location in range(9):
        turnOffO(location)
        turnOffX(location)
    #for switch in Switch_Position.keys():
    #    GPIO.add_event_detect(Switch_Position[switch], GPIO.RISING, sw_callback, bouncetime=150)  
    while True:  
        for location in range(9):
            turnOnX(location)
            turnOnO(location)
            time.sleep(.25)
            turnOffO(location)
            turnOffX(location)
    turnOffO(location)
    turnOffX(location)
    #for switch in Switch_Position.keys():
    #    GPIO.add_event_detect(Switch_Position[switch], GPIO.RISING, sw_callback, bouncetime=150)  
    while True:  
        for location in range(9):
            turnOnX(location)
            turnOnO(location)
            time.sleep(1)
            turnOffO(location)
            turnOffX(location)
