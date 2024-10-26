# Setup Basic Environment
sudo apt-get -y update
sudo apt-get -y install git python3-pip

# Setup SPI & I2C
sudo apt-get -y install i2c-tools
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0
sudo i2cdetect -y 1

# Setup GPIO Library
sudo apt -y remove python3-rpi.gpio
sudo apt -y install python3-rpi-lgpio
sudo apt-get -y install liblo-dev
pip uninstall -y RPi.GPIO --break-system-packages

# Setup Python
sudo apt-get -y install libopenblas-dev # for numpy
sudo apt-get -y install libopenjp2-7 # for PIL
pip install -r requirements.txt --break-system-packages

# Setup Services
sudo bash service/adc/install.sh
sudo bash service/encoder/install.sh
sudo bash service/oled/install.sh
sudo bash service/tof/install.sh