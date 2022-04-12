# Preamble
This document serves as note for the process of researching and accumulating resources to properly implement PN532 into the project. There will not be a focused, singular subject, but a plethora of related facts, articles and videos that was used, or found helpful when learning about this subject. There are also short description of various terms (RFID, NFC) and their underlying principles of operation if I can understand it.

This document should be used like a FAQ, and not reader through sequentially. In case that you want to learn more, then I suggest going through the reference in this order: 
- For general video: [V1], [V2], [V6], [V7], [V5] or [V4].
- For general article: [V3]
- For implementation: [I1], [I2], [I4]
Everything else should serve as reference or supplementary resources.

# Difficulty with references
It seems that the current authority for NFC standards is the [NFC Forum](https://nfc-forum.org/). Their standards require payment to access (same with any ISO standards). This makes finding authoritative info very difficult and any info found on the net is either unreliable or does not have enough detail.

Any resources below is presented as is without any guaranteer from the publisher to be accurate or up to date (as far as I know). A good example of this is [T3], which seems to link to various documentation that is no longer accessible (requires payment or taken down).

See [V7] for the the current (newest that I can find) general info on standard.

# Reference sources:
#### General Video (Youtube)
- [V1]: [What is RFID? How RFID works? RFID Explained in Detail](https://youtu.be/Ukfpq71BoMo)
- [V2]: [NFC Explained: What is NFC? How NFC Works? Applications of NFC](https://youtu.be/eWPtt2hLnJk)
- [V3]: [What is the Difference between RFID and NFC?](https://youtu.be/cJXvT2THdDE)<br>
  Note that this video is heavily aimed toward the use of RFID and NFC within supply chain, retail and "product lifecycle" (not technical). Good mentions of practical use cases.
- [V4]: [How safe is contactless payment? || How does RFID & NFC work? || EB#40](https://youtu.be/mzPb9QLJu8k)
- [V5]: [EEVblog #889 - Credit Card RFID/NFC Theft Protection Tested](https://youtu.be/kp63MZ6RudE)<br>
  Showcase cleanly the modulation of the carrier signal on an oscilloscope with a magnetic probe. Very interesting.
- [V6]: [Fundamentals of NFC/RFID Communications](https://youtu.be/BkddfktQdbc)<br>
  Very good video with valuable info and classification. Though the image quality is low.
- [V7]: [ST25 NFC training v2.1: 1.3 NFC Basics](https://youtu.be/4WcbjTzXN4M)<br>
  Similar to [V6] (but with better image quality). Goes into more depth on NFC standards.
  
#### General Articles
- [T1]: [Radio-frequency identification (Wikipedia)](https://en.wikipedia.org/wiki/Radio-frequency_identification)
- [T2]: [Near-field_communication (Wikipedia)](https://en.wikipedia.org/wiki/Near-field_communication)
- [T3]: [Adafruit PN532 RFID/NFC Breakout and Shield](https://learn.adafruit.com/adafruit-pn532-rfid-nfc)<br>
  Don't let the name fool you (into thinking that this is a guide for JUST the breakout board). This is a very good guide-tutorial styled list of posts that mention a lot of important facets (library for RaspPi, card and tag detail, NDEF format, libNFC in linux). ***The info contained is very old*** (judging by post day, which is 2012) but still good as a reference.
- [T4]: [RFID Selection Guide](https://cdn-shop.adafruit.com/datasheets/rfid+guide.pdf)<br>
  The list of NFC devices and ICs is very infomative. MF1 S50 is MIFARE Classic 1K (nobody mentions this).

#### Datasheet
- [D1]: [MF1 IC S50 - Functional specification](https://cdn-shop.adafruit.com/datasheets/S50.pdf)<br>
  Datasheet for the S50, which can not be found on the NXP site anymore (probably due to the Crypto-1 encryption on these card being cracked - see [this](https://en.wikipedia.org/wiki/Crypto-1) and [this](https://en.wikipedia.org/wiki/MIFARE#MIFARE_Classic))
- [D2]: [MF1S70YYX_V1 - MIFARE Classic EV1 4K - Mainstream contactless smart card IC for fast and easy solution development](https://www.nxp.com/docs/en/data-sheet/MF1S70YYX_V1.pdf)<br>
  A improvde version of the S50 card. This datasheet have more info on various Classic MIFARE commands and (some) corresponding ISO14443 command. I can't buy and use this card but the related info is useful.
- [D3]: [PN532/C1 - Near Field Communication (NFC) controller](https://www.nxp.com/docs/en/nxp/data-sheets/PN532_C1.pdf)

#### Implementation
- [I1]: [Raspberry gPIo](https://learn.sparkfun.com/tutorials/raspberry-gpio)<br>
  Good info on setting up and controlling GPIO in RaspPi. Weirdly enough, the official doc doesn't even talk about this.
- [I2]: [Raspberry Pi SPI and I2C Tutorial](https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial)<br>
  Again, good info on working with I2C and SPI on RaspPi.
- [I3]: [PN532 NFC RFID Module — A Quick Introduction](https://www.electroschematics.com/nfc-rfid-module-pn532/)<br>
  For connecting the PN532 breakout board into the system and use it (module, wiring, library, test code) with Arduino.
- [I4]: [PN532 NFC HAT](https://www.waveshare.com/wiki/PN532_NFC_HAT)<br>
  Has the library for RaspPi, enough said.

---

# RFID
#### Description
Stands for ***Radio Frequency IDentification***. RFID refers to any system that uses radio wave to read and capture info stored on a tag (which can be attached to various object). This definition spans many RF tech. [V6]

A RFID system is comprised of RFID reader(s) and a RFID tag(s) (which can be active, passive or semi-passive). The passive type is the most common due to their price and compactness (not requiring power). When triggered by a nearby RFID reader, the tag transmits data back to the reader.

When establishing a connection, at least one of the device have to be an active (meaning that it can provide power to maintain the connection). A passive device don't need a external power source to funciton (such as card).

RFID operates on various freq ranges with variation between countries, refer to [V1], [V6], [V7], [T1].

#### Priciples of operation
This section is taken from [V1]. Though [V6] and [V7] also offer explanation.

Base on the freq, RFID ultilizes 2 principles:
- Inductive coupling (Near Field Coupling)
- EM coupling (Far Field Coupling)

###### Near Field Coupling
The reader sent RF wave at some freq, which serves as: power source for the tags; synchronization signal; carrier freq for the return data from tag.

The tag and the reader is assumed to be close to each others. Such that their coil is inductively coupled.

The coil of the tag, when receiving the carrier signal, induces a voltage which will serve as the signal source for the tag to power on. Now if we attachs a load across this coil, a current will flow. By controlling the load impedance, we can control the current that flow through the reader coil. This is called load modulation and it is used to sent data from the tag back to the reader.

Note that the tag can not send any data if there is no carrier wave. And the tag don't need dedicated power source.

###### Far Field Coupling
The distance between the tag and the reader now is quite far, so any coupling between coil is infeasible for data and power transfer.

The tag will sent back a weak signal call a backscatter signal. Its intensity is dependent on load matching.

(things start to get way over my head at this point)

---

# NFC
#### Description
Stands for ***Near Field Communication***, a short distance wireless communication tech. NFC can be seen as a subset of the large RFID tech. NFC is defined by specific standards, focused on system where confidentiality and data protection is important (payment and access control).

It uses 13.56MHz carrier freq and provided more specialized functionality over RFID. The range is limited, but this makes NFC more secure.

#### Modes of operation
The content of this section is mentioned in [V1], [V7], [T1], [T3].

There are 3 modes of communication:
- Peer-to-Peer Mode
  Two device is active and generating signal alternatively (each device takes turn to send data by generating the signal, but not both at the same time).
  
- Reader/Writer Mode
  A device will be passive when the other is active. Power for the passive device comes from EM induction within the passive's coil. Signaling from the passive device is done by load modulation - the subcarrier freq for this is 847.5 kHz.
  
- Card Emulation Mode
  A common use case for this is with payment using phone. In this mode, the phone act as a passive device that only respond bach the required infomation to the payment terminal (not really sure if the phone is active or use load modulation).

#### Standards
There seems to be different standards for NFC, with differing coding scheme, modulation and data rates. The table is taken from [V2]

| NFC Forum Standard   | Coding          | Modulation | Rate (Kbps) |
| -------------------- | --------------- | ---------- | ----------- |
| NFC-A (ISO 14443A)   | Modified Miller | ASK 100%   | 106         |
| NFC-B (ISO 14443B)   | NRZ-L           | ASK 10%    | 106         |
| NFC-F (JIS X 6319-4) | Manchester      | ASK 10%    | 212/424     |
| NFC-V (ISO 15693)    | PPM             | ASK        | 26.48       |

More info about various standard can be found in [V6].

---

# RFID vs. NFC
NFC can be considered subset of RFID, but NFC provides enhanced and specialized functionality.

RFID works on a larger freq range while NFC only works at 13.56MHz.

RFID may employ many modulation techniques, while NFC only uses ASK.

RFID can operate over wide range of distance, while NFC only works at short range (<1m).

In short, this comparison is like asking the different between a car and a Toyota car.

---

# MIFARE Classic 1K/4K card

A old tech (datasheet going back before 2005). To know more, recommended reading is [T3] and then [D1]. Memory organization and authentication is found in the [D1] datasheet.
