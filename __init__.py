from neopixel import NeoPixel
import time
from machine import Pin
import display
import random
import buttons
import mch22
import nvs

## Setup
NUM_LEDS = 5
LED_PIN = Pin(5, Pin.OUT)
pixels = NeoPixel(LED_PIN, NUM_LEDS)
NICKNAME = nvs.nvs_getstr("owner", "nickname")
DISPLAY_WIDTH = display.width()

def reboot(pressed):
  if pressed:
    mch22.exit_python()

buttons.attach(buttons.BTN_B,reboot)


def wheel(pos):
  if pos < 0 or pos > 255:
    return (0, 0, 0)
  if pos < 85:
    return (255 - pos * 3, pos * 3, 0)
  if pos < 170:
    pos -= 85
    return (0, 255 - pos * 3, pos * 3)
  pos -= 170
  return (pos * 3, 0, 255 - pos * 3)


def rainbow_cycle(wait):
  for j in range(255):
    for i in range(NUM_LEDS):
      rc_index = (i * 256 // NUM_LEDS) + j
      pixels[i] = wheel(rc_index & 255)
    pixels.write()
    time.sleep_ms(wait)

def drawText(pos_y, text, color):
    font = "PermanentMarker36"
    text_width = display.getTextWidth(text, font)
    if text_width > DISPLAY_WIDTH:
        font = "PermanentMarker22"
        text_width = display.getTextWidth(text, font)

    pos_x = int((DISPLAY_WIDTH - text_width) / 2)
    display.drawText(pos_x, pos_y, text, color, font)

display.drawFill(0)
drawText(60, NICKNAME, 0xffffff)
drawText(150, "FREE HUGS", 0xffffff)
display.flush()

## Loop
while True:
    rainbow_cycle(50)
