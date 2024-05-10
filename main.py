# Flickering RGB-led Python-script for Raspberry PI Pico W
# Author: Henrik Korslind (henrik@korslind.com)

from machine import Pin, PWM
import time
import urandom

# Ange pinnummer för RGB LED
red_pin = PWM(Pin(0))
green_pin = PWM(Pin(1))
blue_pin = PWM(Pin(2))

# Konfigurera varje pin som PWM
red_pin.freq(1000)
green_pin.freq(1000)
blue_pin.freq(1000)

def set_rgb(red, green, blue):
    red_pin.duty_u16(int(red * 65535))
    green_pin.duty_u16(int(green * 65535))
    blue_pin.duty_u16(int(blue * 65535))

def flicker():
    # Sätt en grundläggande färg för "ljuset"
    set_rgb(1.0, 0.5, 0.0) # Varmt gult ljus
    time.sleep(urandom.uniform(0.07, 0.12)) # Vänta slumpmässigt mellan 70 och 120 ms

    # Slumpmässigt justera färgen för att simulera flimring
    set_rgb(1.0, urandom.uniform(0.4, 0.6), 0.0)
    time.sleep(urandom.uniform(0.04, 0.08)) # Vänta slumpmässigt mellan 40 och 80 ms

try:
    while True:
        flicker()
except KeyboardInterrupt:
    set_rgb(0, 0, 0) # Stäng av LED när skriptet avslutas