# PN532 library for the Raspberry Pi

## Introduction

This is the library for the PN532 module used in the project. It is taken from the Waveshare's [PN532 NFC HAT library](https://www.waveshare.com/wiki/PN532_NFC_HAT).

The example code `example_*.py` shows how to use the library without wrapper.

## Basic usage

All code snippets below must be included to correctly use PN532 for reading MIFARE Classic 1K/4K card.

### Importing library

This library have a wrapper class named Reader (in file `Reader.py`) to provide easy to use function. The whole library is written as a Python package and can be imported from the project root as

```python
import nfc
```

### Card reader initialization

A card reader instance can be initialized by

```python
cardReader = nfc.reader('i2c') # use this for i2c interface to RaspPi
cardReader = nfc.reader('spi') # use this for spi interface to RaspPi
cardReader = nfc.reader('uart') # use this for uart interface to RaspPi
```

### Read and write to card

To write to a card, we must have its UID. We retrieve such UID by waiting for a card to come into close proximity to the reader. Then by using the UID as identifier, read and write operation can be performed with appropiate key type and value for associated block.

```python
cardUID = cardReader.waitForCard() # this will block until a card is detected
blockContent = cardReader.readCard(cardUID, blockNum)
success = cardReader.writeCard(cardUID, blockNum, content)
# blockNum is the block number
# content is value to be written to the specified block, is a 16 byte byte array
# blockContent is similar to content, but is the value read from block
# success denotes that writting to card successfully complete
```

###  Terminating the reader

This library use the RaspPi GPIO library. The GPIO needs to be cleaned up after use.

```python
cardReader.cleanup()
```

After calling `cleanup()`, it is safe to terminate to program.

## More information
See [the note file](NOTE.md) for more information and resources.

