import sys, os, time, logging, argparse

import asyncio
import threading
import numpy
import numpy.ma as ma

import pyliblo3 as OSC

import vlc
import time


def tof_scan(interval=0.1):

    import vl53l5cx_ctypes as vl53l5cx
    from vl53l5cx_ctypes import STATUS_RANGE_VALID, STATUS_RANGE_VALID_LARGE_PULSE

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

            yield distance_masked

        else:
            if not args.service:
                print("No data ready")
    
        time.sleep(interval)



def main(args):

    # send all messages to port 1234 on the local machine
    try:
        target = OSC.Address("192.168.10.13", 1234)
    except OSC.AddressError as err:
        print(err)    
        sys.exit()

    # start the transport via OSC
    OSC.send(target, "/rnbo/jack/transport/rolling", 1)



    # 파일 경로 및 시작, 종료 시간 설정
    video_path = "video.mov"
    start_time = 5    # 시작 시간 (초 단위)
    end_time = 10     # 종료 시간 (초 단위)

    # VLC 인스턴스 생성
    instance = vlc.Instance()
    player = instance.media_player_new()

    # 동영상 파일 로드
    media = instance.media_new(video_path)
    player.set_media(media)

    # 플레이어 시작
    player.play()
    time.sleep(0.1)  # 첫 프레임을 로드하기 위한 짧은 대기
    player.set_time(0)  # 첫 프레임 위치로 이동
    player.pause()      # 일시정지 상태 유지
    

    mode = "wait" # wait, event

    for scan in tof_scan(interval=0.1):

        if mode == 'wait':

            # time.sleep(5)
            # player.play()
            # mode = 'play'

            OSC.send(target, "/rnbo/inst/0/params/sound_on/normalized", 0)
            min_distance = scan.min()
            if not args.service:
                print(f'{min_distance=}')

            if min_distance < 200:
                player.play()
                mode = 'play'

        elif mode == 'play':

            player_time = player.get_time()
            print(f'{player_time=}')

            if 27000 <= player_time and player_time < 46000:
                OSC.send(target, "/rnbo/inst/0/params/sound_on/normalized", 1)
            else:
                OSC.send(target, "/rnbo/inst/0/params/sound_on/normalized", 0)

            if player_time > 37000:

                player.pause()      # 일시정지 상태 유지
                player.set_time(0)  # 첫 프레임 위치로 이동
                player.play()
                time.sleep(0.1)  # 첫 프레임을 로드하기 위한 짧은 대기
                player.pause()      # 일시정지 상태 유지
                mode = 'wait'
            


if __name__ == '__main__':

    # Change the current working directory to the script directory
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--service', action='store_true')
    args = parser.parse_args()

    main(args)