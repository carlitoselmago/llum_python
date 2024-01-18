from pythonosc import dispatcher, osc_server
from pyDMXController import pyDMXController
import threading

from classes.dmx_osc import dmx_osc

# Sensors
sensors = [
    #estaticos
    {"type":"static","id":7},
    {"type":"static","id":3},
    {"type":"static","id":2},
    #{"type":"static","id":10},
    #dinamicos
    {"type":"dinamic","id":1},
   # {"type":"dinamic","id":1},
   # {"type":"dinamic","id":3},
   # {"type":"dinamic","id":4},
]


#fixtures, key is an unrealted to fixtures or sensors ids, its just for pairs targeting
fixtures={
    0:{"channels":list(range(1,59)),"type":"old"},#list(range(1,56))
    #1:{"channels":[1,2,3,4],"type":"new"},
    #2:{"channels":[5,6,7,8],"type":"new"},
    #3:{"channels":[9,10,11,12],"type":"new"},
    #4:{"channels":[13,14,15,16],"type":"new"},
    #1:{"channels":list(range(1,16)),"type":"new"},
    #2:{"channels":list(range(28,35)),"type":"new"}

}

# pairs of sensors and fixtures, the key = sensor
pairs={
    #passive ###################################3
    #3:[{"fixture":1,"range":[0,40]}],
    7:[{"fixture":0,"range":[0,40]}],
    #2:[{"fixture":2,"range":[0,40]}],
    #direct ####################################33
    1:[{"fixture":0,"range":[255,0]}]

    
   
}

#for i in range(1,4):
#    pairs[4].append({"fixture":i,"range":[150,255]})

#for i in range(1,4):
#    pairs[0].append({"fixture":i,"range":[255,0]})


#pairs of sensors and audio controllers, audio has 0,1,2,3 controllers as targets
pairs_audio={
   2:[{"control":0,"range":[100,20000]}],
    1:[{"control":1,"range":[0.1,1]}],
    3:[{"control":2,"range":[0.1,1]}],
    4:[{"control":3,"range":[0.1,1]}]
   # 0:[{"control":2,"range":[0.9,1]}]
}

DMXOSC=dmx_osc(oscport=54321,
               #oscip="localhost",
               oscip="172.25.7.255",
               dmxport='/dev/ttyUSB0',
               device_type='enttec',
               margin_padding=0.2,
               audiodeviceindex=3,
               sensors=sensors,
               fixtures=fixtures,
               pairs=pairs,
               pairs_audio=pairs_audio,
               audioback="jack",
               skip_intro=False,
               endminutes=4)


#################################################################################
