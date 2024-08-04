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

while True:
    print("Pot A", potA.value, "Pot B", potB.value)
    OSC.send(target, "/rnbo/inst/0/params/gain/normalized", potA.value)
    OSC.send(target, "/rnbo/inst/0/params/gain/normalized", potB)