from pyo import *
s=Server(sr=44100, nchnls=2, buffersize=256, duplex=1)
s.setOutputDevice(12)
s.boot()                    # boot the server
sin = Sine(mul=0.5)         # start a single sine stream
sin.out()                   # send this sine stream to audio ouput
s.start()                   # start the server

# Keep the script running for a specified duration
try:
    # Run for a certain duration (e.g., 30 seconds)
    time.sleep(30)
except KeyboardInterrupt:
    pass

# Stop the server
s.stop()