import time

from pyA20.gpio import gpio
from pyA20.gpio import port

led = port.PA6
pir = port.PA1

gpio.init()
gpio.setcfg(led, gpio.OUTPUT)
gpio.setcfg(pir, gpio.INPUT)

try:
    while True:
        i = gpio.input(pir)
        if i == 0:   # When output from motion sensor is LOW
            print "No intruders ", i
            gpio.output(led, 0)  # Turn OFF LED
            time.sleep(1)
        elif i == 1:  # When output from motion sensor is HIGH
            print "Intruder detected ", i
            gpio.output(led, 1)  # Turn ON LED
            time.sleep(1)
except KeyboardInterrupt:
    gpio.output(led, 0)
    print "Bye"
