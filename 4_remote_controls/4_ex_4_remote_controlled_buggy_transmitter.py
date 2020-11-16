# 4_ex_3_remote_controlled_buggy_transmitter



# Required packages
from microbit import *
import radio










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
#===================
iteration_time = 50
#===================

# Radio initialization
radio.config(group=23)
# The radio won't work unless it's switched on.
radio.on()







# Event loop
while True:
    x_accel = accelerometer.get_x()
    y_accel = accelerometer.get_y()

    print('x_accel: ', x_accel, 'y_accel: ', y_accel)
    # ls /dev/cu.*
    # screen /dev/cu.usbmodem... 115200    (screen /dev/cu.usbmodem14102 115200)

    adaptLEDmatrixToAccel(x_accel, y_accel)

    # # Sending commands to the receiver micro:bit
    # if abs(x_accel) > thresh_x_accel:
    #     if x_accel < 0: # turn left
    #         radio.send('turn_left')
    #     else: # meaning x_accel > 0 --> turn right
    #         radio.send('turn_right')
    # if abs(y_accel) > thresh_y_accel:
    #     if y_accel < 0: # go forward
    #         radio.send('go_forward')
    #     else: # meaning y_accel > 0 --> go backward
    #         radio.send('go_backward')


    # Simple "send" test
    if button_a.was_pressed():
        radio.send('heart')
    else:
        # Sending commands to the receiver micro:bit
        # Encoding the x_accel and the y_accel in a single string with a ";" as
        # separation in between
        radio.send(str(x_accel) + ';' + str(y_accel))



    sleep(iteration_time)


