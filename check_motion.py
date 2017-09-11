import requests
import time

from config import CAMERA
from led import Led
from pyA20.gpio import gpio
from pyA20.gpio import port
from six import _print


URL = 'http://%s/motion' % CAMERA

led = Led()
# led = port.PA6
# gpio.init()
# gpio.setcfg(led, gpio.OUTPUT)


def _get_last_motion():
    r = requests.get(URL, stream=True, headers={})
    return r.content.strip()


last = _get_last_motion()
try:
    while True:
        this = _get_last_motion()
        _print('%s: last motion %s' % (time.time(), this))
        if this != last:
            _print('Motion detected')
            # Turn on led
            # gpio.output(led, 1)
            led.turn_on()
            _print('Led turned on')
        last = this
        # Sleep 10 seconds
        time.sleep(10)
except KeyboardInterrupt:
    _print('Shut down led')
    # gpio.output(led, 0)
    led.turn_off()
    _print('Bye')
except Exception as e:
    # gpio.output(led, 0)
    led.turn_off()
    _print('Exit with exception')
    _print(e)
