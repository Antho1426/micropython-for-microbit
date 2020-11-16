# 3_ex_1_moving_basics.py





# Setup
# - Mount the Bit:Buggy Car
# - Plug the potentiometer on pin0 of the micro:bit
# - Plug the left servo on pin1 of the micro:bit
# - Plug the right servo on pin2 of the micro:bit


# Working:
# - Turn the potentiometer to adjust the forward speed of the buggy




# Packages
from microbit import *

RES_MAX_MOT = 250



# Functions
def map_value_pot_to_LED(value_to_rescale):
    # LEDs values
    res_max = 25
    res_min = 0
    # potentiometer values
    n_max = 950 # max: 972, adjusted: 950
                # (in order to have the last
                # LED (LED n°25) to also potentially light up)
    n_min = 0 # 0
    mapped_value = int(res_min + value_to_rescale*(res_max - res_min)/(n_max - n_min))
    return mapped_value


def pot_remapping(value_to_rescale):
    # potentiometer new values
    res_max = 972
    res_min = 500
    # potentiometer original values
    n_max = 972
    n_min = 0
    mapped_value = int(res_min + value_to_rescale*(res_max - res_min)/(n_max - n_min))
    return mapped_value


def map_value_pot_to_mot(value_to_rescale):
    # motor values
    res_max = RES_MAX_MOT # initially: 250
    res_min = 50
    # potentiometer values
    n_max = 972
    n_min = 0
    mapped_value = int(res_min + value_to_rescale*(res_max - res_min)/(n_max - n_min))
    return mapped_value


def displayPositiveNumberAndControlMotorSpeed(value, mode):

    # LED matrix
    display.clear()
    mapped_value_LED = map_value_pot_to_LED(value)
    if mapped_value_LED <= 25:
        for i in range(mapped_value_LED):
            display.set_pixel(i%5,int(i/5),9)
    else: # in case we are out of bounds
        display.show(Image.CONFUSED)


    # remapping the potentiometer values
    value = pot_remapping(value)


    # Motor
    mapped_value_mot = map_value_pot_to_mot(value)

    if mode == 'forward':
        if mapped_value_mot <= RES_MAX_MOT & mapped_value_mot >= 50:
            pin1.write_analog(mapped_value_mot)
            pin2.write_analog(-mapped_value_mot+(RES_MAX_MOT+50)) # For conversion since the
                                                     # second servo has to turn in
                                                     # the opposite direction
    else: # i.e. "if mode == 'backward'"
        if mapped_value_mot <= RES_MAX_MOT & mapped_value_mot >= 50:
            pin2.write_analog(mapped_value_mot)
            pin1.write_analog(-mapped_value_mot+(RES_MAX_MOT+50)) # For conversion since the
                                                     # second servo has to turn in
                                                     # the opposite direction




# Initializations
pin1.set_analog_period(10)
pin2.set_analog_period(10)
mode = 'forward'



# Infinite loop
while True:
    # Reading the value from the potentiometer (plugged on pin0)
    value = pin0.read_analog()
    # # Lower bound of the values of the potentiometer
    # # (to make the control of the robot possible only in one direction
    # # using the potentiometer)
    # if value < 500:
    #     value = 500

    # Checking which "mode" the user has chosen
    if button_a.was_pressed(): # move forward
        mode = 'forward'
    if button_b.was_pressed(): # move backward
        mode = 'backward'
    displayPositiveNumberAndControlMotorSpeed(value, mode)
    sleep(50)




