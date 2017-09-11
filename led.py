from pyA20.gpio import gpio
from pyA20.gpio import port


class Led:

    def __init__(self, led=port.PA6):
        self.led = led
        gpio.init()
        gpio.setcfg(led, gpio.OUTPUT)

    def is_on(self):
        return gpio.input(self.led) == 1

    def turn_on(self):
        gpio.output(self.led, 1)

    def turn_off(self):
        gpio.output(self.led, 0)
