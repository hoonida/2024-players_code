import VL53L1X
import liblo as OSC
import time, sys


class ToF:

    def __init__(self, i2c_bus=1, i2c_address=0x29):
        # Open and start the VL53L1X sensor.
        # If you've previously used change-address.py then you
        # should use the new i2c address here.
        # If you're using a software i2c bus (ie: HyperPixel4) then
        # you should `ls /dev/i2c-*` and use the relevant bus number.
        self.tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
        self.tof.open()

        # Optionally set an explicit timing budget
        # These values are measurement time in microseconds,
        # and inter-measurement time in milliseconds.
        # If you uncomment the line below to set a budget you
        # should use `tof.start_ranging(0)`
        # tof.set_timing(66000, 70)

        self.tof.start_ranging(1)  # Start ranging
                            # 0 = Unchanged
                            # 1 = Short Range (136cm)
                            # 2 = Medium Range (290cm)
                            # 3 = Long Range (360cm)

    def __del__(self):
        self.tof.stop_ranging()

    def get_distance(self):
        # Grab the range in mm, this function will block until
        # a reading is returned.
        distance_in_mm = self.tof.get_distance()
        return distance_in_mm



def main():
     
    tof = ToF()

    # OSC 통신 초기화
    port = 1234

    try:
        osc_target = OSC.Address("localhost", port)
        OSC.send(osc_target, "/rnbo/jack/transport/rolling", 1)
    except OSC.AddressError as err:
        print(err)
        sys.exit()


    # ToF 값 읽고 OSC 메시지 전송 반복
    while True:
        distance_in_mm = tof.get_distance()
        distance_in_mm = min(distance_in_mm, 2000) / 2000
        
        print(f"Distance: {distance_in_mm} mm")
        OSC.send(osc_target, "/rnbo/inst/0/params/vl53l1x_tof/normalized", distance_in_mm)
    
        time.sleep(0.5)


if __name__ == '__main__':
    main()