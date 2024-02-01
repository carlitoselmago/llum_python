from pythonosc import dispatcher, osc_server
from pyDMXController import pyDMXController
import threading

from classes.dmx_osc import dmx_osc

# Sensors
sensors = [
    #estaticos
    {"type":"static","id":4},
    {"type":"static","id":5},
    {"type":"static","id":6},
    #{"type":"static","id":10},
    #dinamicos
    {"type":"dinamic","id":0},
    {"type":"dinamic","id":1},
    {"type":"dinamic","id":2},
    {"type":"dinamic","id":3},
    
]


#fixtures, key is an unrealted to fixtures or sensors ids, its just for pairs targeting
fixtures={
    0:{"channels":list(range(42,57)),"type":"old"},#list(range(1,56))

    1:{"channels":list(range(1,17)),"type":"new"}, # fila izq new
    2:{"channels":list(range(20,36)),"type":"new"}, #fila der new

    #3:{"channels":list(range(61,64)),"type":"fog"}

}
allfixtures=[{"fixture":0,"range":[255,0]},
       {"fixture":1,"range":[255,0]},
        {"fixture":2,"range":[255,0]}]
# pairs of sensors and fixtures, the key = sensor
pairs={
    #passive ###################################3
    4:[{"fixture":0,"range":[10,60]}],
    5:[{"fixture":1,"range":[10,60]}],
    6:[{"fixture":2,"range":[10,60]}],
    #direct ####################################33
    0:allfixtures,
    1:[{"fixture":1,"range":[255,0]}],
    2:[{"fixture":2,"range":[255,0]}],
    #3:allfixtures
}

#for i in range(1,4):
#    pairs[4].append({"fixture":i,"range":[150,255]})

#for i in range(1,4):
#    pairs[0].append({"fixture":i,"range":[255,0]})


#pairs of sensors and audio controllers, audio has 0,1,2,3 controllers as targets
pairs_audio={
    0:[{"control":0,"range":[10,20000]}],
    1:[{"control":1,"range":[0.1,1]}],
    2:[{"control":2,"range":[0.1,1]}],
    3:[{"control":3,"range":[0.1,1]}]
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
               skip_intro=True,
               endminutes=400)


#################################################################################
