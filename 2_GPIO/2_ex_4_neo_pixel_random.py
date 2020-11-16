# 2_ex_4_neo_pixel_random.py




# Setup:
# - Neopixel LEDs on pin0
# (no need of batteries if you leave the micro:bit plugged into the computer)






# No need of potentiometer here!

# from microbit import *
# import neopixel
#
# np = neopixel.NeoPixel(pin1, 2) # I connected the special extension board of
#                                 # the buggy to pin1 of the micro:bit
# np[0] = (0, 255, 0)
# np[1] = (0, 0, 255)
# np.show()







# Cf. NeoPixel Docs
# (https://microbit-micropython.readthedocs.io/en/latest/neopixel.html)
#=========================
"""
    neopixel_random.py

    Repeatedly displays random colours onto the LED strip.
    This example requires a strip of 8 Neopixels (WS2812) connected to pin0.

"""
from microbit import *
import neopixel
from random import randint

# Setup the Neopixel strip on pin0 with a length of 8 pixels
np = neopixel.NeoPixel(pin0, 2) # I connected the special extension board of
                                # the buggy to pin0 of the micro:bit

while True:
    #Iterate over each LED in the strip

    for pixel_id in range(0, len(np)):
        red = randint(0, 60)
        green = randint(0, 60)
        blue = randint(0, 60)

        # Assign the current LED a random red, green and blue value between 0 and 60
        np[pixel_id] = (red, green, blue)

        # Display the current pixel data on the Neopixel strip
        np.show()
        sleep(100)
#=========================




