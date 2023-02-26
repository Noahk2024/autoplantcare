from PIL import Image, ImageDraw, ImageFont
import digitalio
import os
import board
from plant_monitor import PlantMonitor
from time import sleep
from datetime import datetime
import RPi.GPIO as GPIO 

pm = PlantMonitor()

from PIL import Image, ImageDraw
from adafruit_rgb_display import st7789  # pylint: disable=unused-import


# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

disp = st7789.ST7789(spi, height=240, y_offset=80, rotation=180, 

    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)

width = disp.width  # Rotates it to landscape orientation
height = disp.height

width = 240
height = 240
image = Image.new("RGBA", (width, height))


draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, width, height), outline=0, fill=(142, 226, 191))

sunnyimg = Image.open("sunny.png", "r")
moonimg = Image.open("moon.png", "r")
rainyimg = Image.open("rainy.png", "r")
backim = image.copy()
backim.paste(moonimg, (0, 50), moonimg)

font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size = 25)

motor = digitalio.DigitalInOut(board.D12)
motor.direction = digitalio.Direction.OUTPUT

motor.value = False

while(True):
    now = datetime.now()
    current_time = now.hour
    wetness_field = str(pm.get_wetness())
    temp_c_field = str(pm.get_temp())
    humidity_field = str(pm.get_humidity())

    print(f"Wetness: {wetness_field} \t Temperature: {temp_c_field} \t Humidity: {humidity_field}")
    
    if float(wetness_field) < 40:
        backim = image.copy()
        backim.paste(rainyimg, (0, 50), rainyimg)
        d1 = ImageDraw.Draw(backim)
        d2 = ImageDraw.Draw(backim)
        d3 = ImageDraw.Draw(backim)
        d1.text((110, 50), f"Wetness%:\n{wetness_field}", (255, 0, 0), font)
        d2.text((110, 100), f"Temp°C:\n{temp_c_field}", (255, 255, 80), font)
        d3.text((110, 150), f"Humidity%:\n{humidity_field}", (0, 0, 255), font)
        disp.image(backim)
        sleep(2)
        motor.value = True
        sleep(4)
        motor.value = False
        sleep(15)
       
    else:
        #image = backim
        backim = image.copy()
        backim.paste(moonimg, (0, 50), moonimg)
        d1 = ImageDraw.Draw(backim)
        d2 = ImageDraw.Draw(backim)
        d3 = ImageDraw.Draw(backim)
        d1.text((110, 50), f"Wetness%:\n{wetness_field}", (255, 0, 0), font)
        d2.text((110, 100), f"Temp°C:\n{temp_c_field}", (255, 255, 80), font)
        d3.text((110, 150), f"Humidity%:\n{humidity_field}", (0, 0, 255), font)
        disp.image(backim)
        
    sleep(2)
