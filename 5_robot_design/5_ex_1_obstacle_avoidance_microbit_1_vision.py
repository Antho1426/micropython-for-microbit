# 5_ex_1_obstacle_avoidance_microbit_1_vision.py







# Setup for this micro:bit:
# - Micro:bit 1 is the micro:bit that integrates the values of the ultrasound
# sensor used to detect obstacles
# /!\ Refer to the instructions for using the HC-SR04!
# - Unplug everything
# - Insert the three AAA batteries
# - Do the montage as specified in the instructions!
# (/!\ micro:bit works with 3.3[V] --> that's the reason why we use a
# potentiometer as a voltage divider to go from the 4.5-5[V] of the battery
# shield with three AAA batteries (3*1.5 = 4.5[V]) to the desired 3.3[V]
# --> the echo sent to the microcontroller goes to 0 to 3.3[V] and no more from
# 0 to 5[V] (which would have burnt the microcontroller))
#
# /!\ The potentiometer has to be turned a little bit more than the half
# (because otherwise we might be at the limit and the micro:bit might not
# recognize the ultrasound sensor...)

# Working:
# "trigger" = input of the sensor --> when it receives the triger, an ultrasound
# is sent
# When this signal is received back, an "echo" is sent to the microcontroller







## Required packages
from microbit import *
import machine
import utime
import radio




## Functions
def get_dist():
    # send a pulse
    pinTrig.write_digital(0)
    utime.sleep_us(2)
    pinTrig.write_digital(1)
    utime.sleep_us(10)
    pinTrig.write_digital(0)

    # check echo and time it to determine distance
    d = machine.time_pulse_us(pinEcho,1,11600)
    if d>0:
        return d/58
    else:
        return d

def displayPix(d):
    #d_int = int(d)
    display.clear()
    for j in range(5):
        for i in range(5):
            if d > j*5+i:
                display.set_pixel(i,j,9)







## Initializations

# Attributing the pins
pinTrig = pin0
pinEcho = pin1

# Following line is used to set the default pull (if it's connected to nothing,
# we can tell the controller to pull the voltage low or high --> in this case,
# by default, the pull is set to 'NO_PULL', this means that we tell our
# microcontroller not to mess with pulling the values of the pins)
pinEcho.set_pull(pinEcho.NO_PULL)

# Radio initialization
radio.config(group=23)
# The radio won't work unless it's switched on.
radio.on()









## Event loop
while True:

    measured_distance = get_dist()
    print('distance in [cm]:', measured_distance)
    # ls /dev/cu.*
    # screen /dev/cu.usbmodem... 115200    (screen /dev/cu.usbmodem14302 115200)

    # Displaying the distance with the LED matrix
    #display.show(d)
    displayPix(measured_distance)


    # Sending the distance measurement to the second micro:bit
    if measured_distance:
        # Encoding the measured_distance in a string
        radio.send(str(measured_distance))


    sleep(100)




