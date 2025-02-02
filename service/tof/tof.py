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
    vl53.set_ranging_frequency_hz(15)
    vl53.set_integration_time_ms(50)
    vl53.start_ranging()

    while True:
        if vl53.data_ready():
            data = vl53.get_data()
            # 2d array of distance
            distance = numpy.flipud(numpy.array(data.distance_mm).reshape((-1, )))
            # 2d array of reflectance
            reflectance = numpy.flipud(numpy.array(data.reflectance).reshape((-1, )))
            # 2d array of good ranging data
            # status = numpy.isin(numpy.flipud(numpy.array(data.target_status).reshape((-1, ))), (STATUS_RANGE_VALID, STATUS_RANGE_VALID_LARGE_PULSE))

            distance = distance[-16:]
            reflectance = reflectance[-16:]
            mask = (reflectance > 0)
            
            distance_masked = distance * mask + 2000.0 * numpy.invert(mask)

            min_distance = distance_masked.min()

            dist0 = (distance_masked[10] + distance_masked[11] + distance_masked[14] + distance_masked[15]) / 4.0
            dist1 = (distance_masked[8] + distance_masked[9] + distance_masked[12] + distance_masked[13]) / 4.0
            dist2 = (distance_masked[0] + distance_masked[1] + distance_masked[4] + distance_masked[5]) / 4.0
            dist3 = (distance_masked[2] + distance_masked[3] + distance_masked[6] + distance_masked[7]) / 4.0

            if not args.service:
                print(f'{min_distance=}')

            OSC.send(target, "/rnbo/inst/0/params/ToF_min/normalized", min_distance/2000.0)

            OSC.send(target, "/rnbo/inst/0/params/ToF_0/normalized", dist0/2000.0)
            OSC.send(target, "/rnbo/inst/0/params/ToF_1/normalized", dist1/2000.0)
            OSC.send(target, "/rnbo/inst/0/params/ToF_2/normalized", dist2/2000.0)
            OSC.send(target, "/rnbo/inst/0/params/ToF_3/normalized", dist3/2000.0)

            # for i in range(16):
            #     OSC.send(target, f"/rnbo/inst/0/params/ToF_{i}/normalized", distance_masked[i]/2000.0)

            
        else:
            if not args.service:
                print("No data ready")
    
        time.sleep(0.15)


if __name__ == '__main__':

    # Change the current working directory to the script directory
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--service', action='store_true')
    args = parser.parse_args()

    main(args)