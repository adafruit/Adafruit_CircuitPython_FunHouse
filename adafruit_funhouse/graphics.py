# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_funhouse.graphics`
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
from adafruit_portalbase.graphics import GraphicsBase

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_FunHouse.git"


class Graphics(GraphicsBase):
    """Graphics Helper Class for the FunHouse Library

    :param default_bg: The path to your default background image file or a hex color.
                       Defaults to 0x000000.
    :param rotation: Default rotation is landscape (270) but can be 0, 90, 180 for portrait/rotated
    :param debug: Turn on debug print outs. Defaults to False.

    """

    # pylint: disable=too-many-instance-attributes, too-many-locals, too-many-branches, too-many-statements, too-few-public-methods
    def __init__(
        self,
        *,
        default_bg: int = 0,
        rotation: int = 270,
        scale: int = 1,
        debug: bool = False
    ) -> None:
        self._debug = debug
        self.display = board.DISPLAY
        self.display.rotation = rotation

        super().__init__(board.DISPLAY, default_bg=default_bg, scale=scale, debug=debug)
