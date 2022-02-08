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
import adafruit_dps310
import adafruit_ahtx0
import adafruit_dotstar

try:
    from typing import Optional
except ImportError:
    pass

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_FunHouse.git"


class Peripherals:
    """Peripherals Helper Class for the FunHouse Library


    Attributes:
        dotstars (DotStar): The DotStars on the FunHouse board.
            See https://circuitpython.readthedocs.io/projects/dotstar/en/latest/api.html
    """

    # pylint: disable=too-many-instance-attributes, too-many-locals, too-many-branches, too-many-statements
    def __init__(self) -> None:
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
            cap.threshold = 20000
            self._ctp.append(cap)

        self.i2c = board.I2C()
        self._dps310 = adafruit_dps310.DPS310(self.i2c)
        self._aht20 = adafruit_ahtx0.AHTx0(self.i2c)

        # LED
        self._led = DigitalInOut(board.LED)
        self._led.direction = Direction.OUTPUT

        # PIR Sensor
        self._pir = DigitalInOut(board.PIR_SENSE)
        self._pir.direction = Direction.INPUT

    @staticmethod
    def play_tone(frequency: float, duration: float) -> None:
        """Automatically Enable/Disable the speaker and play
        a tone at the specified frequency for the specified duration
        It will attempt to play the sound up to 3 times in the case of
        an error.
        """
        if frequency < 0:
            raise ValueError("Negative frequencies are not allowed.")
        attempt = 0
        # Try up to 3 times to play the sound
        while attempt < 3:
            try:
                simpleio.tone(board.SPEAKER, frequency, duration)
                break
            except NameError:
                pass
            attempt += 1

    def set_dotstars(self, *values: int) -> None:
        """Set the dotstar values to the provided values"""
        for i, value in enumerate(values[: len(self.dotstars)]):
            self.dotstars[i] = value

    def deinit(self) -> None:
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
    def button_down(self) -> bool:
        """
        Return whether Down Button is pressed
        """
        return self._buttons[0].value

    @property
    def button_sel(self) -> bool:
        """
        Return whether Sel Button is pressed
        """
        return self._buttons[1].value

    @property
    def button_up(self) -> bool:
        """
        Return whether Up Button is pressed
        """
        return self._buttons[2].value

    @property
    def any_button_pressed(self) -> bool:
        """
        Return whether any button is pressed
        """
        return True in [button.value for (i, button) in enumerate(self._buttons)]

    @property
    def captouch6(self) -> bool:
        """
        Return whether CT6 Touch Pad is touched
        """
        return self._ctp[0].value

    @property
    def captouch7(self) -> bool:
        """
        Return whether CT7 Touch Pad is touched
        """
        return self._ctp[1].value

    @property
    def captouch8(self) -> bool:
        """
        Return whether CT8 Touch Pad is touched
        """
        return self._ctp[2].value

    @property
    def slider(self) -> Optional[float]:
        """
        Return the slider position value in the range of 0.0-1.0 or None if not touched
        """
        val = 0
        cap_map = (0x01, 0x03, 0x02, 0x06, 0x04, 0x0C, 0x08, 0x18, 0x10)
        for cap in range(5):
            if self._ctp[cap + 3].value:
                val += 1 << (cap)
        return cap_map.index(val) / 8 if val in cap_map else None

    @property
    def light(self) -> int:
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
    def temperature(self) -> float:
        """
        Return the temperature in degrees Celsius
        """
        return self._aht20.temperature

    @property
    def relative_humidity(self) -> float:
        """
        Return the relative humidity as a percentage (0 - 100)
        """
        return self._aht20.relative_humidity

    @property
    def pressure(self) -> float:
        """
        Return the barometric pressure in hPa, or equivalently in mBar
        """
        return self._dps310.pressure

    @property
    def led(self) -> bool:
        """
        Return or set the value of the LED
        """
        return self._led.value

    @led.setter
    def led(self, value: bool) -> None:
        self._led.value = bool(value)

    @property
    def pir_sensor(self) -> bool:
        """
        Return the value of the PIR Sensor
        """
        return self._pir.value
