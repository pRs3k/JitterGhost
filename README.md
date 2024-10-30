# JitterGhost
This repository contains instructions and code for building your own shaking ghost Halloween decoration, like the ones from the 90s, only yours will be fully customizable! You pick the sounds, light colors, shake intensity, motion sensitivity, duration, and sleep time! You will also have the opportunity to exercise your artistic abilities in decorating the ghost face however you like.

## Features
- Bring your own sound clips (HD audio supported)
- Fully customizable LED color(s)
- Adjustable shake intensity
- Adjustable motion sensitivity
- Adjustable on/sleep durations
- Design your own ghost face
- 3D printable enclosure or get creative

## Parts List
- Raspberry Pi Pico H RP2040 Microcontroller ($9 pre-soldered for breadboards)
- CQRobot 3W 4Ohm 4O3W-JST-PH2.0 Speakers ($8) - Only need 1 of the 2 speakers
- EUDAX 6 Set 3-12V DC Motors Kit & Battery Packs ($12) - Only need 1 of the 6 motors and battery packs
- DFPlayer Mini ($10)
- Micro SD Card ($5 or less for 1GB which is more than enough)
- HiLetgo 3pcs HC-SR501 PIR Infrared Sensors ($8.50) - Only need 1 of the 3 sensors
- KOOBOOK 5Pcs DRV8833 Motor Drive Module ($8) - Only need 1 of the 5 motor drivers
- White square cloth
- 470uF 10V Capacitors (maybe optional)
- Breadboard (optional)
- Jumper cables
- 0.1uF Capacitors (probably optional)
- Soldering iron
- 3D printer and filament (optional)
- AA batteries (2 count)
- USB power bank (maybe, TBD)
<br>
Total cost: ~$60 but you'll almost end up with enough extra parts to build 3 whole ghosts, assuming you already have a soldering iron, wires, capacitors, and cloth. Also you can opt for a 4 pack of unsoldered RPi Pico for $20.

## Setup
To install the micropython_dfplayer python module, head to https://github.com/redoxcode/micropython-dfplayer/blob/main/src/dfplayer/__init__.py and save the code on your Pico as `micropython_dfplayer.py`<br>

### Cable Connections
 - Pico(GP0) to DFPlayer(RX)
 - Pico(GP1) to DFPlayer(TX)
 - Pico(GND) to DFPlayer(GND)
 - Pico(3V3 OUT) to DFPlayer(VCC)
 - Pico(SPK1) to Speaker(Red)
 - Pico(SPK2) to Speaker(Blk)
 - DRV8833(GND) to Pico(GND)
 - DRV8833(GND) to Battery(BLK)
 - DRV8833(VCC) to Battery(Red)
 - DRV8833(IN2) to Pico(GP14)
 - DRV8833(IN1) to Pico(GP15)
 - DRV8833(OUT1) to Motor(either terminal)
 - DRV8833(OUT2) to Motor(other terminal)
 - PIR(GND) to Pico(GND)
 - PIR(High/Low Output) to Pico(GP28)
 - PIR(+Power) to Pico(VBUS)

## Future Enhancements


## Comments
