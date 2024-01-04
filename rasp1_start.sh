#!/bin/bash
cd /home/pi/llum_python
git pull
sleep 5
screen -d -m -t myjackdserver sh jackd -d alsa -d hw:3,0
sleep 5
python rasp1.py