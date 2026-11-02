from gpiozero import Button
import os

# detect if running on a Raspberry Pi
def _is_raspberry_pi():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            return 'Raspberry Pi' in f.read()
    except:
        return False

IS_PI = _is_raspberry_pi()

if IS_PI:
    from gpiozero import Button
else:
    # mock button class for non-pi development (so u can run this on your laptop without it being mad that u have no gpio interface to talk to :p)
    class Button:
        def __init__(self, pin, pull_up=True, bounce_time=0.05):
            self.pin = pin
            self.is_pressed = False

PIN_MAP = {
    'back':    17,
    'forward': 27,
    'select':  22,
    'home':    23,
}

class HardwareButtons:
    def __init__(self):
        self._btns = {
            name: Button(pin, pull_up=True, bounce_time=0.05)
            for name, pin in PIN_MAP.items()
        }
        self._prev = {name: False for name in self._btns}

    def poll(self):
        just_pressed = []
        for name, btn in self._btns.items():
            now = btn.is_pressed
            if now and not self._prev[name]:
                just_pressed.append(name)
            self._prev[name] = now
        return just_pressed