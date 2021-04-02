# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_funhouse.wifi_module`
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

import gc
import ssl
import wifi
import socketpool
import adafruit_requests

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_FunHouse.git"


class WiFi:
    """Class representing the WiFi portion of the ESP32-S2.

    :param status_dotstar: The initialized object for status DotStar. Defaults to ``None``,
                           to not use the status LED

    """

    def __init__(self, *, status_dotstar=None):
        if status_dotstar:
            self.neopix = status_dotstar
        else:
            self.neopix = None
        self.neo_status(0)
        self.requests = None
        self.pool = None
        self._connected = False

        gc.collect()

    def connect(self, ssid, password):
        """
        Connect to the WiFi Network using the information provided

        :param ssid: The WiFi name
        :param password: The WiFi password

        """
        wifi.radio.connect(ssid, password)
        self.pool = socketpool.SocketPool(wifi.radio)
        self.requests = adafruit_requests.Session(
            self.pool, ssl.create_default_context()
        )
        self._connected = True

    def neo_status(self, value):
        """The status DotStar.

        :param value: The color to change the DotStar.

        """
        if self.neopix:
            self.neopix.fill(value)

    @property
    def is_connected(self):
        """
        Return whether we have already connected since reconnections are handled automatically.

        """
        return self._connected

    @property
    def ip_address(self):
        """
        Return the IP Version 4 Address

        """
        return wifi.radio.ipv4_address

    @property
    def enabled(self):
        """
        Return whether the WiFi Radio is enabled

        """
        return wifi.radio.enabled
