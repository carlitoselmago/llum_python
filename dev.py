from pythonosc import dispatcher, osc_server
from pyDMXController import pyDMXController
import threading

from classes.dmx_osc import dmx_osc

# Sensors
sensors = [
   {"type":"static","id":7},
    {"type":"dinamic","id":0}
]

#fixtures, key is an unrealted to fixtures or sensors ids, its just for pairs targeting
fixtures={
    0:{"channels":[10],"type":"new"},
    1:{"channels":[7],"type":"new"}
}

# pairs of sensors and fixtures, the key = sensor
pairs={
    
    7:[{"fixture":1,"range":[150,255]}],
    0:[{"fixture":1,"range":[255,0]} ],
    
}

DMXOSC=dmx_osc(oscport=54321,
               oscip="localhost",
               dmxport='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0',
               device_type='ftdi',
               margin_padding=0.2,
               audiodeviceindex=12,
               sensors=sensors,
               fixtures=fixtures,
               pairs=pairs)


#################################################################################
