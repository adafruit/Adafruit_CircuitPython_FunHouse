Introduction
============


.. image:: https://readthedocs.org/projects/adafruit-circuitpython-funhouse/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/funhouse/en/latest/
    :alt: Documentation Status


.. image:: https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_Bundle/main/badges/adafruit_discord.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/adafruit/Adafruit_CircuitPython_FunHouse/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_FunHouse/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

Helper library for the Adafruit FunHouse board


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Adafruit FunHouse Home Automation board

`Purchase one from the Adafruit shop <http://www.adafruit.com/products/4985>`_


Usage Example
=============

.. code:: python

    import board
    from digitalio import DigitalInOut, Direction, Pull
    import adafruit_dps310
    import adafruit_ahtx0
    from adafruit_funhouse import FunHouse

    funhouse = FunHouse(
        default_bg=0x0F0F00,
        scale=2,
    )

    i2c = board.I2C()
    dps310 = adafruit_dps310.DPS310(i2c)
    aht20 = adafruit_ahtx0.AHTx0(i2c)

    funhouse.peripherals.set_dotstars(0x800000, 0x808000, 0x008000, 0x000080, 0x800080)

    # sensor setup
    sensors = []
    for p in (board.A0, board.A1, board.A2):
        sensor = DigitalInOut(p)
        sensor.direction = Direction.INPUT
        sensor.pull = Pull.DOWN
        sensors.append(sensor)


    def set_label_color(conditional, index, on_color):
        if conditional:
            funhouse.set_text_color(on_color, index)
        else:
            funhouse.set_text_color(0x606060, index)


    # Create the labels
    funhouse.display.root_group = None
    slider_label = funhouse.add_text(
        text="Slider:", text_position=(50, 30), text_color=0x606060
    )
    capright_label = funhouse.add_text(
        text="Touch", text_position=(85, 10), text_color=0x606060
    )
    pir_label = funhouse.add_text(text="PIR", text_position=(60, 10), text_color=0x606060)
    capleft_label = funhouse.add_text(
        text="Touch", text_position=(25, 10), text_color=0x606060
    )
    onoff_label = funhouse.add_text(text="OFF", text_position=(10, 25), text_color=0x606060)
    up_label = funhouse.add_text(text="UP", text_position=(10, 10), text_color=0x606060)
    sel_label = funhouse.add_text(text="SEL", text_position=(10, 60), text_color=0x606060)
    down_label = funhouse.add_text(
        text="DOWN", text_position=(10, 100), text_color=0x606060
    )
    jst1_label = funhouse.add_text(
        text="SENSOR 1", text_position=(40, 80), text_color=0x606060
    )
    jst2_label = funhouse.add_text(
        text="SENSOR 2", text_position=(40, 95), text_color=0x606060
    )
    jst3_label = funhouse.add_text(
        text="SENSOR 3", text_position=(40, 110), text_color=0x606060
    )
    temp_label = funhouse.add_text(
        text="Temp:", text_position=(50, 45), text_color=0xFF00FF
    )
    pres_label = funhouse.add_text(
        text="Pres:", text_position=(50, 60), text_color=0xFF00FF
    )
    funhouse.display.root_group = funhouse.splash

    while True:
        funhouse.set_text("Temp %0.1F" % dps310.temperature, temp_label)
        funhouse.set_text("Pres %d" % dps310.pressure, pres_label)

        print(aht20.temperature, aht20.relative_humidity)
        set_label_color(funhouse.peripherals.captouch6, onoff_label, 0x00FF00)
        set_label_color(funhouse.peripherals.captouch7, capleft_label, 0x00FF00)
        set_label_color(funhouse.peripherals.captouch8, capright_label, 0x00FF00)

        slider = funhouse.peripherals.slider
        if slider is not None:
            funhouse.peripherals.dotstars.brightness = slider
            funhouse.set_text("Slider: %1.1f" % slider, slider_label)
        set_label_color(slider is not None, slider_label, 0xFFFF00)

        set_label_color(funhouse.peripherals.button_up, up_label, 0xFF0000)
        set_label_color(funhouse.peripherals.button_sel, sel_label, 0xFFFF00)
        set_label_color(funhouse.peripherals.button_down, down_label, 0x00FF00)

        set_label_color(funhouse.peripherals.pir_sensor, pir_label, 0xFF0000)
        set_label_color(sensors[0].value, jst1_label, 0xFFFFFF)
        set_label_color(sensors[1].value, jst2_label, 0xFFFFFF)
        set_label_color(sensors[2].value, jst3_label, 0xFFFFFF)


Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/funhouse/en/latest/>`_.

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_FunHouse/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
