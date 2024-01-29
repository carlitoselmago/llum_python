from pythonosc import dispatcher, osc_server
from pyDMXController import pyDMXController
import threading

from classes.dmx_osc import dmx_osc

# Sensors
sensors = [
   {"type":"static","id":7},
   {"type":"dinamic","id":1,"minthreshold":0}
]

#fixtures, key is an unrealted to fixtures or sensors ids, its just for pairs targeting
fixtures={
    0:{"channels":range(1,59),"type":"new"},
    #1:{"channels":[7],"type":"new"}
}

# pairs of sensors and fixtures, the key = sensor
pairs={
    
    7:[{"fixture":0,"range":[10,60]}],
    1:[{"fixture":0,"range":[255,0]} ],
    
}
#pairs of sensors and audio controllers, audio has 0,1,2,3 controllers as targets
pairs_audio={
    1:[{"control":0,"range":[0.1,1]}]
}

DMXOSC=dmx_osc(oscport=54321,
                oscip="172.25.7.255",
               dmxport='/dev/ttyUSB0',
               device_type='enttec',
               margin_padding=0.2,
               audiodeviceindex=14,
               sensors=sensors,
               fixtures=fixtures,
               pairs=pairs,
               pairs_audio=pairs_audio,
               audioback="jack",
               skip_intro=True,
               endminutes=10000)

DMXOSC.dmx.update_channel(6,255) ### THIS IS ONLY FOR LOCAL TEST (minilead moving head)

#################################################################################
