# 4_ex_3_remote_controlled_buggy_receiver


from microbit import *
import radio





# Functions



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



def sendCommandsToMotors(final_value_pin1, final_value_pin2):

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

value_roll_pin1 = 0
value_roll_pin2 = 0
value_pitch_pin1 = 0
value_pitch_pin2 = 0

#==========
thresh_roll = 80
#==========

#==========
thresh_pitch = 80
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
#===================
iteration_time = 50
#===================
error_roll = 0
error_roll_prior = 0
error_pitch = 0
error_pitch_prior = 0

# Radio initialization
radio.config(group=23)
# The radio won't work unless it's switched on.
radio.on()






# Event loop
while True:

    # # Reading the value from the potentiometer (plugged on pin0)
    # value = pin0.read_analog()

    # # Receiving the acceleration data from the transmitter micro:bit
    # incoming_command = radio.receive()
    # if incoming_command == 'turn_left':
    #     turn_left(value)
    # elif incoming_command == 'turn_right':
    #     turn_right(value)
    # elif incoming_command == 'go_forward':
    #     go_forward(value)
    # else: # meaning that incoming_command == 'go_backward'
    #     go_backward(value)





    ## 0) Receiving the acceleration data from the transmitter micro:bit
    incoming_accel_data = radio.receive()

    # Simple "receive" test
    if incoming_accel_data == 'heart':
        display.clear()
        display.show(Image.HEART)
        sleep(1000)

    if incoming_accel_data:
        x_accel = float(incoming_accel_data.split(";")[0])
        y_accel = float(incoming_accel_data.split(";")[1])
        display.clear()
        display.show(Image.YES)




        ## 1) Orienting the buggy left and right
        desired_x_accel = 0  # (i.e. value of the x accel. when the transmitting micro:bit is horizontal)
        measured_x_accel = x_accel
        error_roll = measured_x_accel - desired_x_accel
        derivative_roll = (error_roll - error_roll_prior) / iteration_time
        # Adjusting the orientation of the Bit:Buggy
        if (abs(error_roll) > thresh_roll):
            value_roll_pin1, value_roll_pin2 = adjustRoll(error_roll,
                                                          derivative_roll)



        ## 2) Going forward or backward
        desired_y_accel = 0 # (i.e. value of the y accel. when the transmitting micro:bit is horizontal)
        measured_y_accel = y_accel
        error_pitch = measured_y_accel - desired_y_accel
        derivative_pitch = (error_pitch - error_pitch_prior) / iteration_time
        # Adjusting the forward speed of the Bit:Buggy
        if (abs(error_pitch) > thresh_pitch):
            value_pitch_pin1, value_pitch_pin2 = adjustPitch(error_pitch, derivative_pitch)





        ## 3) Final values to set to the motors
        if (abs(error_roll) > thresh_roll and abs(error_pitch) > thresh_pitch):
            final_value_pin1 = (value_roll_pin1 + value_pitch_pin1) / 2
            final_value_pin2 = (value_roll_pin2 + value_pitch_pin2) / 2
            sendCommandsToMotors(final_value_pin1, final_value_pin2)
        elif (abs(error_roll) > thresh_roll):
            final_value_pin1 = value_roll_pin1
            final_value_pin2 = value_roll_pin2
            sendCommandsToMotors(final_value_pin1, final_value_pin2)
        elif (abs(error_pitch) > thresh_pitch):
            final_value_pin1 = value_pitch_pin1
            final_value_pin2 = value_pitch_pin2
            sendCommandsToMotors(final_value_pin1, final_value_pin2)
        else:  # The Bit:Buggy doesn't move!
            pin1.write_analog(offset)
            pin2.write_analog(offset)



        ## Printing real-time measurements in a serial monitor "screen"
        print('error_roll: ', error_roll,
              '    values for roll: ', value_roll_pin1, value_roll_pin2,
              '    error_pitch: ', error_pitch,
              '    values for pitch: ', value_pitch_pin1, value_pitch_pin2)



        error_roll_prior = error_roll
        error_pitch_prior = error_pitch

    else:
        display.clear()
        display.show(Image.NO)
        # stopping the motors
        pin1.write_analog(offset)
        pin2.write_analog(offset)



    ## Disabling motors (in case of emergency, press button A of the micro:bit)
    if button_a.was_pressed():
        disable_program = True
        # stopping the motors
        pin1.write_analog(offset)
        pin2.write_analog(offset)






    sleep(iteration_time)







## Python "split" command tests
# Cf.: https://www.w3schools.com/python/ref_string_split.asp
#----------
# incoming_accel_data = "23.45;45.87"
# x_accel = float(incoming_accel_data.split(";")[0])
# y_accel = float(incoming_accel_data.split(";")[1])
#----------

