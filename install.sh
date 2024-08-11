sudo apt-get -y update
sudo apt-get -y install git python3-pip liblo-dev spidev i2c-tools

sudo apt remove python3-rpi.gpio
sudo apt install python3-rpi-lgpio

pip install -r requirements.txt --break-system-packages
