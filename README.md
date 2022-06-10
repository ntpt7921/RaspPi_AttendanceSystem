# RaspPi_AttendanceSystem

## Requirement

This project will utilize a Raspberry Pi 4 (2GB RAM) to implement a attendence system with facial recognition and RFID card reader. It will have the ability to access networked database of authorized personels and display the result.

The system needs to have the ability to update and get new data from and to a database (online or local, preferably online). The ability to deny authorization if target is detected as a display device or a picture is not implemented.

The system ***may*** have a monitor, it will display a UI to help users with alignment of their face. The display will also facilitate directing user to do certain action (to help prevent using a picture to fool the system).

## Structure

All the code in this project will be written in Python, with Python's library and packages.

Project organization is as follow
```
.
├── database             # the database folder
├── face_recognition     # the face recognition folder
├── nfc                  # the nfc card reader folder
├── LICENSE
└── README.md
```

Each folder represents a big segment of the project. Every file or documentation related to a particular segment should be put info their corresponding folder.

## Python dependencies

Library used in this project beside built-in one are:

- OpenCV (`cv2`)
- Waveshare's PN532 NFC HAT (most of `database` folder)

## Hardware

- Raspberry Pi 4 (2GB RAM)
- PN532 module ([buy here](https://hshop.vn/products/mach-rfid-nfc-13-56mhz-pn532))
- Camera Raspberry Pi V1 OV5647 ([buy here](https://hshop.vn/products/camera-raspberry-pi))
- MIFARE Classic 1K ([buy here](https://hshop.vn/products/the-nhua-nfc-philips-s50rfid-13-56-mhz))
