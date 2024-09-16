import RPi.GPIO as GPIO
import time
import threading

class HX711:

    def __init__(self, dout, pd_sck):

        self.PD_SCK = pd_sck
        self.DOUT = dout

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PD_SCK, GPIO.OUT)
        GPIO.setup(self.DOUT, GPIO.IN)

        # The value returned by the hx711 that corresponds to your reference
        # unit AFTER dividing by the SCALE.
        self.REFERENCE_UNIT_A = 114
        self.OFFSET_A = 1

        # Think about whether this is necessary.
        time.sleep(1)


    def isReady(self):
        return GPIO.input(self.DOUT) == GPIO.LOW

    def readNextBit(self):
       # Clock HX711 Digital Serial Clock (PD_SCK).  DOUT will be
       # ready 1us after PD_SCK rising edge, so we sample after
       # lowering PD_SCL, when we know DOUT will be stable.
       GPIO.output(self.PD_SCK, True)
       GPIO.output(self.PD_SCK, False)
       bitValue = GPIO.input(self.DOUT)

       # Convert Boolean to int and return it.
       return int(bitValue)

    def readNextByte(self):
       byteValue = 0

       # Read bits and build the byte from top, or bottom, depending
       # on whether we are in MSB or LSB bit mode.
       for x in range(8):
            # Most significant Byte first.
            byteValue <<= 1
            byteValue |= self.readNextBit()

       # Return the packed byte.
       return byteValue 

    def readRawBytes(self, blockUntilReady=True):
        
        # Wait until HX711 is ready for us to read a sample.
        while self.isReady() is not True:
           pass

        # Read three bytes of data from the HX711.
        firstByte  = self.readNextByte()
        secondByte = self.readNextByte()
        thirdByte  = self.readNextByte()

        # HX711 Channel and gain factor are set by number of bits read
        # after 24 data bits.
        self.readNextBit()         

        # Most significant Byte first.
        return [firstByte, secondByte, thirdByte]
    
    def convertFromTwosComplement24bit(self, inputValue):
        return -(inputValue & 0x800000) + (inputValue & 0x7fffff)

    def rawBytesToLong(self, rawBytes=None):
        
        if rawBytes is None:
            return None

        # Join the raw bytes into a single 24bit 2s complement value.
        twosComplementValue = ((rawBytes[0] << 16) |
                               (rawBytes[1] << 8)  |
                               rawBytes[2])
        
        # Convert from 24bit twos-complement to a signed value.
        signed_int_value = self.convertFromTwosComplement24bit(twosComplementValue)

        # Return the sample value we've read from the HX711.
        return int(signed_int_value)

    def getWeight(self, channel='A'):
        rawBytes = self.readRawBytes()
        longWithOffset = self.rawBytesToLong(rawBytes) - self.OFFSET_A
        return longWithOffset / self.REFERENCE_UNIT_A

    def autosetOffset(self, channel='A'):
        
        newOffsetValue = 0
        for i in range(10):
            rawBytes = self.readRawBytes()
            newOffsetValue += self.rawBytesToLong(rawBytes)
        newOffsetValue /= 10
        
        self.OFFSET_A = newOffsetValue

    
# EOF - hx711.py