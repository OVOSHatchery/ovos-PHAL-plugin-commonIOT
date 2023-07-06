import itertools
import random
import time
from threading import Thread
from time import sleep

from lingua_franca.util.colors import Color

from ovos_PHAL_plugin_commonIOT.opm.base import IOTCapabilties, Switch, IOTDeviceType, Plug


class Bulb(Switch):
    capabilities = Plug.capabilities + [
        IOTCapabilties.REPORT_BRIGHTNESS,
        IOTCapabilties.CHANGE_BRIGHTNESS,
        IOTCapabilties.BLINK_LIGHT,
        IOTCapabilties.BEACON_LIGHT
    ]

    def __init__(self, device_id, host=None, name="generic_bulb",
                 area=None, device_type=IOTDeviceType.BULB, raw_data=None):
        super().__init__(device_id, host, name, area, device_type, raw_data)

    def change_color(self, color="white"):
        if isinstance(color, Color):
            if color.rgb255 == (0, 0, 0):
                self.turn_off()
            else:
                if self.is_off:
                    self.turn_on()
                if Color.from_name("white") != color:
                    print("ERROR: bulb does not support color change")
        else:
            color = Color.from_name(color)
            self.change_color(color)

    @property
    def color(self):
        if self.is_off:
            return Color.from_name("black")
        return Color.from_name("white")

    @property
    def brightness(self):
        """
        Return current brightness 0-100%
        """
        return self.brightness_255 * 100 / 255

    @property
    def brightness_255(self):
        """
        Return current brightness 0-255
        """
        return 255

    def change_brightness(self, value, percent=True):
        pass

    def set_low_brightness(self):
        self.change_brightness(25)

    def set_high_brightness(self):
        self.change_brightness(100)

    def reset(self):
        self.mode = ""
        self._timer = None
        if self.is_off:
            self.turn_on()
        self.set_high_brightness()

    def beacon_slow(self, speed=0.9):

        assert 0 <= speed <= 1

        if self.is_off:
            self.turn_on()
        self.mode = "beacon"

        def cycle():
            while self.mode == "beacon":
                i = 5
                while i < 100:
                    i += 5
                    self.change_brightness(i)
                    sleep(1 - speed)

                while i > 5:
                    i -= 5
                    self.change_brightness(i)
                    sleep(1 - speed)

        self._timer = Thread(target=cycle)
        self._timer.setDaemon(True)
        self._timer.start()

    def beacon(self, speed=0.7):

        assert 0 <= speed <= 1

        if self.is_off:
            self.turn_on()
        self.mode = "beacon"

        def cycle():
            while self.mode == "beacon":
                self.change_brightness(100)
                sleep(1 - speed)
                self.change_brightness(50)
                sleep(1 - speed)
                self.change_brightness(1)
                sleep(1 - speed)
                self.change_brightness(50)

        self._timer = Thread(target=cycle)
        self._timer.setDaemon(True)
        self._timer.start()

    def blink(self, speed=0):

        assert 0 <= speed <= 1

        self.mode = "blink"
        if self.is_off:
            self.turn_on()

        def cycle():
            while self.mode == "blink":
                self.turn_off()
                sleep(1 - speed)
                self.turn_on()
                sleep(1 - speed)

        self._timer = Thread(target=cycle)
        self._timer.setDaemon(True)
        self._timer.start()


class RGBBulb(Bulb):
    capabilities = Bulb.capabilities + [
        IOTCapabilties.REPORT_COLOR,
        IOTCapabilties.CHANGE_COLOR
    ]

    def __init__(self, device_id, host=None, name="generic_rgb_bulb",
                 area=None, device_type=IOTDeviceType.RGB_BULB, raw_data=None):
        super().__init__(device_id, host, name, area, device_type, raw_data)

    def reset(self):
        super().reset()
        self.change_color("white")

    @property
    def as_dict(self):
        return {
            "host": self.host,
            "name": self.name,
            "device_type": "rgb bulb",
            "brightness": self.brightness_255,
            "state": self.is_on,
            "raw": self.raw_data
        }

    # color operations
    def change_color_hex(self, hexcolor):
        self.change_color(Color.from_hex(hexcolor))

    def change_color_hsv(self, h, s, v):
        self.change_color(Color.from_hsv(h, s, v))

    def change_color_rgb(self, r, g, b):
        self.change_color(Color.from_rgb(r, g, b))

    def cross_fade(self, color1, color2, steps=100):
        if isinstance(color1, Color):
            color1 = color1.rgb255
        if isinstance(color2, Color):
            color2 = color2.rgb255
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        for i in range(1, steps + 1):
            r = r1 - int(i * float(r1 - r2) // steps)
            g = g1 - int(i * float(g1 - g2) // steps)
            b = b1 - int(i * float(b1 - b2) // steps)

            self.change_color_rgb(r, g, b)

    def color_cycle(self, color_time=2, cross_fade=False):
        self.mode = "color_cycle"
        # print("Light mode: {mode}".format(mode=self.mode))
        if self.is_off:
            self.turn_on()

        def cycle_color():

            class Red(Color):
                def __new__(cls, *args, **kwargs):
                    return Color.from_rgb(255, 0, 0)

            class Orange(Color):
                def __new__(cls, *args, **kwargs):
                    return Color.from_rgb(255, 125, 0)

            class Yellow(Color):
                def __new__(cls, *args, **kwargs):
                    return Color.from_rgb(255, 255, 0)

            class SpringGreen(Color):
                def __new__(cls, *args, **kwargs):
                    return Color.from_rgb(125, 255, 0)

            class Green(Color):
                def __new__(cls, *args, **kwargs):
                    return Color.from_rgb(0, 255, 0)

            class Turquoise(Color):
                def __new__(cls, *args, **kwargs):
                    return Color.from_rgb(0, 255, 125)

            class Cyan(Color):
                def __new__(cls, *args, **kwargs):
                    return Color.from_rgb(0, 255, 255)

            class Ocean(Color):
                def __new__(cls, *args, **kwargs):
                    return Color.from_rgb(0, 125, 255)

            class Blue(Color):
                def __new__(cls, *args, **kwargs):
                    return Color.from_rgb(0, 0, 255)

            class Violet(Color):
                def __new__(cls, *args, **kwargs):
                    return Color.from_rgb(125, 0, 255)

            class Magenta(Color):
                def __new__(cls, *args, **kwargs):
                    return Color.from_rgb(255, 0, 255)

            class Raspberry(Color):
                def __new__(cls, *args, **kwargs):
                    return Color.from_rgb(255, 0, 125)

            colorwheel = [Red(), Orange(), Yellow(), SpringGreen(),
                          Green(), Turquoise(), Cyan(), Ocean(),
                          Blue(), Violet(), Magenta(), Raspberry()]

            # use cycle() to treat the list in a circular fashion
            colorpool = itertools.cycle(colorwheel)

            # get the first color before the loop
            color = next(colorpool)

            while self.mode == "color_cycle":
                # set to color and wait
                self.change_color(color)
                time.sleep(color_time)

                # fade from color to next color
                next_color = next(colorpool)
                if cross_fade:
                    self.cross_fade(color, next_color)

                # ready for next loop
                color = next_color

        self._timer = Thread(target=cycle_color)
        self._timer.setDaemon(True)
        self._timer.start()

    def random_color_cycle(self, color_time=2):
        self.mode = "random_color_cycle"
        if self.is_off:
            self.turn_on()

        def cycle_color():

            while self.mode == "random_color_cycle":
                # set to color and wait
                self.random_color()
                time.sleep(color_time)

        self._timer = Thread(target=cycle_color)
        self._timer.setDaemon(True)
        self._timer.start()

    def random_color(self):
        color = Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.change_color(color)


class RGBWBulb(RGBBulb):
    def __init__(self, device_id, host=None, name="generic_rgbw_bulb",
                 area=None, device_type=IOTDeviceType.RGBW_BULB, raw_data=None):
        super().__init__(device_id, host, name, area, device_type, raw_data)

