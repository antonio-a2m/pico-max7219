kangurera is a python3 desktop app designed to set the contents of the banners  on the 7129 led matrix

The contents are saved in the content.json file, which is parsed in the Raspberry Pi Pico and displayed as banners.


By now, there can 2 kinds of banners:

* Text banners: Texts displayed in the led matrix adn can have one of the following visual effects:
- Vertical scroll
- Horizontal scroll
- Blink

* Bitmaps: Basic 8x32 px drawings to be created with this app

The communication with the pico, is done with
https://github.com/dhylands/rshell