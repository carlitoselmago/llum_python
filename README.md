# Llum python

## Install pyo on raspberry (with jack support)

sudo apt-get install python-dev libjack-jackd2-dev libportmidi-dev portaudio19-dev liblo-dev libsndfile-dev python-dev python-tk python-imaging-tk python-wxgtk2.8

git clone https://github.com/belangeo/pyo

cd  pyo

sudo python setup.py install --use-jack --use-double

-----

### fedora install
I recommend using conda:
```
sudo yum install python-devel
pip install pyserial
conda install -c conda-forge gcc=12.1.0
pip install --user pyo
```
### Windos config
Server(buffersize=1024, duplex=0, winhost="asio") 
https://belangeo.github.io/pyo/winaudioinspect.html
