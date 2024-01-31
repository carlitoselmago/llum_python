# Llum python

## Install pyo on raspberry (with jack support)
```
sudo apt-get install python3-dev libjack-jackd2-dev libportmidi-dev portaudio19-dev liblo-dev libsndfile-dev python3-tk  python3-wxgtk4.0 
git clone https://github.com/belangeo/pyo
cd  pyo
sudo python setup.py install --use-jack --use-double
```
## install jack
```
sudo apt-get install -y libasound2-dev libsndfile1-dev libreadline-dev libreadline6-dev libtinfo-dev
git clone https://github.com/jackaudio/jack2.git --depth 1
cd jack2
./waf configure --prefix /usr
./waf build
sudo ./waf install
sudo ldconfig
sudo sh -c "echo @audio - memlock 256000 >> /etc/security/limits.conf"
sudo sh -c "echo @audio - rtprio 75 >> /etc/security/limits.conf"
```
