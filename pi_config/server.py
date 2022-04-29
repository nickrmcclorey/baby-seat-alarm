#!/usr/bin/python3
import RPi.GPIO as gpio
import time
from threading import Thread
from flask import Flask
from flask import cli

# set up gpio
gpio.setmode(gpio.BCM)
gpio.setup(26, gpio.IN)
# set up flask
app = Flask(__name__)

babyInCar = False
readings = [1 for x in range(0, 10)]
readingsIndex = 0
keepReading = True

@app.route('/')
def hello_world():
    return str(babyInCar)


def updateGpio():
    global readingsIndex
    global readings
    global babyInCar
    while keepReading:
        readings[readingsIndex] = gpio.input(26)
        readingsIndex = (readingsIndex + 1) % 10
        babyInCar = (sum(readings) < 1)
        time.sleep(1)

try:
    if __name__ == '__main__':
        gpioThread = Thread(target=updateGpio);
        gpioThread.start()
        cli.show_server_banner = lambda *_:None 
        app.run(host='0.0.0.0',port=5000)
        keepReading = False
        gpioThread.join()

finally:
    gpio.cleanup()
