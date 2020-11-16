# 4_ex_3_integers_transmitter.py






# Required packages
from microbit import *
import radio
radio.config(group=23)
# The radio won't work unless it's switched on.
radio.on()








# Functions
def adaptLEDmatrixToAccel(x_accel, y_accel):

    # clearing the LED matrix
    display.clear()

    # mapping the values of the acceleration to the values of the
    # pixels of the LED matrix
    x_pos = map_value_accel_to_LED(x_accel)
    y_pos = map_value_accel_to_LED(y_accel)

    # upper and lower bounding the values for x_pos and y_pos
    if x_pos > 2:
        x_pos = 2
    if x_pos < -2:
        x_pos = -2
    if y_pos > 2:
        y_pos = 2
    if y_pos < -2:
        y_pos = -2

    # displaying the current location of the bright point on the LED matrix
    display.set_pixel(x_init + x_pos, y_init + y_pos, 9)

def map_value_accel_to_LED(value_to_rescale):
    # LEDs values
    res_max = 2
    res_min = -2
    # accelerometer values
    n_max = 300
    n_min = -300
    mapped_value = int(value_to_rescale*(res_max - res_min)/(n_max - n_min))
    return mapped_value










# Initializations
x_init = 2
y_init = 2
display.set_pixel(x_init, y_init, 9)
sending_both_accel = False









# Event loop
while True:
    x_accel = accelerometer.get_x() # float
    y_accel = accelerometer.get_y() # float
    print('x_accel: ', x_accel, 'y_accel: ', y_accel)
    # ls /dev/cu.*
    # screen /dev/cu.usbmodem... 115200    (screen /dev/cu.usbmodem14102 115200)


    adaptLEDmatrixToAccel(x_accel, y_accel)

    # single time sending a single accel. value
    if button_a.was_pressed():
        radio.send(str(x_accel)) # sending a string
                                 # (the float has been encoded into a string)

    # sending two accel. values
    # toggling the boolean "sending_both_accel"
    if button_b.was_pressed():
        sending_both_accel = not sending_both_accel
    if sending_both_accel:
        # Sending commands to the receiver micro:bit
        # Encoding the x_accel and the y_accel in a single string with a ";" as
        # separation in between
        radio.send(str(x_accel) + ';' + str(y_accel))

    sleep(100)
