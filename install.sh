sudo apt install portaudio19-dev
sudo apt-get install libsndfile1-dev
sudo apt-get install libportmidi-dev libportmidi0
sudo apt-get install liblo-dev
#sudo apt install python3-pyo
git clone https://github.com/belangeo/pyo.git
cd pyo
sudo sh scripts/compile_linux_withJack.sh
#sudo python setup.py install --use-double --use-jack
pip install -r requirements.txt


#raspberry with latest image
sudo apt update
sudo apt upgrade
sudo apt install  pipewire-jack -y
