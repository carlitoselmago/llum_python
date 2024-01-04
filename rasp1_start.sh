#!/bin/bash
cd /home/pi/llum_python
git pull
#jackd -d alsa -d hw:3,0 &
python rasp1.py