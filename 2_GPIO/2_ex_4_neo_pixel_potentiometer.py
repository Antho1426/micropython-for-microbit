# 2_ex_4_neo_pixel_potentiometer.py





# Setup:
# - Neopixel LEDs on pin0
# - Potentiometer on pin1
# (no need of batteries if you leave the micro:bit plugged into the computer)





# You need a potentiometer here!
# (neopixel module on pin0 and potentiometer on pin1)






"""
This code allows to manually set the blue intensity of the two LEDs of the
neopixel module using the potentiometer. Pressing the button A allows to control
the blue intensity of the left LED (and shuts down the right LED) and pressing
the button B allows to control the blue intensity of the right LED
(and shuts down the left LED)
"""






from microbit import *
import neopixel




# Setup the Neopixel strip on pin0 with a length of 8 pixels
np = neopixel.NeoPixel(pin0, 2) # I connected the special extension board of
                                # the buggy to pin0 of the micro:bit
pixel_id = 0





def map_value_pot_to_LED(value_to_rescale):
    # LEDs values
    res_max = 25
    res_min = 0
    # potentiometer values
    n_max = 950 # max: 972, adjusted: 950
                # (in order to have the last
                # LED (LED n°25) to also potentially light up)
    n_min = 0
    mapped_value = int(res_min + value_to_rescale*(res_max - res_min)/(n_max - n_min))
    return mapped_value


def map_value_pot_to_color(value_to_rescale):
    # motor values
    res_max = 255
    res_min = 0
    # potentiometer values
    n_max = 972
    n_min = 0
    mapped_value = int(res_min + value_to_rescale*(res_max - res_min)/(n_max - n_min))
    return mapped_value



def displayPositiveNumberAndControlNeopixelLEDs(value, pixel_id):

    # LED matrix
    display.clear()
    mapped_value_LED = map_value_pot_to_LED(value)
    if mapped_value_LED <= 25:
        for i in range(mapped_value_LED):
            display.set_pixel(i%5,int(i/5),9)
    else: # in case we are out of bounds
        display.show(Image.CONFUSED)

    # Neopixel LEDs
    mapped_value_neopixel = map_value_pot_to_color(value)
    if (mapped_value_neopixel >= 0) and (mapped_value_neopixel < 230): # 255
        print('mapped_value_neopixel: ', mapped_value_neopixel)
        # ls /dev/cu.*
        # screen /dev/cu.usbmodem... 115200    (screen /dev/cu.usbmodem14102 115200)

        # Assign the current LED a blue value between 0 and 255
        np[pixel_id] = (0, 0, mapped_value_neopixel)

    else:
        np[pixel_id] = (0, 0, 0)







while True:
    # Getting the value from the potentiometer plugged on pin1
    value = pin1.read_analog()

    # Checking which button was pressed
    if button_a.was_pressed():
        pixel_id = 0
        # shutting down the other led
        np[1] = (0, 0, 0)
    if button_b.was_pressed():
        pixel_id = 1
        # shutting down the other led
        np[0] = (0, 0, 0)

    # Computing the blue value for the LED
    displayPositiveNumberAndControlNeopixelLEDs(value, pixel_id)

    # Display the current pixel data on the Neopixel strip
    np.show()
    sleep(100)






