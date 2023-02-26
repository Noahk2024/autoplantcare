from PIL import Image, ImageDraw, ImageFont
import digitalio
import os
import board
from plant_monitor import PlantMonitor
from time import sleep
from datetime import datetime
import RPi.GPIO as GPIO 

pm = PlantMonitor()
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Be sure to check the learn guides for more usage information.

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!

Author(s): Melissa LeBlanc-Williams for Adafruit Industries
"""


from PIL import Image, ImageDraw
from adafruit_rgb_display import ili9341
from adafruit_rgb_display import st7789  # pylint: disable=unused-import
from adafruit_rgb_display import hx8357  # pylint: disable=unused-import
from adafruit_rgb_display import st7735  # pylint: disable=unused-import
from adafruit_rgb_display import ssd1351  # pylint: disable=unused-import
from adafruit_rgb_display import ssd1331  # pylint: disable=unused-import

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)
#motor = digitalio.DigitalInOut(board.D36)
#motor.direction = digitalio.Direction.OUTPUT
# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

disp = st7789.ST7789(spi, height=240, y_offset=80, rotation=180,  # 1.3", 1.54" ST7789

    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)
# pylint: enable=line-too-long


width = disp.width  # we swap height/width to rotate it to landscape!
height = disp.height



#
#
width = 240
height = 240
image = Image.new("RGBA", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(142, 226, 191))
#image.show(image)


sunnyimg = Image.open("sunny.png", "r")
moonimg = Image.open("moon.png", "r")
rainyimg = Image.open("rainy.png", "r")
backim = image.copy()
backim.paste(moonimg, (0, 50), moonimg)

#wetness_field = str(pm.get_wetness())
#temp_c_field = str(pm.get_temp())
#humidity_field = str(pm.get_humidity())
#wetness_field = "39"
#temp_c_field = "24.33"
#humidity_field = "35.02"
font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size = 25)

#GPIO.setup(12, GPIO.OUT, initial=1)

led = digitalio.DigitalInOut(board.D12)
led.direction = digitalio.Direction.OUTPUT
#led.value = True
#sleep(4)
led.value = False

#motor.value = False
while(True):
   # led.value = True
   # sleep(4)
   # led.value = False
    now = datetime.now()
    current_time = now.hour
    wetness_field = str(pm.get_wetness())
    temp_c_field = str(pm.get_temp())
    humidity_field = str(pm.get_humidity())
   # if (current_time > 5 and current_time < 20):
        #  os.system(sudo uhubctl -l 1-1 -p 2 -a on) #Turns on LED lights
       # backim = image.copy()
      #  print(".")
     #   backim.paste(sunnyimg, (0, 50), sunnyimg)
    #    sleep(20) #Pause 20 seconds
#    else:
    print(f"Wetness: {wetness_field} \t Temperature: {temp_c_field} \t Humidity: {humidity_field}")
      #  os.system(sudo uhubctl -l 1-1 -p 2 -a off) #Tuns off LED lights
    if float(wetness_field) < 40:
        #image = backim
        led.value = True
        sleep(4)
        led.value = False
        sleep(15)
        backim = image.copy()
        backim.paste(rainyimg, (0, 50), rainyimg)
 #       motor.value = True
    else:
        #image = backim
        backim = image.copy()
        backim.paste(moonimg, (0, 50), moonimg)
    #os.system(sudo uhubctl -l 1-1 -p 2 -a off)
    #os.system(sudo uhubctl -l 1-1 -p 2 -a on)
    d1 = ImageDraw.Draw(backim)
    d2 = ImageDraw.Draw(backim)
    d3 = ImageDraw.Draw(backim)
    d1.text((110, 50), f"Wetness%:\n{wetness_field}", (255, 0, 0), font)
    d2.text((110, 100), f"Temp°C:\n{temp_c_field}", (255, 255, 80), font)
    d3.text((110, 150), f"Humidity%:\n{humidity_field}", (0, 0, 255), font)
    disp.image(backim)
    sleep(2)
