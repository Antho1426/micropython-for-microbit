# 3_ex_2_turning_towards_the_slope.py




# Setup
# - Mount the Bit:Buggy Car

# Working
# - Place the buggy on a tilted plane




# Info accelerometer of micro:bit,
# cf.: https://microbit-challenges.readthedocs.io/en/latest/tutorials/accelerometer.html

from microbit import *



# Functions

# def map_value_acc_to_mot(value_to_rescale):
#     # motor values
#     res_max = 250
#     res_min = 50
#     # accelerometer values
#     n_max = 1070 * Kp
#     n_min = -1070 * Kp
#     mapped_value = int(res_min + value_to_rescale*(res_max - res_min)/(n_max - n_min))
#     return mapped_value


def adjustRoll(error_roll, derivative_roll):

    # Motor

    # mapped_value_mot = map_value_acc_to_mot(value)
    #
    # if mapped_value_mot <= 250 & mapped_value_mot >= 50:
    #     pin1.write_analog(mapped_value_mot)
    #     pin2.write_analog(mapped_value_mot)
    #
    # return mapped_value_mot

    #adjustment = abs(Kp * error_roll + Kd * derivative_roll)
    value = Kp * error_roll + Kd * derivative_roll + offset

    # # negative error --> turn left (otherwise --> turn right)
    # if error_roll < 0:
    #     value = offset - adjustment
    # if error_roll > 0:
    #     value = offset + adjustment

    # upper and lower bounding the values for the motors
    if value >= 250:
        value = 250
    if value <= 50:
        value = 50

    # setting the values to the motors
    if (not disable_program):
        pin1.write_analog(value)
        pin2.write_analog(value)




    return value









# Initializations
pin1.set_analog_period(10)
pin2.set_analog_period(10)









# Alternatively to flashing this whole code onto the micro:bit as usual and
# looking at the serial values from a terminal (as described below),
# you can,to see the values of the accelerometer printing in real time
# (as with a "serial monitor"), simply use the REPL tool of the MicroPython
# plugin and copy-paste following part of code only:
#---------------

value = None
# mapped_value_mot = None
#==========
thresh = 70
#==========
#=======
Kp = 0.35
Kd = 0.2
# =======
offset = 150
disable_program = False
iteration_time = 100
error_roll = 0
error_roll_prior = 0

while True:
    x = accelerometer.get_x()
    #print("x: ", x) # for printing in a serial monitor "screen"
    #display.scroll(str(x)) # this line slows down the printing for the serial
                           # monitor a lot! Don't hesitate to comment it!
    desired_x_accel = 0
    measured_x_accel = x

    error_roll = measured_x_accel - desired_x_accel

    derivative_roll = (error_roll - error_roll_prior) / iteration_time

    # Adjusting the orientation of the Bit:Buggy
    if (abs(error_roll) > thresh):
        value = adjustRoll(error_roll, derivative_roll)
    else:
        value = None
        pin1.write_analog(150)
        pin2.write_analog(150)
        # mapped_value_mot = None

    if button_a.was_pressed():
        disable_program = True
        # stopping the motors
        pin1.write_analog(150)
        pin2.write_analog(150)

    print('error in x accel. (error_roll): ', error_roll, '    value for mot (P + D control.): ', value)

    error_roll_prior = error_roll

    sleep(iteration_time)
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






