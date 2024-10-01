import sys, os, time, logging, argparse
import atexit

import liblo as OSC
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import graphic


address = {
    1 : "10, Dangsan-ro, Yeongdeungpo-gu",
    2 : "40, Sejong-daero, Jung-gu",
    3 : "273, Ttukseom-ro, Seongdong-gu",
    4 : "281, Eulji-ro, Jung-gu",
}

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
    text = ''

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

    try:
        server = OSC.Server(4321)
    except OSC.ServerError as err:
        print(err)
        print("Please stop rnbo services before running this script")
        sys.exit()

    def update_transport_state(path, args):
        i = args[0]
        global transport_running
        transport_running = bool(i)

    def message_callback(path, args):
        index = int(args[0])
        text = address[index]
        print(f'{index=}, {text=}')
        textline = graphic.TextLine(screen_size, text, font)

    def fallback(path, args, types, src):
        pass
        # print("got unknown message '%s' from '%s'" % (path, src.url))
        # print("don't panic - probably just the runner echoing back your changes :)")
        # for a, t in zip(args, types):
        #     print("argument of type '%s': %s" % (t, a))

    # register callback methods for server routes
    server.add_method("/rnbo/jack/transport/rolling", None, update_transport_state)
    server.add_method("/rnbo/inst/0/messages/out/oled_step", 'f', message_callback)

    # Finally add fallback method for unhandled OSC addrs
    server.add_method(None, None, fallback)




    while True:

        server.recv(100)

        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, *screen_size), outline=0, fill=0)

        textline.draw(draw, x_offset, y_offset)
        textline.shift(4)

        # Display image.
        disp.image(image)
        disp.display()



if __name__ == '__main__':

    # Change the current working directory to the script directory
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--service', action='store_true')
    args = parser.parse_args()

    main(args)