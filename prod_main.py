from pythonosc import dispatcher, osc_server
from pyDMXController import pyDMXController
import threading

from classes.dmx_osc import dmx_osc

# Sensors
sensors = [
   {"type":"static","id":8},
    {"type":"dinamic","id":0}
]


#fixtures, key is an unrealted to fixtures or sensors ids, its just for pairs targeting
fixtures={
    #0:{"channels":list(range(1,56))},#list(range(1,56))
    1:{"channels":[1,2,3,4]},
    2:{"cannels":[5,6,7,8]},
    3:{"channels":[9,10,11,12]},
    4:{"channels":[13,14,15,16]},
    5:{"channels":[54,55,56]},
    6:{"channels":[51,52,53]},
    7:{"channels":[48,49,50]},
    8:{"channels":[42,43,44]},
    9:{"channels":[45,46,47]},
    10:{"channels":[32,33,34,35]},
    11:{"channels":[20,21,22,23]},
    12:{"channels":[24,25,26,27]},
    13:{"channels":[28,29,30,31]},
}

# pairs of sensors and fixtures, the key = sensor
pairs={
    
    8:[{"fixture":0,"range":[150,255]}],
    0:[{"fixture":0,"range":[255,10]} ],
    
}

DMXOSC=dmx_osc(oscport=54321,
               dmxport='/dev/ttyUSB0',
               device_type='enttec',
               margin_padding=0.2,
               audiodeviceindex=3,
               sensors=sensors,
               fixtures=fixtures,
               pairs=pairs)


#################################################################################
