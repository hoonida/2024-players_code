import vl53l5cx_ctypes as vl53l5cx
from vl53l5cx_ctypes import STATUS_RANGE_VALID, STATUS_RANGE_VALID_LARGE_PULSE

import numpy
import liblo as OSC
import time, sys

# gpip 3 scl
# gpio 2 sda

class ToF:

    def __init__(self, i2c_bus=1, i2c_address=0x29):
        print("Uploading firmware, please wait...")
        self.vl53 = vl53l5cx.VL53L5CX()
        print("Done!")
        self.vl53.set_resolution(8 * 8)
        # self.vl53.enable_motion_indicator(8 * 8)

        # vl53.set_integration_time_ms(50)

        # Enable motion indication at 8x8 resolution
        # self.vl53.enable_motion_indicator(8 * 8)

        # Default motion distance is quite far, set a sensible range
        # eg: 40cm to 1.4m
        # self.vl53.set_motion_distance(400, 1400)

        self.vl53.start_ranging()

    def __del__(self):
        self.tof.stop_ranging()

    def data_ready(self):
        return self.vl53.data_ready()

    def get_distance(self):

        data = self.vl53.get_data()
        # 2d array of motion data (always 4x4?)
        motion = numpy.flipud(numpy.array(data.motion_indicator.motion[0:16]).reshape((4, 4)))
        # 2d array of distance
        distance = numpy.flipud(numpy.array(data.distance_mm).reshape((8, 8)))
        # 2d array of reflectance
        reflectance = numpy.flipud(numpy.array(data.reflectance).reshape((8, 8)))
        # 2d array of good ranging data
        status = numpy.isin(numpy.flipud(numpy.array(data.target_status).reshape((8, 8))), (STATUS_RANGE_VALID, STATUS_RANGE_VALID_LARGE_PULSE))
        # print(motion, distance, reflectance, status)

        return distance, status



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
    count = 0
    while True:
        if tof.data_ready():
            data = tof.vl53.get_data()
            distance_in_mm = tof.get_distance()
            # distance_in_mm = min(distance_in_mm, 2000) / 2000
            print(f"Distance: {distance_in_mm} {count}")
            count += 1
            
            # print(f"Distance: {distance_in_mm} mm")
            # OSC.send(osc_target, "/rnbo/inst/0/params/vl53l1x_tof/normalized", distance_in_mm)
        
            time.sleep(0.5)


if __name__ == '__main__':
    main()
