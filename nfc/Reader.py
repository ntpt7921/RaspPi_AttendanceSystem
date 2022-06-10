import RPi.GPIO as GPIO

from .pn532 import pn532 as nfc
from .pn532 import *

class Reader:
    pn532 = None # card reader

    INTERFACE_SPI = 'spi'
    INTERFACE_I2C = 'i2c'
    INTERFACE_UART = 'uart'
    KEY_TYPE_DEFAULT = 'A'
    KEY_A_VALUE_DEFAULT = b'\xFF\xFF\xFF\xFF\xFF\xFF'

    def __init__(self, interface):
        if (interface == INTERFACE_SPI):
            self.pn532 = PN532_SPI(debug=False, reset=20, cs=4)
        elif (interface == INTERFACE_I2C):
            self.pn532 = PN532_I2C(debug=False, reset=20, req=16)
        elif (inteface = INTERFACE_UART):
            self.pn532 = pn532 = PN532_UART(debug=False, reset=20)
        else
            raise Exception("Unknown interface type: " + interface)

        ic, ver, rev, support = pn532.get_firmware_version()
        print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
        self.pn532.SAM_configuration()

    def waitForCard(self, timeoutValue = 0.5):
        print('Waiting for RFID/NFC card')
        while True:
            uid = self.pn532.read_passive_target(timeout=timeoutValue)
            print('.', end="")
            if uid is not None:
                break
        print('Found card with UID:', [hex(i) for i in uid])
        return uid

    def readCard(self, uid, blockNum, keyType = KEY_TYPE_DEFAULT, keyValue = KEY_A_VALUE_DEFAULT):
        self.authenticateCard(uid, blockNum, keyType, keyValue)
        return self.readBlock(blockNum)

    def writeCard(self, uid, blockNum, content, keyType = KEY_TYPE_DEFAULT, keyValue = KEY_A_VALUE_DEFAULe):
        self.authenticateCard(uid, blockNum, keyType, keyValue)
        return self.writeBlock(blockNum, content)

    def readBlock(self, blockNum):
        return self.pn532.mifare_classic_read_block(blockNum)

    def writeBlock(self, blockNum, content):
        self.mifare_classic_write_block(blockNum, content)
        if (content = self.readBlock(blockNum)):
            return True
        else:
            return False

    def cleanup():
        GPIO.cleanup()
