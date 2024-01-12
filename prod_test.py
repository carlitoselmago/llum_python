from pythonosc import dispatcher, osc_server
from pyDMXController import pyDMXController
import threading

from classes.dmx_osc import dmx_osc

# Sensors
sensors = [
    #estaticos
   {"type":"static","id":4},
  #  {"type":"static","id":10},
    #dinamicos
    {"type":"dinamic","id":0},
]


#fixtures, key is an unrealted to fixtures or sensors ids, its just for pairs targeting
fixtures={
    #0:{"channels":list(range(1,56))},#list(range(1,56))
    1:{"channels":[1,2,3,4],"type":"new"},
    2:{"channels":[5,6,7,8],"type":"new"},
    3:{"channels":[9,10,11,12],"type":"new"},
    4:{"channels":[13,14,15,16],"type":"new"},
}

# pairs of sensors and fixtures, the key = sensor
pairs={
    #passive ###################################3
    4:[],
    #direct ####################################33
    0:[],
   
}

for i in range(1,4):
    pairs[4].append({"fixture":i,"range":[150,255]})

for i in range(1,4):
    pairs[0].append({"fixture":i,"range":[0,255]})


#pairs of sensors and audio controllers, audio has 0,1,2,3 controllers as targets
pairs_audio={
   # 0:[{"control":0,"range":[60,2000]}],
    1:[{"control":1,"range":[0.1,1]}],
   # 0:[{"control":2,"range":[0.9,1]}]
}

DMXOSC=dmx_osc(oscport=54321,
               oscip="172.25.7.255",
               dmxport='/dev/ttyUSB0',
               device_type='enttec',
               margin_padding=0.2,
               audiodeviceindex=3,
               sensors=sensors,
               fixtures=fixtures,
               pairs=pairs,
               pairs_audio=pairs_audio)


#################################################################################
