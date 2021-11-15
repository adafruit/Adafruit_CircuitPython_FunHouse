# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_funhouse`
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
import time
from adafruit_portalbase import PortalBase
from adafruit_funhouse.network import Network
from adafruit_funhouse.graphics import Graphics
from adafruit_funhouse.peripherals import Peripherals

try:
    from typing import Optional, Dict, Union, Callable, Sequence, List
    from adafruit_dotstar import DotStar
except ImportError:
    pass

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_FunHouse.git"


class FunHouse(PortalBase):
    """Class representing the Adafruit FunHouse.

    :param url: The URL of your data source. Defaults to ``None``.
    :param headers: The headers for authentication, typically used by Azure API's.
    :param json_path: The list of json traversal to get data out of. Can be list of lists for
                      multiple data points. Defaults to ``None`` to not use json.
    :param regexp_path: The list of regexp strings to get data out (use a single regexp group). Can
                        be list of regexps for multiple data points. Defaults to ``None`` to not
                        use regexp.
    :param default_bg: The path to your default background image file or a hex color.
                       Defaults to 0x000000.
    :param status_dotstar: The initialized object for status DotStar. Defaults to ``None``,
                           to not use the status LED
    :param json_transform: A function or a list of functions to call with the parsed JSON.
                           Changes and additions are permitted for the ``dict`` object.
    :param rotation: Default rotation is landscape (270) but can be 0, 90, or 180 for
                     portrait/rotated
    :param scale: Default scale is 1, but can be an integer of 1 or greater
    :param debug: Turn on debug print outs. Defaults to False.

    """

    # pylint: disable=too-many-instance-attributes, too-many-locals, too-many-branches, too-many-statements
    def __init__(
        self,
        *,
        url: Optional[str] = None,
        headers: Dict[str, str] = None,
        json_path: Optional[Union[List[str], List[List[str]]]] = None,
        regexp_path: Optional[Sequence[str]] = None,
        default_bg: int = 0,
        status_dotstar: Optional[DotStar] = None,
        json_transform: Optional[Union[Callable, List[Callable]]] = None,
        rotation: int = 270,
        scale: int = 1,
        debug: bool = False,
    ) -> None:

        network = Network(
            status_dotstar=status_dotstar,
            extract_values=False,
            debug=debug,
        )

        graphics = Graphics(
            default_bg=default_bg,
            rotation=rotation,
            scale=scale,
            debug=debug,
        )

        super().__init__(
            network,
            graphics,
            url=url,
            headers=headers,
            json_path=json_path,
            regexp_path=regexp_path,
            json_transform=json_transform,
            debug=debug,
        )

        self.peripherals = Peripherals()

        gc.collect()

    def enter_light_sleep(self, sleep_time: float) -> None:
        """
        Enter light sleep and resume the program after a certain period of time.

        See https://circuitpython.readthedocs.io/en/latest/shared-bindings/alarm/index.html for more
        details.

        :param float sleep_time: The amount of time to sleep in seconds

        """
        if self._alarm:
            dotstar_values = self.peripherals.dotstars
        super().enter_light_sleep(sleep_time)
        for i, _ in enumerate(self.peripherals.dotstars):
            self.peripherals.dotstars[i] = dotstar_values[i]
        gc.collect()
