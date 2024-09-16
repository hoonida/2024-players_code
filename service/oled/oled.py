import os
import atexit
import time
import logging

import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def get_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_text = s.getsockname()[0]
    s.close()
    return ip_text


def main():

    # 128x64 display with hardware I2C:
    disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)

    # Initialize library.
    disp.begin()

    # Clear display.
    disp.clear()
    disp.display()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    screen_size = (disp.width, disp.height)

    image = Image.new('1', screen_size)

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, *screen_size), outline=0, fill=0)

    # Load default font.
    font = ImageFont.load_default()

    # Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
    # Some other nice fonts to try: http://www.dafont.com/bitmap.php
    font = ImageFont.truetype('HomeVideo-Regular.ttf', 20)
    text = f"HELLO WORLD!"
    text = text + "      " + text

    y_offset = 10
    x_offset = 0

    def get_text_size(font, text):
        text += "    "
        text_width, _ = font.getsize(text)
        text += text
        return text, text_width

    text, max_offset = get_text_size(font, text)


    def terminate_callback():
        draw.rectangle((0, 0, *screen_size), outline=0, fill=0)
        draw.text((0, 0), 'BYE!',  font=font, fill=255)
        disp.image(image)
        disp.display()
    atexit.register(terminate_callback)


    ip_text = get_ip()
    draw.text((x_offset, y_offset), ip_text,  font=font, fill=255)
    time.sleep(1)

    while True:

        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, *screen_size), outline=0, fill=0)

        draw.text((x_offset, y_offset), text,  font=font, fill=255)

        # Display image.
        disp.image(image)
        disp.display()
        time.sleep(0.02)

        x_offset -= 1
        if x_offset < -max_offset:
            x_offset = 0


if __name__ == '__main__':

    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    main()