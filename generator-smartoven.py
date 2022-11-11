import json
import requests
from datetime import datetime
from fhict_cb_01.CustomPymata4 import CustomPymata4
import time, sys


DHTPIN  = 12
BUTTON1 = 8
number = 3
level = 1
prevLevel = 1
LED_RED = [4]
LED_GREEN = [5]

data = ["time", "temp", "timer", "ovenID"]

def setup():
    global board
    board = CustomPymata4(com_port = "COM4")
    board.set_pin_mode_dht(DHTPIN, sensor_type=11, differential=.05)
    board.displayOn()
    board.set_pin_mode_digital_input_pullup(BUTTON1, callback = ButtonChanged)
    for pin in LED_RED:
        board.set_pin_mode_digital_output(pin)
    for pin in LED_GREEN:
        board.set_pin_mode_digital_output(pin)

def ButtonChanged(data):
    global level
    level = data[2]


def current_time():
    rightNow = datetime.now()
    time = rightNow.strftime("%I:%M%p")
    time = time.lstrip('0')
    time = time.lower()
    return time 



def current_temperature():
    humidity, temperature,  timestamp = board.dht_read(DHTPIN)
    time.sleep(0.01)
    temperature = temperature + 160
    return temperature

def loop():
    if (level != prevLevel):
        global number
        while number > -1:
            if number != 0:
                number -= 1
                for pin in LED_GREEN:
                    board.digital_pin_write(pin, 0)
                for pin in LED_RED:
                    board.digital_pin_write(pin, 1)
                board.displayShow(number) 
                return number
            elif number == 0:
                for pin in LED_RED:
                    board.digital_pin_write(pin, 0)
                for pin in LED_GREEN:
                    board.digital_pin_write(pin, 1)
                return number
    else:
        number = 3
        return number
    time.sleep(0.01)

setup()
while True:
    time.sleep(0.01)
    data = [current_time, current_temperature, loop]
    jsonData = {'time' : current_time(), 'temperature' : current_temperature(), 'timer' : loop(), 'ovenID' : '1'}
    response = requests.post("http://localhost:5000/oven_data", json = jsonData)
