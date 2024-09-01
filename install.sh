sudo apt-get -y update
sudo apt-get -y install git python3-pip liblo-dev spidev i2c-tools
sudo apt-get -y install libopenblas-dev # for numpy
sudo apt-get -y install libopenjp2-7 # for PIL

sudo apt -y remove python3-rpi.gpio
sudo apt -y install python3-rpi-lgpio

pip install -r requirements.txt --break-system-packages

# Setup I2C
sudo raspi-config nonint do_i2c 0
sudo i2cdetect -y 1

# Setup SPI
sudo raspi-config nonint do_spi 0