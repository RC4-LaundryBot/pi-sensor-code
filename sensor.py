from time import sleep
import requests
import RPi.GPIO as gpio
from pathlib import Path

pin = [7, 11, 13, 15]

status = [0, 0, 0, 0]
oncount = [0, 0, 0, 0]
offcount = [0, 0, 0, 0]
readout = [0, 0, 0, 0]

# Setup pins
gpio.setmode(gpio.BOARD)
for i in range(4):
    gpio.setup(pin[i], gpio.IN)

# Load floorcode from config file
path = Path.home().joinpath("config.txt")
file = path.open()
floorcode = file.read()
floorcode = floorcode.strip()

while(True):
    statusChanged = False;


    for i in range(4):
        readout[i] = gpio.input(pin[i])

    for i in range(4):
        if (readout[i] == 1):
            oncount[i] = 0
            offcount[i] += 1
        else:
            offcount[i] = 0
            oncount[i] += 1

        if (offcount[i] > 8):
            offcount[i] = 8

        if (oncount[i] > 8):
            oncount[i] = 8

        if (offcount[i] >= 8 and status[i] != 0):
            status[i] = 0
            offcount[i] = 0
            statusChanged = True;
        elif (oncount[i] >= 8 and status[i] != 1):
            oncount[i] = 0
            status[i] = 1
            statusChanged = True;
        elif (offcount[i] > 1 and status[i] == 1):
           status[i] = 2
           statusChanged = True;
        elif (oncount[i] > 1 and status[i] == 0):
            status[i] = 2
            statusChanged = True;

    res = ''.join(str(e) for e in status)

    if (statusChanged):
        print("change detected")
        print(res)
        requests.post("https://us-central1-rc4laundrybot.cloudfunctions.net/writeData",
        data = {
            "floor":floorcode,
            "data":res
        })
        statusChanged = False

    sleep(0.15)
