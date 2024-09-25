import sys, os, time, logging, argparse

import liblo as OSC



def main(args):

    try:
        server = OSC.Server(1234)
    except OSC.ServerError as err:
        print(err)
        print("Please stop rnbo services before running this script")
        sys.exit()


    if args.path is None:
        # register a fallback for unhandled messages

        def fallback(path, args, types, src):
            print(f"{path}")
            for a, t in zip(args, types):
                print(f"  [{t}] {a}")

        server.add_method(None, None, fallback)

    else:
        # register method taking a float

        def message_callback(path, args):
            print(f'{args[0]}')

        server.add_method(args.path, 'f', message_callback)


    # loop and dispatch messages every 100ms
    while True:
        server.recv(100)



if __name__ == '__main__':

    # Change the current working directory to the script directory
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, required=False, default=None)
    args = parser.parse_args()

    main(args)