# 3_ex_3_climbing_mountains.py






# Setup
# - Mount the Bit:Buggy Car

# Working
# - Place the buggy on a tilted plane






# Info accelerometer of micro:bit,
# cf.: https://microbit-challenges.readthedocs.io/en/latest/tutorials/accelerometer.html

from microbit import *





def adjustRoll(error_roll, derivative_roll):

    value_roll = Kp_roll * error_roll + Kd_roll * derivative_roll + offset

    # # upper and lower bounding the values for the motors
    # if value_roll >= 250:
    #     value_roll = 250
    # if value_roll <= 50:
    #     value_roll = 50
    #
    # # setting the values to the motors
    # if (not disable_program):
    #     pin1.write_analog(value_roll)
    #     pin2.write_analog(value_roll)

    value_roll_pin1 = value_roll
    value_roll_pin2 = value_roll


    return value_roll_pin1, value_roll_pin2




def adjustPitch(error_pitch, derivative_pitch):

    value_pitch = Kp_pitch * error_pitch + Kd_pitch * derivative_pitch + offset

    # # upper and lower bounding the values for the motors
    # if value_pitch >= 250:
    #     value_pitch = 250
    # if value_pitch <= 50:
    #     value_pitch = 50
    #
    # # setting the values to the motors
    # if (not disable_program):
    #     pin2.write_analog(value_pitch)
    #     pin1.write_analog(-value_pitch+300)

    value_pitch_pin1 = -value_pitch + 300
    value_pitch_pin2 = value_pitch

    return value_pitch_pin1, value_pitch_pin2



def sendCommands(final_value_pin1, final_value_pin2):

    # upper and lower bounding the values for the motors
    if final_value_pin1 >= 250:
        final_value_pin1 = 250
    if final_value_pin1 <= 50:
        final_value_pin1 = 50
    if final_value_pin2 >= 250:
        final_value_pin2 = 250
    if final_value_pin2 <= 50:
        final_value_pin2 = 50

    # setting the values to the motors
    if (not disable_program):
        pin1.write_analog(final_value_pin1)
        pin2.write_analog(final_value_pin2)







# Initializations
pin1.set_analog_period(10)
pin2.set_analog_period(10)









# Alternatively to flashing this whole code onto the micro:bit as usual and
# looking at the serial values from a terminal (as described below),
# you can,to see the values of the accelerometer printing in real time
# (as with a "serial monitor"), simply use the REPL tool of the MicroPython
# plugin and copy-paste following part of code only:
#---------------

value_roll_pin1 = 0
value_roll_pin2 = 0
value_pitch_pin1 = 0
value_pitch_pin2 = 0

#==========
thresh_roll = 70
#==========

#==========
thresh_pitch = 70
#==========

#=======
Kp_roll = 0.35
Kd_roll = 0.2
# =======

#=======
Kp_pitch = 0.35
Kd_pitch = 0.2
# =======

offset = 150
disable_program = False
iteration_time = 100
error_roll = 0
error_roll_prior = 0
error_pitch = 0
error_pitch_prior = 0


while True:

    ## A) Orienting towards steepest slope

    x = accelerometer.get_x()
    #print("x: ", x) # for printing in a serial monitor "screen"
    #display.scroll(str(x)) # this line slows down the printing for the serial
                           # monitor a lot! Don't hesitate to comment it!
    desired_x_accel = 0 # (i.e. value of the x accel. when the Bit:Buggy is on a flat surface)
    measured_x_accel = x
    error_roll = measured_x_accel - desired_x_accel
    derivative_roll = (error_roll - error_roll_prior) / iteration_time
    # Adjusting the orientation of the Bit:Buggy
    if (abs(error_roll) > thresh_roll):
        value_roll_pin1, value_roll_pin2 = adjustRoll(error_roll, derivative_roll)








    ## B) Going towards steepest slope

    y = accelerometer.get_y()
    desired_y_accel = 968 # (i.e. value of the y accel. when the Bit:Buggy (whose micro:bit is tilted by around 60° by design) is on a flat surface)
    measured_y_accel = y
    error_pitch = measured_y_accel - desired_y_accel
    derivative_pitch = (error_pitch - error_pitch_prior) / iteration_time
    # Adjusting the forward speed of the Bit:Buggy
    if (abs(error_pitch) > thresh_pitch):
        value_pitch_pin1, value_pitch_pin2 = adjustPitch(error_pitch, derivative_pitch)





    ## C) Final values to set to the motors
    if (abs(error_roll) > thresh_roll and abs(error_pitch) > thresh_pitch):
        final_value_pin1 = (value_roll_pin1 + value_pitch_pin1) / 2
        final_value_pin2 = (value_roll_pin2 + value_pitch_pin2) / 2
        sendCommands(final_value_pin1, final_value_pin2)
    elif (abs(error_roll) > thresh_roll):
        final_value_pin1 = value_roll_pin1
        final_value_pin2 = value_roll_pin2
        sendCommands(final_value_pin1, final_value_pin2)
    elif (abs(error_pitch) > thresh_pitch):
        final_value_pin1 = value_pitch_pin1
        final_value_pin2 = value_pitch_pin2
        sendCommands(final_value_pin1, final_value_pin2)
    else: # The Bit:Buggy doesn't move!
        pin1.write_analog(offset)
        pin2.write_analog(offset)






    ## Disabling motors (in case of emergency, press button A of the micro:bit)
    if button_a.was_pressed():
        disable_program = True
        # stopping the motors
        pin1.write_analog(offset)
        pin2.write_analog(offset)



    ## Printing real-time measurements in a serial monitor "screen"
    print('error_roll: ', error_roll,
          '    values for roll: ', value_roll_pin1, value_roll_pin2,
          '    error_pitch: ', error_pitch,
          '    values for pitch: ', value_pitch_pin1, value_pitch_pin2)


    error_roll_prior = error_roll
    error_pitch_prior = error_pitch

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






