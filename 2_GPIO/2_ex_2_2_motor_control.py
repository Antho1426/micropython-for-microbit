# 2_ex_2_2_motor_control.py




# Setup
# - Set the potentiometer to pin0 of the micro:bit
# - Set a servo to pin1 of the micro:bit




# To run this example directly entirely from the python file of PyCharm
# (and not with the copy-pasting technique of the micropython_programs.py (since
# it doesn't work very well with big blocks of code...)), you simply have to:
#
# 1) set up the proper configuration of the Python file:
# Go to Run > Edit Configurations > Add New Configuration > MicroPython,
# click "Apply" and then "Ok" (this should be the configuration for the Python
# FILE in which your Python code is situated, i.e. here the
# "ex_2_2_motor_control.py" file).
#
# 2) Then you simply have to click on the green triangle to flash the code on the
# micro:bit and execute it (it automatically creates a .hex file and flashes
# the code onto the micro:bit).
#
# 3) If the message "Unable to find micro:bit. Is it plugged in?" appears in the
# "Run" window at the bottom of the page, simply unplug and re-plug your
# micro:bit in your computer.







from microbit import *

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

def map_value_pot_to_mot(value_to_rescale):
    # motor values
    res_max = 250
    res_min = 50
    # potentiometer values
    n_max = 972
    n_min = 0
    mapped_value = int(res_min + value_to_rescale*(res_max - res_min)/(n_max - n_min))
    return mapped_value

def displayPositiveNumberAndControlMotorSpeed(value):

    # LED matrix
    display.clear()
    mapped_value_LED = map_value_pot_to_LED(value)
    if mapped_value_LED <= 25:
        for i in range(mapped_value_LED):
            display.set_pixel(i%5,int(i/5),9)
    else: # in case we are out of bounds
        display.show(Image.CONFUSED)

    # Motor
    mapped_value_mot = map_value_pot_to_mot(value)
    if mapped_value_mot <= 250 & mapped_value_mot >= 50:
        pin1.write_analog(mapped_value_mot)
    #else:
        #display.show(Image.CONFUSED)



pin1.set_analog_period(10)
# the line above has to be part of the initialization because we have to specify
# the period of the PWM for pin1 only once
# (we don't have to repeat this instruction and especially not in while loop
# (which would slow down the process))


while True:
    value = pin0.read_analog()
    displayPositiveNumberAndControlMotorSpeed(value)
    sleep(50)



# Observations:
#
# With this code, we observe that with up to around the half of the
# values of potentiometer (i.e. when we have around 12/25 LEDs that light up),
# the motor turns clcockwise. Then with around 13/25 LEDs that light up, the
# motor stops and then, it goes in the other direction (counterclockwise)
#
# Potentiometer value  |  Number of LEDs that light up  |  Behaviour of the motor
#---------------------------------------------------------------------------------
#        2             |             0                  |  turns quickly clockwise
#       234            |             6                  |      turns clockwise
#       350            |             9                  |           stops
#       467            |             12                 |           stops
#       623            |             16                 |           stops
#       739            |             19                 |  turns counterclockwise
#       972            |             25                 |  turns quickly counterclockwise



