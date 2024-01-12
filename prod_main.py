from pythonosc import dispatcher, osc_server
from pyDMXController import pyDMXController
import threading

from classes.dmx_osc import dmx_osc

# Sensors
sensors = [
    #estaticos
   {"type":"static","id":7},
    {"type":"static","id":8},
    {"type":"static","id":9},
  #  {"type":"static","id":10},
    #dinamicos
    {"type":"dinamic","id":0},
    {"type":"dinamic","id":1},
    #{"type":"dinamic","id":2}, -> usado para sala pequeña
    {"type":"dinamic","id":3},
    {"type":"dinamic","id":4},
    {"type":"dinamic","id":5}
]


#fixtures, key is an unrealted to fixtures or sensors ids, its just for pairs targeting
fixtures={
    #0:{"channels":list(range(1,56))},#list(range(1,56))
    1:{"channels":[1,2,3,4],"type":"new"},
    2:{"channels":[5,6,7,8],"type":"new"},
    3:{"channels":[9,10,11,12],"type":"new"},
    4:{"channels":[13,14,15,16],"type":"new"},
    5:{"channels":[54,55,56],"type":"old"},
    6:{"channels":[51,52,53],"type":"old"},
    7:{"channels":[48,49,50],"type":"old"},
    8:{"channels":[42,43,44],"type":"old"},
    9:{"channels":[45,46,47],"type":"old"},
    10:{"channels":[32,33,34,35],"type":"new"},
    11:{"channels":[20,21,22,23],"type":"new"},
    12:{"channels":[24,25,26,27],"type":"new"},
    13:{"channels":[28,29,30,31],"type":"new"},

    14:{"channels":[61,62,63,64],"type":"new"},

    60:{"channels":[60],"type":"old"},
}

# pairs of sensors and fixtures, the key = sensor
pairs={
    #passive ###################################3
     7:[
        {"fixture":2,"range":[150,255]},
        {"fixture":10,"range":[150,255]},
    ],
     8:[
        {"fixture":6,"range":[150,255]},
         {"fixture":3,"range":[150,255]},
    ],
     9:[
        {"fixture":4,"range":[150,255]},
        {"fixture":11,"range":[150,255]},
    ],
    #10:[], #los de arriba
   
    #direct ####################################33
   
    #2:[],
    3:[],
    4:[
         {"fixture":5,"range":[0,255]},
         {"fixture":13,"range":[0,255]},
    ],
    5:[
         {"fixture":1,"range":[0,255]},
         {"fixture":12,"range":[0,255]},
        {"fixture":7,"range":[0,255]},
    ],
    6:[
        {"fixture":4,"range":[0,255]},
        {"fixture":9,"range":[0,255]},
    ],
     0:[],  
    #2:[{"fixture":60,"range":[0,10]}],
    1:[],
   
}

for i in range(5,9):
    pairs[3].append({"fixture":i,"range":[0,255]})

for i in range(1,4):
    pairs[0].append({"fixture":i,"range":[0,255]})

for i in range(10,14):
    pairs[1].append({"fixture":i,"range":[0,255]})

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
