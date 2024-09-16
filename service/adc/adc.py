from gpiozero import MCP3008
import liblo as OSC
import sys

# send all messages to port 1234 on the local machine
try:
    target = OSC.Address(1234)
except OSC.AddressError as err:
    print(err)    
    sys.exit()

# start the transport via OSC
OSC.send(target, "/rnbo/jack/transport/rolling", 1)

# read from last two channels
potA = MCP3008(channel=6)
potB = MCP3008(channel=7)

potA_filtered = 0.0
potB_filtered = 0.0

while True:

    potA_filtered = potA_filtered * 0.99 + potA.value * 0.01
    potB_filtered = potB_filtered * 0.99 + potB.value * 0.01

    print("Pot A", potA_filtered, "Pot B", potB_filtered)
    OSC.send(target, "/rnbo/inst/0/params/gain/normalized", potA_filtered)
    OSC.send(target, "/rnbo/inst/0/params/gain2/normalized", potB_filtered)
