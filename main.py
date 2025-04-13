from machine import Pin, PWM
import time
import urandom

# Designad för ESP32-C3-Mini

# Konstanter
PWM_FREQ = 1000
BASE_RED = 1.0
BASE_GREEN = 0.5
BASE_BLUE = 0.0
FLICKER_GREEN_MIN = 0.4
FLICKER_GREEN_MAX = 0.6
FLICKER_DELAY_MIN = 0.04
FLICKER_DELAY_MAX = 0.12

# Ange pinnummer för RGB LED
red_pin = PWM(Pin(2))
green_pin = PWM(Pin(3))
blue_pin = PWM(Pin(4))

# Initiera PWM
def init_pwm():
    red_pin.freq(PWM_FREQ)
    green_pin.freq(PWM_FREQ)
    blue_pin.freq(PWM_FREQ)

# Sätt RGB-färger
def set_rgb(red, green, blue):
    red_pin.duty_u16(int(red * 65535))
    green_pin.duty_u16(int(green * 65535))
    blue_pin.duty_u16(int(blue * 65535))

# Mjuk fade-out när programmet avbryts
def fade_out():
    for i in range(100, -1, -1):
        factor = i / 100
        set_rgb(BASE_RED * factor, BASE_GREEN * factor, BASE_BLUE * factor)
        time.sleep(0.01)

# Flimra LED
def flicker():
    # Sätt grundfärgen
    set_rgb(BASE_RED, BASE_GREEN, BASE_BLUE)
    time.sleep(urandom.uniform(FLICKER_DELAY_MIN, FLICKER_DELAY_MAX))

    # Justera färgen för flimrande effekt
    flicker_green = urandom.uniform(FLICKER_GREEN_MIN, FLICKER_GREEN_MAX)
    set_rgb(BASE_RED, flicker_green, BASE_BLUE)
    time.sleep(urandom.uniform(FLICKER_DELAY_MIN, FLICKER_DELAY_MAX))

# Kör programmet
init_pwm()

try:
    while True:
        flicker()
except KeyboardInterrupt:
    fade_out()  # Mjuk fade-out
    set_rgb(0, 0, 0)  # Släck helt efter fade-out