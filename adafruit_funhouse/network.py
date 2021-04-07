# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_funhouse.network`
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

import ssl
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from adafruit_io.adafruit_io import IO_MQTT
from adafruit_portalbase.network import NetworkBase
from adafruit_funhouse.wifi_module import WiFi

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_FunHouse.git"

IO_MQTT_BROKER = "io.adafruit.com"


class Network(NetworkBase):
    """Class representing the Adafruit FunHouse.

    :param status_dotstar: The initialized object for status DotStar. Defaults to ``None``,
                           to not use the status LED
    :param bool extract_values: If true, single-length fetched values are automatically extracted
                                from lists and tuples. Defaults to ``True``.
    :param debug: Turn on debug print outs. Defaults to False.

    """

    # pylint: disable=too-many-instance-attributes, too-many-locals, too-many-branches, too-many-statements
    def __init__(
        self,
        *,
        status_dotstar=None,
        extract_values=True,
        debug=False,
    ):
        super().__init__(
            WiFi(status_dotstar=status_dotstar),
            extract_values=extract_values,
            debug=debug,
        )
        self._mqtt_client = None
        self.mqtt_connect = None
        self.mqtt_publish = None

    def init_io_mqtt(self):
        """Initialize MQTT for Adafruit IO"""
        try:
            aio_username = self._secrets["aio_username"]
            aio_key = self._secrets["aio_key"]
        except KeyError:
            raise KeyError(
                "Adafruit IO secrets are kept in secrets.py, please add them there!\n\n"
            ) from KeyError

        return self.init_mqtt(IO_MQTT_BROKER, 1883, aio_username, aio_key, True)

    # pylint: disable=too-many-arguments
    def init_mqtt(self, broker, port=1883, username=None, password=None, use_io=False):
        """Initialize MQTT"""
        self.connect()
        self._mqtt_client = MQTT.MQTT(
            broker=broker,
            port=port,
            username=username,
            password=password,
            socket_pool=self._wifi.pool,
            ssl_context=ssl.create_default_context(),
        )
        if use_io:
            self._mqtt_client = IO_MQTT(self._mqtt_client)
        self.mqtt_connect = self._mqtt_client.connect
        self.mqtt_publish = self._mqtt_client.publish

        return self._mqtt_client

    # pylint: enable=too-many-arguments

    def _get_mqtt_client(self):
        if self._mqtt_client is not None:
            return self._mqtt_client
        raise RuntimeError("Please initialize MQTT before using")

    def mqtt_loop(self):
        """Run the MQTT Loop"""
        try:
            if self._mqtt_client is not None:
                self._mqtt_client.loop()
        except MQTT.MMQTTException:
            pass

    @property
    def on_mqtt_connect(self):
        """
        Get or Set the MQTT Connect Handler

        """
        if self._mqtt_client:
            return self._mqtt_client.on_connect
        return None

    @on_mqtt_connect.setter
    def on_mqtt_connect(self, value):
        self._get_mqtt_client()
        self._mqtt_client.on_connect = value

    @property
    def on_mqtt_disconnect(self):
        """
        Get or Set the MQTT Disconnect Handler

        """
        if self._mqtt_client:
            return self._mqtt_client.on_disconnect
        return None

    @on_mqtt_disconnect.setter
    def on_mqtt_disconnect(self, value):
        self._get_mqtt_client()
        self._mqtt_client.on_disconnect = value

    @property
    def on_mqtt_subscribe(self):
        """
        Get or Set the MQTT Subscribe Handler

        """
        if self._mqtt_client:
            return self._mqtt_client.on_subscribe
        return None

    @on_mqtt_subscribe.setter
    def on_mqtt_subscribe(self, value):
        self._get_mqtt_client()
        self._mqtt_client.on_subscribe = value

    @property
    def on_mqtt_message(self):
        """
        Get or Set the MQTT Message Handler

        """
        if self._mqtt_client:
            return self._mqtt_client.on_message
        return None

    @on_mqtt_message.setter
    def on_mqtt_message(self, value):
        self._get_mqtt_client()
        self._mqtt_client.on_message = value

    @property
    def enabled(self):
        """
        Return whether the WiFi is enabled

        """
        return self._wifi.enabled
