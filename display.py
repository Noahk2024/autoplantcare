from PIL import Image, ImageDraw, ImageFont
import digitalio
import board
from plant_monitor import PlantMonitor
from time import sleep
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

while(True):
    
    wetness_field = str(pm.get_wetness())
    temp_c_field = str(pm.get_temp())
    humidity_field = str(pm.get_humidity())
     
    if float(wetness_field) < 50:
        image = backim
        backim = image.copy()
        backim.paste(rainyimg, (0, 50), rainyimg)
    else:
        image = backim
        backim = image.copy()
        backim.paste(moonimg, (0, 50), moonimg)
    d1 = ImageDraw.Draw(backim)
    d2 = ImageDraw.Draw(backim)
    d3 = ImageDraw.Draw(backim)
    d1.text((110, 50), f"Wetness%:\n{wetness_field}", (255, 0, 0), font)
    d2.text((110, 100), f"Temp°C:\n{temp_c_field}", (0, 255, 0), font)
    d3.text((110, 150), f"Humidity%:\n{humidity_field}", (0, 0, 255), font)
    disp.image(backim)
    sleep(2)
