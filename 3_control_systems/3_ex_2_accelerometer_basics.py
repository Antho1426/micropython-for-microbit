# 3_ex_2_accelerometer_basics.py




# Setup:
# - No need of batteries, leave the micro:bit plugged into the computer
# (this is for the serial monitor)




# Info accelerometer of micro:bit,
# cf.: https://microbit-challenges.readthedocs.io/en/latest/tutorials/accelerometer.html

from microbit import *




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





# Alternatively to flashing this whole code onto the micro:bit as usual and
# looking at the serial values from a terminal (as described below),
# you can,to see the values of the accelerometer printing in real time
# (as with a "serial monitor"), simply use the REPL tool of the MicroPython
# plugin and copy-paste following part of code only:
#---------------
while True:
    x = accelerometer.get_x()
    y = accelerometer.get_y()
    z = accelerometer.get_z()
    print("x, y, z:", x, y, z) # for printing in a serial monitor "screen"
    #display.scroll(str(x)) # this line slows down the printing for the serial
                           # monitor a lot! Don't hesitate to comment it!

    adaptLEDmatrixToAccel(x, y)

    sleep(200)
#---------------




# Once the above code is flashed onto the micro:bit and runs, you can manually
# set up a serial monitor with following method:
#
# Outputing serial data from the micro:bit to a computer using Mac OS terminal
# (Cf.: https://support.microbit.org/support/solutions/articles/19000022103-outputing-serial-data-from-the-micro-bit-to-a-computer)
#
# Terminal commands:
#
# ls /dev/cu.*
#
# The command above allows to find the correct number in "/dev/cu.usbmodem14302"
# Then simply replace it in following line and run the following command in a
# terminal window (either the Terminal app, iTerm or the built-in terminal of
# PyCharm). This will open the micro:bit's serial output and show all
# messages received from the device.
#
# screen /dev/cu.usbmodem14302 115200
#
# If this command doesn't work, go to Activity Monitor and terminate any
# "screen" processes (or alternatively "kill" any "screen" processes using
# the Alfred utility app e.g.)
#
# Make sure to exit the "screen" properly using following method:
# To exit, press Ctrl-A then Ctrl-D.





# Observations:
#
# Min value: -1068
# Max value: 1068
# Although, in the docs, it is written:
# "These values are registered on a scale of values in range 0 .. 1024"
#
# "The accelerometer is set to measure acceleration values in the range +2g to -2g"