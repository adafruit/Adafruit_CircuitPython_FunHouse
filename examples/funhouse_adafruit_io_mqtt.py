# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import time
import random
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

def random_color():
    return random.randrange(0, 7) * 32

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
funhouse.display.show(None)
slider_label = funhouse.add_text(text="Slider:", text_position=(50, 30), text_color=0x606060)
capright_label = funhouse.add_text(text="Touch", text_position=(85, 10), text_color=0x606060)
pir_label = funhouse.add_text(text="PIR", text_position=(60, 10), text_color=0x606060)
capleft_label = funhouse.add_text(text="Touch", text_position=(25, 10), text_color=0x606060)
onoff_label = funhouse.add_text(text="OFF", text_position=(10, 25), text_color=0x606060)
up_label = funhouse.add_text(text="UP", text_position=(10, 10), text_color=0x606060)
sel_label = funhouse.add_text(text="SEL", text_position=(10, 60), text_color=0x606060)
down_label = funhouse.add_text(text="DOWN", text_position=(10, 100), text_color=0x606060)
jst1_label = funhouse.add_text(text="SENSOR 1", text_position=(40, 80), text_color=0x606060)
jst2_label = funhouse.add_text(text="SENSOR 2", text_position=(40, 95), text_color=0x606060)
jst3_label = funhouse.add_text(text="SENSOR 3", text_position=(40, 110), text_color=0x606060)
temp_label = funhouse.add_text(text="Temp:", text_position=(50, 45), text_color=0xFF00FF)
pres_label = funhouse.add_text(text="Pres:", text_position=(50, 60), text_color=0xFF00FF)
funhouse.display.show(funhouse.splash)

#pylint: disable=unused-argument
def connected(client):
    print("Connected to Adafruit IO! Subscribing...")
    client.subscribe("buzzer")
    client.subscribe("neopixels")

def subscribe(client, userdata, topic, granted_qos):
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))

def disconnected(client):
    print("Disconnected from Adafruit IO!")

def message(client, feed_id, payload):
    print("Feed {0} received new value: {1}".format(feed_id, payload))
    if feed_id == "buzzer":
        if int(payload) == 1:
            funhouse.peripherals.play_tone(2000, 0.25)
    if feed_id == "neopixels":
        print(payload)
        color = int(payload[1:], 16)
        funhouse.peripherals.dotstars.fill(color)

#pylint: enable=unused-argument

# Initialize a new MQTT Client object
funhouse.network.init_io_mqtt()
funhouse.network.on_mqtt_connect = connected
funhouse.network.on_mqtt_disconnect = disconnected
funhouse.network.on_mqtt_subscribe = subscribe
funhouse.network.on_mqtt_message = message

print("Connecting to Adafruit IO...")
funhouse.network.mqtt_connect()
sensorwrite_timestamp = time.monotonic()
last_pir = None

while True:
    funhouse.network.mqtt_loop()

    funhouse.set_text("Temp %0.1F" % dps310.temperature, temp_label)
    funhouse.set_text("Pres %d" % dps310.pressure, pres_label)

    # every 10 seconds, write temp/hum/press
    if (time.monotonic() - sensorwrite_timestamp) > 10:
        funhouse.peripherals.led = True
        print("Sending data to adafruit IO!")
        funhouse.network.mqtt_publish("temperature", dps310.temperature)
        funhouse.network.mqtt_publish("humidity", int(aht20.relative_humidity))
        funhouse.network.mqtt_publish("pressure", int(dps310.pressure))
        sensorwrite_timestamp = time.monotonic()
        # Send PIR only if changed!
        if last_pir is None or last_pir != funhouse.peripherals.pir_sensor:
            last_pir = funhouse.peripherals.pir_sensor
            funhouse.network.mqtt_publish("pir", "%d" % last_pir)
        funhouse.peripherals.led = False

    set_label_color(funhouse.peripherals.captouch6, onoff_label, 0x00FF00)
    set_label_color(funhouse.peripherals.captouch7, capleft_label, 0x00FF00)
    set_label_color(funhouse.peripherals.captouch8, capright_label, 0x00FF00)

    slider = funhouse.peripherals.slider
    if slider is not None:
        funhouse.peripherals.dotstars.brightness=slider
        funhouse.set_text("Slider: %1.1f" % slider, slider_label)
    set_label_color(slider is not None, slider_label, 0xFFFF00)

    set_label_color(funhouse.peripherals.button_up, up_label, 0xFF0000)
    set_label_color(funhouse.peripherals.button_sel, sel_label, 0xFFFF00)
    set_label_color(funhouse.peripherals.button_down, down_label, 0x00FF00)
    set_label_color(funhouse.peripherals.pir_sensor, pir_label, 0xFF0000)
    set_label_color(sensors[0].value, jst1_label, 0xFFFFFF)
    set_label_color(sensors[1].value, jst2_label, 0xFFFFFF)
    set_label_color(sensors[2].value, jst3_label, 0xFFFFFF)
