import sys, os, time, logging, argparse

import asyncio
import threading
import numpy
import numpy.ma as ma

import pyliblo3 as OSC

import vlc
import time


def main(args):

    # send all messages to port 1234 on the local machine
    try:
        target = OSC.Address("192.168.10.13", 1234)
    except OSC.AddressError as err:
        print(err)    
        sys.exit()

    # start the transport via OSC
    OSC.send(target, "/rnbo/jack/transport/rolling", 1)


    while True:
        for i in range(100):

            if i == 30:
                OSC.send(target, "/rnbo/inst/0/params/sound_on/normalized", 1)
                print(f'send start')

            if i == 99:
                OSC.send(target, "/rnbo/inst/0/params/sound_on/normalized", 0)
                print(f'send stop')

            print(f'send {i}')
            time.sleep(0.1)


if __name__ == '__main__':

    # Change the current working directory to the script directory
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--service', action='store_true')
    args = parser.parse_args()

    main(args)