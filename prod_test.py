from pythonosc import dispatcher, osc_server
from pyDMXController import pyDMXController
from classes.helpers import *
import threading

from classes.dmx_osc import dmx_osc

# Sensors
sensors = [
    #estaticos
    {"type":"static","id":6},
    {"type":"static","id":7},
    {"type":"static","id":8},
    {"type":"static","id":9},
    {"type":"static","id":10},
    #dinamicos
    {"type":"dinamic","id":0},
    {"type":"dinamic","id":1},
    {"type":"dinamic","id":2}, #-> usado para sala pequeña
    {"type":"dinamic","id":3}, 
    {"type":"dinamic","id":4},
    {"type":"dinamic","id":5}, # CORTINA

    #test respuesto
    {"type":"dinamic","id":11},
    {"type":"dinamic","id":12},

]


#fixtures, key is an unrealted to fixtures or sensors ids, its just for pairs targeting
fixtures={
    #0:{"channels":list(range(1,56))},#list(range(1,56))
    1:{"channels":[1,2,3,4],"type":"new"},
    2:{"channels":[5,6,7,8],"type":"new"},
    3:{"channels":[9,10,11,12],"type":"new"},
    #4:{"channels":[13,14,15,16],"type":"new"},

    5:{"channels":[54,55,56],"type":"old"},
    6:{"channels":[51,52,53],"type":"old"},
    7:{"channels":[48,49,50],"type":"old"},
    8:{"channels":[42,43,44],"type":"old"},
    9:{"channels":[45,46,47],"type":"old"},

    #10:{"channels":[70,71,72,73],"type":"new"},
    11:{"channels":[20,21,22,23],"type":"new"},
    12:{"channels":[24,25,26,27],"type":"new"},
    13:{"channels":[28,29,30,31],"type":"new"},

    #14:{"channels":[81,82,83,84],"type":"new"}, #humo

    #balcon
    14:{"channels":[30,31,32],"type":"old"},
    15:{"channels":[36,37,38],"type":"old"},
    16:{"channels":[33,34,35],"type":"old"},

    17:{"channels":[64,65,66],"type":"old"},
   
    #60:{"channels":[80],"type":"old"},
}

rangoreposo=[10,60]
rangoAD=[100,0]
rangoADplus=[200,0]
rangoADplus2=[300,-100]
negativo=[-355,0]


adelante=[ #hipersensible
    {"fixture":5,"range":[1455,-100]},
    {"fixture":6,"range":[1455,-100]},
    {"fixture":7,"range":[1455,-100]},
    {"fixture":8,"range":[1455,-100]},
    {"fixture":9,"range":[1455,-100]},
]

izq=[#hipersensible
    {"fixture":1,"range":[255,0]},
    {"fixture":2,"range":[255,0]},
    {"fixture":3,"range":[255,0]},
   
]
der=[#hipersensible
   
    {"fixture":11,"range":[1455,0]},
    {"fixture":12,"range":[1455,0]},
    {"fixture":13,"range":[1455,0]},
]
arriba=[{"fixture":17,"range":[255,0]},
        {"fixture":14,"range":[255,0]},
        {"fixture":15,"range":[255,0]},
        {"fixture":16,"range":[255,0]}
]

abajonegativo=[
    {"fixture":1,"range":negativo},
    {"fixture":2,"range":negativo},
    {"fixture":3,"range":negativo},
    
    {"fixture":5,"range":negativo},
    {"fixture":6,"range":negativo},
    {"fixture":7,"range":negativo},
    {"fixture":8,"range":negativo},
    {"fixture":9,"range":negativo},

   
    {"fixture":11,"range":negativo},
    {"fixture":12,"range":negativo},
    {"fixture":13,"range":negativo},
]

# pairs of sensors and fixtures, the key = sensor


pairs={
    
    12:izq,#izq

    11:abajonegativo+arriba
    
# HACER QUE SENSOR 2 TENG RANGO NEGATIVO PARA QUE RESTE EN LA LINEA

}


#pairs of sensors and audio controllers, audio has 0,1,2,3 controllers as targets
pairs_audio={
    #cortina
    5:[{"control":0,"range":[10,20000]}],
    
    #repos #TODO check , mateix problema de solapament, deixar 10 si es molt lio
    #7:[{"control":2,"range":[1.0,0.7]}],
    #8:[{"control":2,"range":[1.0,0.7]}],
    #9:[{"control":2,"range":[1.0,0.7]}],
    #10:[{"control":2,"range":[1.0,0.7]}],
    
    # TODO: aquests es trepitja lultim, haurien de coexistir
    #0:[{"control":1,"range":[1.0,0]}],
    #6:[{"control":1,"range":[1.0,0]}],
    1:[{"control":1,"range":[1.0,0]}],

    #reverb #TODO: check mismo caso que grupo anterior
    #2:[{"control":3,"range":[1,0.1]}] ,
    #3:[{"control":3,"range":[1,0.1]}] ,
    4:[{"control":3,"range":[1,0.1]}] 
}

DMXOSC=dmx_osc(oscport=54321,
            oscip="172.25.7.255",
               dmxport='/dev/ttyUSB0',
               device_type='enttec',
               #dmxport='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0',
               #device_type='ftdi',
               margin_padding=0.2,
               audiodeviceindex=3,
               sensors=sensors,
               fixtures=fixtures,
               pairs=pairs,
               pairs_audio=pairs_audio,
               audioback="jack",
               skip_intro=True,
               skip_fadein=True,
               endminutes=10)

#################################################################################
