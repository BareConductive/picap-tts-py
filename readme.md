[![Bare Conductive](http://bareconductive.com/assets/images/LOGO_256x106.png)](http://www.bareconductive.com/)

# Bare Conductive Pi Cap Text To Speech Utility

Example text-input speech synthesis code for the [Bare Conductive Pi Cap](http://www.bareconductive.com/shop/pi-cap/). You need twelve plain text files named TEXT000.txt to TEXT011.txt in a folder called `texts` inside this folder. When you touch electrode E0, TEXT000.txt will be read out to you. When you touch electrode E1, TEXT001.txt will be read, and so on. Playback is not polyphonic (espeak can't handle it).

    picap-tts-py    
    │
    └──texts
         TEXT000.txt    
         TEXT001.txt  
         TEXT002.txt  
         TEXT003.txt  
         TEXT004.txt  
         TEXT005.txt  
         TEXT006.txt  
         TEXT007.txt  
         TEXT008.txt  
         TEXT009.txt  
         TEXT010.txt  
         TEXT011.txt  

## Requirements
* Requires [WiringPi](http://wiringpi.com/) (`apt-get install wiringpi`)
* Requires [Bare Conductive's MPR121 libary for WiringPi](https://github.com/BareConductive/wiringpi-mpr121)
* Requires [espeak](http://espeak.sourceforge.net/) (`apt-get install espeak`)
* Requires [python-espeak](https://launchpad.net/python-espeak) (`apt-get install python-espeak`)

## Install / Build

* You should install this code as part of the Pi Cap Raspbian package: `sudo apt-get install picap`    
* However, if you are doing this yourself, clone the repository, enter it and run `make`

## Usage

    python tts.py

N.B. must be run as root       
