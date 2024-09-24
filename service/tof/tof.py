import sys, os, time, logging, argparse

import numpy
import numpy.ma as ma
import vl53l5cx_ctypes as vl53l5cx
from vl53l5cx_ctypes import STATUS_RANGE_VALID, STATUS_RANGE_VALID_LARGE_PULSE
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


    print("Uploading firmware, please wait...")
    vl53 = vl53l5cx.VL53L5CX()
    print("Done!")
    vl53.set_resolution(4 * 4)
    vl53.set_ranging_frequency_hz(30)
    vl53.set_integration_time_ms(20)
    vl53.start_ranging()

    while True:
        if vl53.data_ready():
            data = vl53.get_data()
            # 2d array of distance
            distance = numpy.flipud(numpy.array(data.distance_mm).reshape((-1, )))
            # 2d array of reflectance
            reflectance = numpy.flipud(numpy.array(data.reflectance).reshape((-1, )))
            # 2d array of good ranging data
            status = numpy.isin(numpy.flipud(numpy.array(data.target_status).reshape((-1, ))), (STATUS_RANGE_VALID, STATUS_RANGE_VALID_LARGE_PULSE))

            distance = distance[-16:]
            reflectance = reflectance[-16:]
            mask = (reflectance > 0)
            
            distance_masked = distance * mask + 1000.0 * numpy.invert(mask)

            min_distance = distance_masked.min()
            # print(f'{min_distance=}')
            OSC.send(target, "/rnbo/inst/0/params/ToF_num/normalized", min_distance/1000.0)
    
        time.sleep(0.03)


if __name__ == '__main__':

    # Change the current working directory to the script directory
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--service', action='store_true')
    args = parser.parse_args()

    main(args)