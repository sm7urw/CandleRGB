from machine import Pin, PWM, freq
import time
import urandom

# Designad för ESP32-C3-Mini

# Sätt processorfrekvensen till 40 MHz för att spara energi
freq(40000000)

# Konstanter för PWM-frekvens och grundfärger
PWM_FREQ = 1000  # PWM-frekvens i Hz
BASE_RED = 1.0  # Grundintensitet för rött ljus
BASE_GREEN = 0.5  # Grundintensitet för grönt ljus

# Konstanter för flimrande effekten
FLICKER_RED_MIN = 0.9  # Minsta intensitet för rött ljus under flimmer
FLICKER_RED_MAX = 1.0  # Högsta intensitet för rött ljus under flimmer
FLICKER_GREEN_MIN = 0.45  # Minsta intensitet för grönt ljus under flimmer
FLICKER_GREEN_MAX = 0.75  # Högsta intensitet för grönt ljus under flimmer
FLICKER_DELAY_MIN = 0.05  # Minsta fördröjning mellan flimrande effekter i sekunder
FLICKER_DELAY_MAX = 0.2  # Högsta fördröjning mellan flimrande effekter i sekunder

# Ange pinnummer för RGB LED
red_pin = PWM(Pin(2))  # Pin för rött ljus
green_pin = PWM(Pin(3))  # Pin för grönt ljus

# Initiera PWM på de angivna pinnarna
def init_pwm():
    red_pin.freq(PWM_FREQ)  # Ställ in PWM-frekvens för rött ljus
    green_pin.freq(PWM_FREQ)  # Ställ in PWM-frekvens för grönt ljus

# Sätt RGB-färger (utan blå)
def set_rgb(red, green):
    red_pin.duty_u16(int(red * 35535))  # Ställ in duty-cykel för rött ljus
    green_pin.duty_u16(int(green * 35535))  # Ställ in duty-cykel för grönt ljus

# Mjuk fade-out när programmet avbryts
def fade_out():
    for i in range(100, -1, -1):
        factor = i / 100  # Beräkna faktor för gradvis minskning av intensitet
        set_rgb(BASE_RED * factor, BASE_GREEN * factor)  # Ställ in intensitet med faktor
        time.sleep(0.02)  # Vänta kort stund för mjuk övergång

# Flimra LED
def flicker():
    # Sätt grundfärgen
    set_rgb(BASE_RED, BASE_GREEN)  # Ställ in grundfärger
    time.sleep(urandom.uniform(FLICKER_DELAY_MIN, FLICKER_DELAY_MAX))  # Vänta slumpmässig tid

    # Justera färgen för flimrande effekt
    flicker_red = urandom.uniform(FLICKER_RED_MIN, FLICKER_RED_MAX)  # Slumpmässig intensitet för rött ljus
    flicker_green = urandom.uniform(FLICKER_GREEN_MIN, FLICKER_GREEN_MAX)  # Slumpmässig intensitet för grönt ljus
    set_rgb(flicker_red, flicker_green)  # Ställ in slumpmässiga intensiteter
    time.sleep(urandom.uniform(FLICKER_DELAY_MIN, FLICKER_DELAY_MAX))  # Vänta slumpmässig tid

# Kör programmet
init_pwm()  # Initiera PWM

try:
    while True:
        flicker()  # Kör flimrande effekt i en oändlig loop
except KeyboardInterrupt:
    fade_out()  # Mjuk fade-out vid avbrott
    set_rgb(0, 0)  # Släck helt efter fade-out