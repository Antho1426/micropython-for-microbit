# 2_ex_3_measuring_distance.py


# /!\ Don't forget to set the potentiometer in the middle
# (slightly more than the middle position)
# and don't forget to turn on the battery shield!

#================
from microbit import *

import machine # /!\ It seems that this package works only with Python 3.5!!
               # Install following package within PyCharm:
               # micropython-cpython-machine
               # Same problem as I had with the "machine" library:
               # https://python-forum.io/Thread-RE-import-machine-module-named-not-found
               # In Tools > MicroPython > MicroPython REPL, when we type
               # help('modules'), we see that "machine" is one of the available
               # modules of MicroPython
               # Info about the "machine" package of MicroPython:
               # https://docs.micropython.org/en/latest/library/machine.html
import utime # Cf.: https://pypi.org/project/micropython-cpython-utime/
             # Install following package within PyCharm:
             # micropython-cpython-utime


pinTrig = pin0
pinEcho = pin1

# Info about the choice of the value of the "Constant":
# In the environment we work in, the sounds travel at about 343 meters per
# seconds. That corresponds to 0.0343 centimeters per microseconds.
# While *distance = time x velocity*, in our case the distance is travelled
# back and forth, therefore we have *2 x distance = time x velocity*.
# Which leads to *d = t x v / 2 = t x 0.0343 / 2 = t x 0.01715
# = t / 58.3*. So *Constant = 58.3*.
Constant = 58.3

def get_dist_in_cm():
    # send a high pulse to the trigger of HC-SR04
    pinTrig.write_digital(0)
    utime.sleep_us(2)
    pinTrig.write_digital(1)
    utime.sleep_us(10)
    pinTrig.write_digital(0)

    # measure the time in microseconds that it takes to receive a high pulse on the echo pin
    d = machine.time_pulse_us(pinEcho,1,10000) # timeout in 10000 us = 0.01 s
    if d > 0: # echo received
        return d/Constant
    else: # timeout returns -1
        return d

pinEcho.set_pull(pinEcho.NO_PULL)
# Info about "Set Pull": https://makecode.microbit.org/reference/pins/set-pull

while True:
    # display.scroll('ok')
    distance = get_dist_in_cm()
    display.scroll(distance)
    sleep(150)
#================







# Cf. example 1 at https://www.programcreek.com/python/example/101403/machine.time_pulse_us
#----------------
# from microbit import *
# import utime
# import machine
#
# def read_distance():
#     """
#     Reads distance from HC SR04 sensor
#     The result is in centimeters
#     Divider is taken from Makecode library for micro:maqueen
#     """
#     divider = 45 # 42
#     maxtime = 250 * divider
#     pin2.read_digital()  # just for setting PULL_DOWN on pin2
#     pin0.write_digital(0)
#     utime.sleep_us(2)
#     pin0.write_digital(1)
#     utime.sleep_us(10)
#     pin0.write_digital(0)
#
#     duration = machine.time_pulse_us(pin1, 1, maxtime)
#     distance = duration/divider
#     return distance
#
# while True:
#     distance = read_distance()
#     display.scroll(distance)
#----------------


