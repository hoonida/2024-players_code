import time
import sys
import RPi.GPIO as GPIO
import liblo as OSC
from hx711v0_5_1 import HX711


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
    try:
        weightValues = hx.getWeight()

        print(f"weight (grams): {weightValues}")
        for i, weightValue in enumerate(weightValues):
            OSC.send(target, f"/rnbo/inst/0/params/weight{i}/normalized", weightValue)
        
            
    except (KeyboardInterrupt, SystemExit):
        GPIO.cleanup()
        print("[INFO] 'KeyboardInterrupt Exception' detected. Cleaning and exiting...")
        sys.exit()
        