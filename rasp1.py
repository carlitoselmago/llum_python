from pythonosc import dispatcher, osc_server
from pyDMXController import pyDMXController
import threading

from classes.dmx_osc import dmx_osc

# Sensors
sensors = [
   {"type":"static","id":11},
    {"type":"dinamic","id":0},
   {"type":"dinamic","id":1}
]

#fixtures, key is an unrealted to fixtures or sensors ids, its just for pairs targeting
fixtures={
   # 0:{"channels":[10],"type":"new"},
    1:{"channels":[range(1,255)],"type":"new"}
}

# pairs of sensors and fixtures, the key = sensor
pairs={
    
    11:[{"fixture":1,"range":[30,0]}],
    0:[{"fixture":1,"range":[255,0]} ],
    
}
#pairs of sensors and audio controllers, audio has 0,1,2,3 controllers as targets
pairs_audio={
   
    0:[ 
      {"control":1,"range":[60,2000]},
        #{"control":0,"range":[0.1,1]},
     ],
     1:[ 
       # {"control":1,"range":[60,2000]},
        {"control":2,"range":[0.9,1]},
     ]
    
}
DMXOSC=dmx_osc(oscport=54321,
                oscip="172.25.7.255",
               #dmxport='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0',
               #device_type='ftdi',
               dmxport='/dev/ttyUSB0',
               device_type='enttec',
               margin_padding=0.2,
               audiodeviceindex=2,
               sensors=sensors,
               fixtures=fixtures,
               pairs=pairs,
               pairs_audio=pairs_audio)


#################################################################################
