# 5_ex_1_obstacle_avoidance_microbit_2_motor_control.py
# Using a finite state machine

## Required packages
from microbit import *
import radio
import utime


## Functions
def clip(v):
    vmin = -100
    vmax = 100
    if v > vmax: v = vmax
    if v < vmin: v = vmin
    return v

def goStraight(v):
    """
    Function that sets the left and right servos to a specific speed
    :param v: integer in [-100, 100]
    """
    setLeftSpeed(v+left_motor_adjustement)
    setRightSpeed(v+right_motor_adjustment)

def turnLeft():
    """
    Function that makes the buggy turn to the left with "rotating_speed"
    """
    setLeftSpeed(v=-rotating_speed)
    setRightSpeed(v=rotating_speed)

def turnRight():
    """
    Function that makes the buggy turn to the right with "rotating_speed"
    """
    setLeftSpeed(v=rotating_speed)
    setRightSpeed(v=-rotating_speed)

def setLeftSpeed(v):
    """
    Function that sets the left servo to a specific speed
    :param v: integer in [-100, 100]
    """
    clip(v)
    mapped_value_mot = map_v_range_to_mot_range(v)
    pin1.write_analog(
        -mapped_value_mot + (250 + 50))

def setRightSpeed(v):
    """
    Function that sets the right servo to a specific speed
    :param v: integer in [-100, 100]
    """
    clip(v)
    mapped_value_mot = map_v_range_to_mot_range(v)
    pin2.write_analog(
        mapped_value_mot)  # For conversion

def map_v_range_to_mot_range(value_to_rescale):
    """
    Mapping the values of the range of speed "v"
    ("v" situated between -100 and 100) to the range of the values that the
    servos (i.e. the function write_analog) can take (i.e. between 50 and 250)

    :param value_to_rescale: this is the "v" value to map from
                             (-100,100) to (50,250)
    :return mapped_value: integer value corresponding to the mapped value for
                          the function write_analog
    """
    # motor values
    res_max = 250
    res_min = 50
    # "v" values
    n_max = 100
    n_min = -100
    mapped_value = int(
        150 - value_to_rescale * (res_max - res_min) / (n_max - n_min))
    return mapped_value

def setState(state_forward_access_0, state_rotating_left_access_1, state_forward_a_bit_access_2, state_rotating_right_access_3):
    """
    Function that set the current state of the robot
    """
    global state_forward_access, state_rotating_left_access, state_forward_a_bit_access, state_rotating_right_access
    state_forward_access = state_forward_access_0
    state_rotating_left_access = state_rotating_left_access_1
    state_forward_a_bit_access = state_forward_a_bit_access_2
    state_rotating_right_access = state_rotating_right_access_3



## Initializations

pin1.set_analog_period(10)
pin2.set_analog_period(10)

disable_program = False

incoming_measured_distance_float = 0

state = 'going forward'

enter_set_time_turn_left = True
enter_set_time_going_forward_a_bit = True
enter_set_time_turn_right = True

state_forward_access, state_rotating_left_access, state_forward_a_bit_access, state_rotating_right_access = True, True, True, True

start_time = 0
current_time = 0

# Values to adjust to make the robot go straight ahead and turning correctly
# by 90 degrees
#========================
going_forward_time = 1700
rotating_time_left = 750
rotating_time_right = 700
#========================
rotating_speed = 70
forwardSpeed = 60
#========================
# Adjustments to avoid drift
right_motor_adjustment = 5
left_motor_adjustement = 3
#========================

# Radio initialization
radio.config(group=23)
# The radio won't work unless it's switched on
radio.on()

## Event loop
while True:

    ## Receiving the measured distance from the first micro:bit
    incoming_measured_distance = radio.receive()


    if (not disable_program):

        # Checking that the received data from the radio is not None
        if incoming_measured_distance:
            incoming_measured_distance_float = float(incoming_measured_distance)

            ## 0) Go forward
            if state_forward_access and (incoming_measured_distance_float < 0 or incoming_measured_distance_float > 10):
                state = 'going forward'

            ## Otherwise, entering the obstacle avoidance procedure
            # if an obstacle is closer than 10[cm] to the front of the robot
            # 1) Turning left
            elif state_rotating_left_access:
                state = 'turning left'
            # 2) Going forward a bit
            elif state_forward_a_bit_access:
                state = 'going forward a bit'
            # 3) Turning right
            elif state_rotating_right_access:
                state = 'turning right'
            else:
                pass


            ## Dealing with the current state
            # 0)
            if state == 'going forward':
                goStraight(v=forwardSpeed)
                display.show(Image.HAPPY)

            # 1)
            elif state == 'turning left':
                if enter_set_time_turn_left:
                    start_time = utime.ticks_ms()
                    enter_set_time_turn_left = False

                    setState(False, True, False, False)

                    turnLeft()
                    display.show(Image.ARROW_E)
                current_time = utime.ticks_ms()
                if (abs(current_time - start_time) > rotating_time_left):
                    enter_set_time_turn_left = True

                    setState(False, False, True, False)

                    state = 'going forward a bit'

            # 2)
            elif state == 'going forward a bit':
                if enter_set_time_going_forward_a_bit:
                    start_time = utime.ticks_ms()
                    enter_set_time_going_forward_a_bit = False

                    setState(False, False, True, False)

                    goStraight(v=forwardSpeed)
                    display.show(Image.ARROW_S)
                current_time = utime.ticks_ms()
                if (abs(current_time - start_time) > going_forward_time):
                    enter_set_time_going_forward_a_bit = True

                    setState(False, False, False, True)

                    state = 'turning right'

            # 3)
            elif state == 'turning right':
                if enter_set_time_turn_right:
                    start_time = utime.ticks_ms()
                    enter_set_time_turn_right = False

                    setState(False, False, False, True)

                    turnRight()
                    display.show(Image.ARROW_W)
                current_time = utime.ticks_ms()
                if (abs(current_time - start_time) > rotating_time_right):
                    enter_set_time_turn_right = True
                    # If obstacle detected after right rotation:
                    # Avoid obstacle using the same procedure
                    if (incoming_measured_distance_float <= 10):

                        setState(False, True, False, False)

                        state = 'turning left'
                    # Else, if the passage is free:
                    # Reinitialize the state machine program
                    else:

                        setState(True, True, True, True)

            else:
                pass

    ## Disabling motors (in case of emergency, press button A of the micro:bit)
    if button_a.was_pressed(): # if incoming_measured_distance == 'stop':
        disable_program = True
        # stopping the motors
        pin1.write_analog(150)
        pin2.write_analog(150)


    ## Printing the measured values
    # Printing the received measured distance
    #print('dist. in [cm]: ', incoming_measured_distance_float, '   or. in [°]: ', orientation_in_degrees, '   targ. or. in [°]: ', target_orientation)
    print('dist. in [cm]: ', incoming_measured_distance_float, '   st. - cur. time: ', start_time - current_time)
    # ls /dev/cu.*
    # screen /dev/cu.usbmodem... 115200    (screen /dev/cu.usbmodem14302 115200)

    sleep(90)
    # Make the sleep smaller than the transmitter to
    # prevent old messages from queuing