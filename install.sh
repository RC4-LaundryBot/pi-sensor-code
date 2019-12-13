#!/bin/bash

# install required python packages
sudo apt-get update
sudo apt-get install python-requests

# add crontab to restart once per day
echo "15 4 * * * /sbin/shutdown -r now" > tmp
sudo crontab tmp
rm tmp

# create configuration file
touch config.txt
echo $1 > config.txt

# install sensor script as service
sudo cp ~/sensor.service /lib/systemd/system/sensor.service

sudo chmod 644 /lib/systemd/system/sensor.service
chmod +x /home/pi/sensor.py
sudo systemctl daemon-reload
sudo systemctl enable sensor.service
sudo systemctl start sensor.service

# add network configuration
sudo cp ~/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf
sudo cp ~/interfaces /etc/network/interfaces

# restart
sudo reboot
