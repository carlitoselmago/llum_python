#!/bin/bash

# Update and Install JACK Audio Connection Kit
sudo apt-get update
sudo apt-get install -y jackd2 screen

# Add user "pi" to the audio group
sudo usermod -a -G audio pi

# Configure HiFiBerry DAC in /boot/config.txt
echo "Configuring HiFiBerry DAC..."
sudo sed -i '/dtoverlay=hifiberry-dac/d' /boot/config.txt
echo "dtoverlay=hifiberry-dac" | sudo tee -a /boot/config.txt > /dev/null

# Create a systemd service for JACK
echo "Creating systemd service for JACK..."
sudo bash -c 'cat << EOF > /etc/systemd/system/jackd.service
[Unit]
Description=JACK Sound Server

[Service]
ExecStart=/usr/bin/jackd -d alsa -d hw:3,0
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
EOF'

# Enable and start the JACK service
sudo systemctl daemon-reload
sudo systemctl enable jackd
sudo systemctl start jackd

echo "JACK Audio Connection Kit installation and configuration complete."
