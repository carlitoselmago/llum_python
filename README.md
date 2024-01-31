# Llum python

## Install pyo on raspberry (with jack support)

sudo apt-get install python-dev libjack-jackd2-dev libportmidi-dev portaudio19-dev liblo-dev libsndfile-dev python-dev python-tk python-imaging-tk python-wxgtk2.8

git clone https://github.com/belangeo/pyo

cd  pyo

sudo python setup.py install --use-jack --use-double

#install jack
git clone https://github.com/jackaudio/jack2.git
cd jack2
./waf configure
./waf
sudo ./waf install
