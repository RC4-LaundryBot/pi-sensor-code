PI_NUMBER=`cat config.txt`
SERVER_IP=`cat server.txt`

content="#!/bin/bash
myIP=`hostname -I | tr -d \" \"`
echo $myIP | ssh orca@${SERVER_IP} \"cat - > ip${PI_NUMBER}.txt\""

touch /home/pi/setIP.sh
echo "$content" > /home/pi/setIP.sh

chmod a+x /home/pi/setIP.sh
 
sudo -c 'echo "sudo -i -u pi /home/pi/setIP.sh" >> /etc/xdg/lxsession/LXDE-pi/autostart'