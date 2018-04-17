import lifxlan
from lifxlan import LifxLAN
import numpy as np
import math
import time


def map_range(x, in_min, in_max, out_min, out_max, clamp=True, return_as_int=False):
    value = out_min + (out_max - out_min) * (x - in_min) / (in_max - in_min)
    value = max(value, out_min)
    value = min(value, out_max)

    if return_as_int:
        value = int(value)

    return value


def colour_to_int(x, int_min=0, int_max=65535, clamp=True):
    x = map_range(x, 0, 1, int_min, int_max, clamp=clamp, return_as_int=True)
    return x


def colour_to_float(x, int_min=0, int_max=65535, clamp=True):
    x = map_range(x, int_min, int_max, 0, 1, clamp=clamp, return_as_int=False)
    return x


class Light():

    def __init__(self, transition_ms=1000, hours_until_refresh=1):
        self.transition_ms = transition_ms
        self.ip = None
        self.mac = None
        self.refresh_threshold = 60 * 60 * hours_until_refresh
        self.last_refresh_time = time.time()
        self.__update_local_lights()

    def __update_local_lights(self):
        refresh = self.last_refresh_time - time.time() > self.refresh_threshold
        self.last_refresh_time = time.time()
        if (self.mac is None) or (self.ip is None) or refresh:
            lifx = LifxLAN()
            self.lights = lifx.get_lights()
            for _light in self.lights:
                self.mac = _light.get_mac_addr()
                self.ip = _light.get_ip_addr()

    def turn_on(self):
        self.__update_local_lights()
        _light = lifxlan.Light(self.mac, self.ip)
        _light.set_power('on', duration=self.transition_ms)

    def turn_off(self):
        self.__update_local_lights()
        _light = lifxlan.Light(self.mac, self.ip)
        _light.set_power('off', duration=self.transition_ms)

    def set_colour(self, hue, saturation, brightness, kelvin):
        hue = colour_to_int(hue)
        saturation = colour_to_int(saturation)
        brightness = colour_to_int(brightness)
        kelvin = colour_to_int(kelvin, int_min=2500, int_max=9000)

        colour = [
            hue,
            saturation,
            brightness,
            kelvin
        ]

        self.__update_local_lights()
        _light = lifxlan.Light(self.mac, self.ip)
        _light.set_color(colour, duration=self.transition_ms)

    def get_colour(self):
        self.__update_local_lights()
        _light = lifxlan.Light(self.mac, self.ip)
        hue, saturation, brightness, kelvin = tuple(_light.get_color())

        hue = colour_to_float(hue)
        saturation = colour_to_float(saturation)
        brightness = colour_to_float(brightness)
        kelvin = colour_to_float(kelvin, int_min=2500, int_max=9000)
        return (hue, saturation, brightness, kelvin)

    def random_colour(self):
        colour = tuple(np.random.random_sample() for _ in range(4))
        self.set_colour(*colour)

    def increase_hue(self, amount=0.2):
        hue, saturation, brightness, kelvin = self.get_colour()
        hue += amount
        hue = math.fmod(hue, 1.0)
        self.set_colour(hue, saturation, brightness, kelvin)

    def set_hue(self, amount=0.2):
        hue, saturation, brightness, kelvin = self.get_colour()
        hue = amount
        hue = math.fmod(hue, 1.0)
        self.set_colour(hue, saturation, brightness, kelvin)

    def decrease_hue(self, amount=0.2):
        hue, saturation, brightness, kelvin = self.get_colour()
        hue -= amount
        hue = math.fmod(hue, 1.0)
        while hue < 0.0:
            hue = 1.0 + hue
        self.set_colour(hue, saturation, brightness, kelvin)

    def increase_saturation(self, amount=0.2):
        hue, saturation, brightness, kelvin = self.get_colour()
        saturation += amount
        self.set_colour(hue, saturation, brightness, kelvin)

    def set_saturation(self, amount=0.2):
        hue, saturation, brightness, kelvin = self.get_colour()
        saturation = amount
        self.set_colour(hue, saturation, brightness, kelvin)

    def decrease_saturation(self, amount=0.2):
        hue, saturation, brightness, kelvin = self.get_colour()
        saturation -= amount
        self.set_colour(hue, saturation, brightness, kelvin)

    def increase_brightness(self, amount=0.2):
        hue, saturation, brightness, kelvin = self.get_colour()
        brightness += amount
        self.set_colour(hue, saturation, brightness, kelvin)

    def set_brightness(self, amount=0.2):
        hue, saturation, brightness, kelvin = self.get_colour()
        brightness = amount
        self.set_colour(hue, saturation, brightness, kelvin)

    def decrease_brightness(self, amount=0.2):
        hue, saturation, brightness, kelvin = self.get_colour()
        brightness -= amount
        self.set_colour(hue, saturation, brightness, kelvin)

    def increase_warmth(self, amount=0.2):
        hue, saturation, brightness, kelvin = self.get_colour()
        kelvin -= amount
        self.set_colour(hue, saturation, brightness, kelvin)

    def set_warmth(self, amount=0.2):
        hue, saturation, brightness, kelvin = self.get_colour()
        kelvin = amount
        self.set_colour(hue, saturation, brightness, kelvin)

    def decrease_warmth(self, amount=0.2):
        hue, saturation, brightness, kelvin = self.get_colour()
        kelvin += amount
        self.set_colour(hue, saturation, brightness, kelvin)
