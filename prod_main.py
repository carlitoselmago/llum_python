from pythonosc import dispatcher, osc_server
from pyDMXController import pyDMXController
import threading

from classes.dmx_osc import dmx_osc

# Sensors
sensors = [
    #estaticos
    {"type":"static","id":6},
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
    {"type":"dinamic","id":5} # CORTINA
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

    #14:{"channels":[61,62,63,64],"type":"new"},
    #60:{"channels":[60],"type":"old"},
}
adelante=[
    {"fixture":5,"range":[1455,-100]},
    {"fixture":6,"range":[1455,-100]},
     {"fixture":7,"range":[1455,-100]},
      {"fixture":8,"range":[1455,-100]},
       {"fixture":9,"range":[1455,-100]},
]

izq=[
    {"fixture":1,"range":[1455,0]},
    {"fixture":2,"range":[1455,0]},
     {"fixture":3,"range":[1455,0]},
      {"fixture":4,"range":[1455,0]},
]
der=[
     {"fixture":10,"range":[1455,0]},
    {"fixture":11,"range":[1455,0]},
     {"fixture":12,"range":[1455,0]},
      {"fixture":13,"range":[1455,0]},
]
# pairs of sensors and fixtures, the key = sensor
pairs={
     #REPOSOS
    6:[{"fixture":5,"range":[10,60]},
       {"fixture":10,"range":[10,60]},
       {"fixture":1,"range":[10,60]},
       {"fixture":13,"range":[10,60]},
       {"fixture":8,"range":[10,60]},]  ,

    #ACCION DIRECTA
    0:izq,
    1:der,
    #2:TODOS LOS DE ARRIBA
    3: adelante,
    4:[ {"fixture":1,"range":[1455,0]},
        {"fixture":4,"range":[1455,0]},
       {"fixture":7,"range":[100,0]},
       {"fixture":10,"range":[14255,0]},
       {"fixture":12,"range":[1455,0]}], 
    5:[ {"fixture":2,"range":[200,0]}, 
       {"fixture":5,"range":[200,0]}, 
       {"fixture":11,"range":[200,0]} ],
    6:[ {"fixture":5,"range":[200,0]},
        {"fixture":10,"range":[200,0]},
        {"fixture":13,"range":[200,0]} ,
        {"fixture":8,"range":[200,0]} ],
    7:[ {"fixture":9,"range":[100,0]},
        {"fixture":6,"range":[100,0]},
        {"fixture":3,"range":[200,0]} ],
    8:[ {"fixture":8,"range":[100,0]},
        {"fixture":4,"range":[100,0]},
        {"fixture":2,"range":[100,0]} ],
    9:[ {"fixture":1,"range":[100,0]},
        {"fixture":12,"range":[100,0]},
        {"fixture":7,"range":[100,0]} ],
    10:[ {"fixture":5,"range":[100,0]},
        {"fixture":11,"range":[100,0]},
        {"fixture":13,"range":[100,0]} ],
      

}


#pairs of sensors and audio controllers, audio has 0,1,2,3 controllers as targets
pairs_audio={
   5:[{"control":0,"range":[10,20000]}],
    1:[{"control":1,"range":[0.1,1]}],
    2:[{"control":2,"range":[0.1,1]}],
    3:[{"control":3,"range":[0.1,1]}]
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
               pairs_audio=pairs_audio,
               audioback="jack",
               skip_intro=True,
               endminutes=5)

#################################################################################
