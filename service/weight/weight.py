import sys, os, time, logging, argparse

import RPi.GPIO as GPIO
import liblo as OSC
from hx711v0_5_1 import HX711


def main(args):

    # send all messages to port 1234 on the local machine
    try:
        target = OSC.Address(1234)
    except OSC.AddressError as err:
        print(err)    
        sys.exit()

    # start the transport via OSC
    OSC.send(target, "/rnbo/jack/transport/rolling", 1)

    hx = HX711(douts=[5], pd_sck=6)
    hx.autosetOffset()

    while True:
        weightValues = hx.getWeightFiltered()

        print(f"weight (grams): {weightValues}")
        for i, weightValue in enumerate(weightValues):
            OSC.send(target, f"/rnbo/inst/0/params/weight{i}/normalized", weightValue)



if __name__ == '__main__':

    # Change the current working directory to the script directory
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--service', action='store_true')
    args = parser.parse_args()

    main(args)