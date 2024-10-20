import sys, os, time, logging, argparse

from gpiozero import MCP3008
import liblo as OSC



def main(args):

    # send all messages to port 1234 on the local machine
    try:
        target = OSC.Address(1234)
    except OSC.AddressError as err:
        print(err)    
        sys.exit()

    # start the transport via OSC
    OSC.send(target, "/rnbo/jack/transport/rolling", 1)

    # read from last two channels
    potA = MCP3008(channel=6)   #6 or 0
    potB = MCP3008(channel=7)   #7 or 1

    potA_filtered = 0.0
    potB_filtered = 0.0

    while True:

        potA_filtered = potA_filtered * 0.85 + potA.value * 0.15
        potB_filtered = potB_filtered * 0.85 + potB.value * 0.15

        # print("Pot A", potA_filtered, "Pot B", potB_filtered)
        OSC.send(target, "/rnbo/inst/0/params/gain/normalized", 1 - potA_filtered)
        OSC.send(target, "/rnbo/inst/0/params/gain2/normalized", 1 - potB_filtered)

        time.sleep(0.06)


if __name__ == '__main__':

    # Change the current working directory to the script directory
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--service', action='store_true')
    args = parser.parse_args()

    main(args)