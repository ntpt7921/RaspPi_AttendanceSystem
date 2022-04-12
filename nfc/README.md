# PN532 library for the Raspberry Pi

## Introduction

This is the library for the PN532 module used in the project. It is taken from the Waveshare's [PN532 NFC HAT library](https://www.waveshare.com/wiki/PN532_NFC_HAT).

The example code `example_*.py` shows how to use the library.

## Basic usage

All code snippets below must be included to correctly use PN532 for reading MIFARE Classic 1K/4K card.

### Importing library

This library relied on RPi.GPIO, to import the library
``` python3
import RPi.GPIO as GPIO

import pn532.pn532 as nfc
from pn532 import *
```

### Handler declaration

The PN532 module can be used with UART, I2C and SPI. We will use I2C in the project. To declare the handler
``` python3
pn532 = PN532_I2C(debug=False, reset=20, req=16)
```
The `reset` and `req` argument contains the pin number (BCM style) for the RSTPD_N and INT0 for the PN532 (see the datasheet). This is used for resetting the chip and packet availability signalling.

### Configuration

``` python3
# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()
```

### Detect, authentication, read and write

To detect the card
``` python3
uid = pn532.read_passive_target(timeout=0.5)
```
`uid` will have value `None` if card is not detected for and waiting period of 0.5s (`timeout=0.5`), else it will have the UID of the card.



To access the EEPROM on the card, first we must authenticate.
``` python3
pn532.mifare_classic_authenticate_block(
        uid, block_number=block_number, key_number=nfc.MIFARE_CMD_AUTH_A, key=key_a)
```
`uid` is the UID we have read when detecting. The `block_number` is a integer (start from 0) that represent a block of memory. `key_number` is the secret key used to authenticate (think of a password), each sector (contains many block) have two of such key (A and B). More info on memory organization, see the MF1 S50 datasheet (link contained in [the note file](NOTE.md)).



To read and write into a authenticated block
``` python3
pn532.mifare_classic_write_block(block_number, data)
pn532.mifare_classic_read_block(block_number)
```
`data` is a 16 bytes list. The read operation will also return a 16 bytes list.


## More information
See [the note file](NOTE.md) for more information and resources.

