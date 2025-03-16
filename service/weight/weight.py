import sys
import smbus
import time
import struct
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



    SLAVE_ADDRESS = 0x50
    I2C_BUS = 1

    bus = smbus.SMBus(I2C_BUS)
    i = 0

    def request_and_receive_float(address, index):
        try:
            bus.write_byte(address, index)
            time.sleep(0.05)
            data = bus.read_i2c_block_data(address, 0, 4) # float 는 4바이트
            float_value, = struct.unpack('<f', bytes(data))
            return float_value
        except Exception as e:
            print(f"Error: {e}")
            return None

    try:
        while True:
                

            weight0 = request_and_receive_float(SLAVE_ADDRESS, 0)
            weight1 = request_and_receive_float(SLAVE_ADDRESS, 1)
            weight2 = request_and_receive_float(SLAVE_ADDRESS, 2)
            weight3 = request_and_receive_float(SLAVE_ADDRESS, 3)

            # print(f"{weight0:.0f}, {weight1:.0f}, {weight2:.0f}, {weight3:.0f}")
            if not args.service:
                print(f"{weight0}")

            OSC.send(target, "/rnbo/inst/0/params/weight0/normalized", weight0)
            OSC.send(target, "/rnbo/inst/0/params/weight1/normalized", weight1)
            OSC.send(target, "/rnbo/inst/0/params/weight2/normalized", weight2)
            OSC.send(target, "/rnbo/inst/0/params/weight3/normalized", weight3)

            time.sleep(0.250/4)


    except KeyboardInterrupt:
        print("Program terminated by user.")
    finally:
        bus.close()


if __name__ == '__main__':

    # Change the current working directory to the script directory
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--service', action='store_true')
    args = parser.parse_args()

    main(args)