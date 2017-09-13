# XiaomiPI Doorbell

This project interfaces Xiaomi Yi Ants camera and an OrangePI|RaspberryPI board.
When motion is detected by the camera, a led is lighted up on the breadboard.

## Requirements
### Xiaomi Camera
A modified version of the Yi camera, mounting [fritz-smh](https://github.com/fritz-smh/yi-hack) firmware, or one of its fork.
### Orange PI
An OrangePI board. I used OrangePI PC with [Loboris' ubuntu vivid mate distro](http://www.orangepi.org/orangepibbsen/forum.php?mod=viewthread&tid=342&extra=&page=1).
Requirements listed in `requirements.txt` and Python-Virtualenv (not mandatory):
```bash
$ virtualenv venv
$ source venv/bin/activate
$ sudo pip install -r requirements.txt
```
Please note that in order to use GPIO, scripts must be run as a superuser.
### RaspberryPI
TODO

## Usage
Launch scripts `check_motion.py` and `proxy.py` in two different shells:
```bash
$ sudo python check_motion.py
```
```bash
$ sudo python proxy.py
```
### check_motion.py
This script queries the webcam in order to check wether motion is detected. 
In case of motion detection, a led is turned on.
### proxy.py
The proxy offers an interface on the localhost such that when the motion page is opened, the led is turned off.
It is not mandatory to run this proxy for motion detection, its usefulness is to switch off the led.
### Assembly

