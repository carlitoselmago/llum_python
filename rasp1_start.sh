#!/bin/bash
cd /home/pi/llum_python
git pull
screen -d -m -t myjackdserver sh jackd -d alsa -d hw:3,0
sleep 40
python rasp1.py