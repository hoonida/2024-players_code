import sys, os, time, logging, argparse
import atexit

import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import graphic


def get_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip, socket.gethostname()


def main(args):

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
    font = ImageFont.truetype('DungGeunMo.ttf', 18)
    text = f"서울특별시 영등포구 당산로 10"

    y_offset = 10
    x_offset = 0

    textline = graphic.TextLine(screen_size, text, font)


    def terminate_callback():
        draw.rectangle((0, 0, *screen_size), outline=0, fill=0)
        # draw.text((0, 0), 'BYE!',  font=font, fill=255)
        disp.image(image)
        disp.display()
    atexit.register(terminate_callback)


    ip_text, host_text = get_ip()
    draw.text((x_offset, y_offset), ip_text,  font=ImageFont.load_default(), fill=255)
    draw.text((x_offset, y_offset + 8), host_text,  font=ImageFont.load_default(), fill=255)
    disp.image(image)
    disp.display()
    time.sleep(2)

    while True:

        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, *screen_size), outline=0, fill=0)

        textline.draw(draw, x_offset, y_offset)
        textline.shift(2)

        # Display image.
        disp.image(image)
        disp.display()



if __name__ == '__main__':

    # Change the current working directory to the script directory
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--service', store=True)
    args = parser.parse_args()

    main(args)