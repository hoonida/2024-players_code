import time
import sys
import liblo as OSC

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

RST = None     # on the PiOLED this pin isnt used

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.load_default()
# font = ImageFont.truetype('Minecraftia.ttf', 8)


display_text = {
    0: "",
    1: "Eulji-ro 15-gil, Jung-gu, Seoul",
    2: "Eulji-ro, Jung-gu, Seoul",
    3: "Changgyeonggung-ro 5na-gil, Jung-gu, Seoul",
    4: "Changgyeonggung-ro 5-gil, Jung-gu, Seoul",
}

def handle_step(path, args):
    i = args[0]
    global display_text
    print("current step:", i)

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    draw.text((x, top), display_text[i],  font=font, fill=255)
    # draw.text((x, top+8), f"HOONIDA",  font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()

    #led_vals = [0] * len(leds)
    #led_vals[i] = 1
    #leds.value = tuple(led_vals)

# set up OSC client - send all messages to port 1234 on the local machine (rnbo>
try:
    target = OSC.Address(1234)
except OSC.AddressError as err:
    print(err)
    sys.exit()# set up OSC server - listening on port 4321

try:
    server = OSC.Server(4321)
except OSC.ServerError as err:
    print(err)

server.add_method("/rnbo/inst/0/messages/out/oled_step", 'i', handle_step)

# Set up RNBO OSC listener
OSC.send(target, "/rnbo/listeners/add", f"127.0.0.1:4321")




while True:

    server.recv(100)

    continue

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    draw.text((x, top), f"HELLO WORLD! HOONIDA",  font=font, fill=255)
    # draw.text((x, top+8), f"HOONIDA",  font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(.1)