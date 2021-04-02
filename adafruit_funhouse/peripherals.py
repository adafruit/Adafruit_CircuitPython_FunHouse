# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_funhouse.peripherals`
================================================================================

Helper library for the Adafruit FunHouse board.


* Author(s): Melissa LeBlanc-Williams

Implementation Notes
--------------------

**Hardware:**

* `Adafruit FunHouse <https://www.adafruit.com/product/4985>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

* Adafruit's PortalBase library: https://github.com/adafruit/Adafruit_CircuitPython_PortalBase

"""

import board
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn
import touchio
import simpleio
import adafruit_dotstar

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_FunHouse.git"


class Peripherals:
    """Peripherals Helper Class for the FunHouse Library"""

    # pylint: disable=too-many-instance-attributes, too-many-locals, too-many-branches, too-many-statements
    def __init__(self):
        # Dotstars
        self.dotstars = adafruit_dotstar.DotStar(
            board.DOTSTAR_CLOCK, board.DOTSTAR_DATA, 5, brightness=0.3
        )

        # Light Sensor
        self._light = AnalogIn(board.LIGHT)

        # Buttons
        self._buttons = []
        for pin in (board.BUTTON_DOWN, board.BUTTON_SELECT, board.BUTTON_UP):
            switch = DigitalInOut(pin)
            switch.direction = Direction.INPUT
            switch.pull = Pull.DOWN
            self._buttons.append(switch)

        # Cap Tocuh Pads
        self._ctp = []
        for pin in (
            board.CAP6,
            board.CAP7,
            board.CAP8,
            board.CAP13,
            board.CAP12,
            board.CAP11,
            board.CAP10,
            board.CAP9,
        ):
            cap = touchio.TouchIn(pin)
            self._ctp.append(cap)

        # LED
        self._led = DigitalInOut(board.LED)
        self._led.direction = Direction.OUTPUT

        # PIR Sensor
        self._pir = DigitalInOut(board.PIR_SENSE)
        self._pir.direction = Direction.INPUT

    @staticmethod
    def play_tone(frequency, duration):
        """Automatically Enable/Disable the speaker and play
        a tone at the specified frequency for the specified duration
        It will attempt to play the sound up to 3 times in the case of
        an error.
        """
        if frequency <= 0:
            raise ValueError("The frequency has to be greater than 0.")
        attempt = 0
        # Try up to 3 times to play the sound
        while attempt < 3:
            try:
                simpleio.tone(board.SPEAKER, frequency, duration)
                break
            except NameError:
                pass
            attempt += 1

    def set_dotstars(self, *values):
        """Set the dotstar values to the provided values"""
        for i, value in enumerate(values[: len(self.dotstars)]):
            self.dotstars[i] = value

    def deinit(self):
        """Call deinit on all resources to free them"""
        self.dotstars.deinit()
        for button in self._buttons:
            button.deinit()
        for ctp in self._ctp:
            ctp.deinit()
        self._light.deinit()
        self._led.deinit()
        self._pir.deinit()

    @property
    def button_down(self):
        """
        Return whether Down Button is pressed
        """
        return self._buttons[0].value

    @property
    def button_sel(self):
        """
        Return whether Sel Button is pressed
        """
        return self._buttons[1].value

    @property
    def button_up(self):
        """
        Return whether Up Button is pressed
        """
        return self._buttons[2].value

    @property
    def any_button_pressed(self):
        """
        Return whether any button is pressed
        """
        return True in [button.value for button in enumerate(self._buttons)]

    @property
    def captouch6(self):
        """
        Return whether CT6 Touch Pad is touched
        """
        return self._ctp[0].value

    @property
    def captouch7(self):
        """
        Return whether CT7 Touch Pad is touched
        """
        return self._ctp[1].value

    @property
    def captouch8(self):
        """
        Return whether CT8 Touch Pad is touched
        """
        return self._ctp[2].value

    @property
    def slider(self):
        """
        Return the slider position value in the range of 0.0-1.0 or None if not touched
        """
        val = 0
        cap_map = b"\x01\x03\x02\x05\x04\x0c\x08\x18\x10"
        for cap in range(5):
            raw = self._ctp[cap + 3].raw_value
            if raw > 15000:
                val += 1 << (cap)
        for i, pos in enumerate(tuple(cap_map)):
            if val == pos:
                print(i, len(cap_map) - 1)
                return round(i / (len(cap_map) - 1), 1)
        return None

    @property
    def light(self):
        """
        Return the value of the light sensor. The neopixel_disable property
        must be false to get a value.

        .. code-block:: python

            import time
            from adafruit_funhouse import FunHouse

            funhouse = FunHouse()

            while True:
                print(funhouse.peripherals.light)
                time.sleep(0.01)

        """
        return self._light.value

    @property
    def led(self):
        """
        Return or set the value of the LED
        """
        return self._led.value

    @led.setter
    def led(self, value):
        self._led.value = bool(value)

    @property
    def pir_sensor(self):
        """
        Return the value of the PIR Sensor
        """
        return self._pir.value
