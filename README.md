# Pwnagotchi-build

This is a Raspberry Pi based Pwnagotchi: a Raspberry Pi using bettercap to passively listen for WPA/WPA2 handshakes. It is important to mention that the pwnagotchi also has feelings! It will get bored or even angry at you when you do not feed it WPA/WPA2 handshakes and it will be amused when you do. I built this project to learn WiFi security hands-on.

## Hardware
 
- Board: While this project is normally done with a Raspberry Pi Zero 2 WH as a compact, mobile design, I could not find the board in stock so I chose to use the Raspberry Pi 3 Model B. This project can be done on any Raspberry Pi. 
- Display: The Waveshare 2.13" e-ink V4 is the typical screen for this project. Beware this screen can come dead sometimes, mine came dead and I had to replace it but then it worked.
- Power: I used the INIU 10000 mAh power bank. I chose this over a UPS HAT because it was cheaper and I didn't want to buy separate batteries. Choose the UPS HAT if you prefer a nicer software shutdown.
- Storage: 32 GB microSD card is perfect for this.
- Cables: If you choose the INIU 10000 mAh power bank, a short USB A to right angle Micro USB cable is helpful. You may refer to my build in the images file in this repo. 

## Software:
- Image: Pwnagotchi image is from https://github.com/jayofelony/pwnagotchi
- Flashed with: I used balenaEtcher to flash but Raspberry Pi imager works as well.

## Build steps:
1. Flash the pwnagotchi image to the microSD card. Make sure you have a device or an adapter that has a microSD card port. Install the image to your device then use a flasher such as balenaEtcher to flash the image onto the microSD card. Once done you may put the microSD into the microSD slot on the Pi. Every Pi is different but on the Pi 3B it was on the bottom side of the Pi. 
2. Attach the e-ink display to the GPIO header on the Pi. There should be 40 pins in two rows on the Pi. Make sure you seat the screen properly with all pins connected firmly to the screen.
3. Then power the Pi using the micro USB slot. Wait for it to boot as it will restart once or twice. Once booted, ssh into the pi using "ssh pi@pwnagotchi.local" to see if it is running properly. The default password for the Pi is "raspberry".
4. Once in check the config.toml file. cd / then cat /etc/pi/pwnagotchi/config.toml. The config file should match the config file in this repo at the bare minimum. You may edit this file later on if you need to.
5. At this point everything should be working properly. Enjoy your pwnagotchi!

## Problems I hit (and how I fixed them):
- I wanted to do this project with the Pi Zero 2 WH but could not find it in stock anywhere for a long time so had to rebuild the plan around the Pi 3 Model B.
- The Waveshare screen that I initially ordered did not work at first. I made sure the config file was correct, the screen was attached correctly, the FPC cable was attached correctly, and ran tests on the screen such as the demo from waveshare themselves. Unfortunately, the screen did not end up working at all so I had to replace the screen for it to then work.

## What I learned:
- How the WPA/WPA 2 4-way handshake works and why capturing it matters.
- Monitor mode on devices and how WiFi deauthentication works.
- Linux/SSH basics on a headless Raspberry Pi. 

