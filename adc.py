import spidev
import liblo as OSC
import time, sys

 
class McpEx:
    def __init__(self, bus=0, device=0):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.mode = 3
        self.spi.max_speed_hz = 1000000
 
    def analog_read(self, channel):
        # 매개변수 (시작비트, 채널, 자릿수 맞춤 위치), 리턴값 : 아날로그 값
        r = self.spi.xfer2([1, (0x08+channel)<<4, 0])  # Pi -> MCP, MCP -> Pi
        adc_out = ((r[1]&0x03)<<8) + r[2] # 수신 데이터 결합
        return adc_out


def main():
     
    mcp = McpEx()

    # OSC 통신 초기화
    port = 1234

    try:
        osc_target = OSC.Address("localhost", port)
        OSC.send(osc_target, "/rnbo/jack/transport/rolling", 1)
    except OSC.AddressError as err:
        print(err)
        sys.exit()


    # ADC 값 읽고 OSC 메시지 전송 반복
    while True:
        adc = mcp.analog_read(0)
        voltage = adc*5/1023
        print("ADC = %s(%d) Voltage = %.3fV" % (hex(adc), adc, voltage))
        OSC.send(osc_target, "/rnbo/inst/0/params/oscillator_frequency/normalized", voltage)
    
        time.sleep(0.5)


if __name__ == '__main__':
    main()