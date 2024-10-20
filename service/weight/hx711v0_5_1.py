import RPi.GPIO as GPIO
import time
import threading
import numpy as np

class HX711:

    def __init__(self, douts, pd_sck):

        self.PD_SCK = pd_sck
        self.DOUT_list = douts
        self.channels = len(douts)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PD_SCK, GPIO.OUT)
        for DOUT in self.DOUT_list:
            GPIO.setup(DOUT, GPIO.IN)

        # The value returned by the hx711 that corresponds to your reference
        # unit AFTER dividing by the SCALE.
        self.REFERENCE_UNIT_A = 114
        self.OFFSET_A = np.zeros((self.channels, 1))

        self.old_weights = np.zeros(self.channels)

        # Think about whether this is necessary.
        time.sleep(1)


    def isReady(self):
        # check all the DOUT pins to see if any of them are high.
        for DOUT in self.DOUT_list:
            if GPIO.input(DOUT) == GPIO.HIGH:
                return False
        return True

    def readNextBit(self):
       # Clock HX711 Digital Serial Clock (PD_SCK).  DOUT will be
       # ready 1us after PD_SCK rising edge, so we sample after
       # lowering PD_SCL, when we know DOUT will be stable.
       GPIO.output(self.PD_SCK, True)
       GPIO.output(self.PD_SCK, False)
       bitValues = [int(GPIO.input(DOUT)) for DOUT in self.DOUT_list]
       bitValues = np.array(bitValues)
       return np.expand_dims(bitValues, axis=1)

    def readNextByte(self):
        byteValues = np.zeros((self.channels, 1), dtype=int)

        # Read bits and build the byte from top, or bottom, depending
        # on whether we are in MSB or LSB bit mode.
        for x in range(8):
            byteValues <<= 1
            byteValues |= self.readNextBit()

        # Return the packed byte.
        return byteValues

    def readRawBytes(self, blockUntilReady=True):
        
        # Wait until HX711 is ready for us to read a sample.
        while self.isReady() is not True:
           pass

        # Read three bytes of data from the HX711.
        firstBytes  = self.readNextByte()
        secondBytes = self.readNextByte()
        thirdBytes  = self.readNextByte()

        # HX711 Channel and gain factor are set by number of bits read
        # after 24 data bits.
        self.readNextBit()         

        # Most significant Byte first.
        return np.concatenate([firstBytes, secondBytes, thirdBytes], axis=1)
        
    def convertFromTwosComplement24bit(self, inputValue):
        return -(inputValue & 0x800000) + (inputValue & 0x7fffff)

    def rawBytesToLong(self, rawBytes):
        # Join the raw bytes into a single 24bit 2s complement value.
        twosComplementValue = ((rawBytes[:, 0:1] << 16) |
                               (rawBytes[:, 1:2] << 8)  |
                               rawBytes[:, 2:3])
        
        # Convert from 24bit twos-complement to a signed value.
        signed_int_value = self.convertFromTwosComplement24bit(twosComplementValue)

        # Return the sample value we've read from the HX711.
        return signed_int_value

    def getWeight(self):
        rawBytes = self.readRawBytes()
        longWithOffset = self.rawBytesToLong(rawBytes) - self.OFFSET_A
        return longWithOffset[:,0] / self.REFERENCE_UNIT_A

    def getWeightFiltered(self):
        new_weights = self.getWeight()
        self.old_weights = self.old_weights * 0.5 + new_weights * 0.5
        return self.old_weights


    def autosetOffset(self):        
        newOffsetValue = np.zeros((self.channels, 1))
        for i in range(10):
            rawBytes = self.readRawBytes()
            newOffsetValue += self.rawBytesToLong(rawBytes)
        newOffsetValue /= 10
        
        self.OFFSET_A = newOffsetValue

    
# EOF - hx711.py