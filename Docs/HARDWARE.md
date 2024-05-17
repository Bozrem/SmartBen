# Hardware
Some parts have been bought already, others I would like to finish the software for it before buying


## Board
The system runs on a Raspberry Pi 4b
## Display
[3.2 Inch IPS LCD display at 800x480px][1] \
$28.55. Sits right on the Pi with a nice Mini-HDMI to HDMI connector. USB-C power connection

## Audio
Tore apart some $7 speakers from Goodwill to get 2 10watt 4ohm speakers. I need an amplifier for them to connect with 3.5mm\
I also need to get a microphone setup for when I integrate Google Assistant

## Light
A cool feature I saw on some other high end alarm clocks was a light that slowly turns on to mimic the sun coming up. I would like to integrate this with either a color filtered LED or an RGB led so that the light is a warmer hue

## Buttons
I mess around with keyboards, and I had some spare mechanical switches laying around. It should be as simple as connecting wires to GPIO pins through the switch to GND. Wires are ordered and on the way
### Configuration/Layout
Button 1 (17): Click for Bluetooth Hold for Brightness adjust Clicking it toggles Bluetooth. If its off then turn it on ready to pair, if its on/connected disconnect and turn on. Detect that it has been held if its been down for more than 2 seconds or if another button was pressed while it was still down\
Button 2 (27): Click for dismiss (will just toggle the 'currently going off' boolean in alarm logic or something) Click does a brightness down if button 1 is held\
Button 3 (22): Click for snooze (toggle it like dismiss and reset the timer for 5 minutes from now. Don't implement this logic yet besides a comment) Click does a brightness up if button 1 is held.\
Button 4 (23): Click for play/pause Hold for next track Hold in this case is only to hold for 2 seconds. Other buttons shouldn't do anything when button 4 is held.



[1]: https://thepihut.com/products/3-2-ips-hdmi-lcd-display-for-raspberry-pi-480x800