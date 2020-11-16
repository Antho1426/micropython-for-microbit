# 4_ex_1_teleporting_duck.py





# Teleporting duck

# Cf.: https://microbit.org/projects/make-it-code-it/teleporting-duck/?editor=python

# How it works
# Flash this program onto two micro:bits (ONE AFTER THE OTHER (i.e. UNPLUG THE FIRST ONE BEFORE FLASHING ON THE SECOND)), shake one and a duck appears to travel magically through the air from one to the other. Shake the other to send it back.
# It’s not really magic. It uses the micro:bit’s radio function to send data from one micro:bit to another when the accelerometer detects a shake gesture.
# The program first sets the radio group to 23. Groups are like channels on walkie-talkie radios; they can be number between 0 and 255. It doesn’t matter what number you pick as long as your friend’s micro:bit is using the same group number, and no-one else nearby is using the same group.
# When you shake it, it sends the word ‘DUCK’ on that radio group and clears the screen. If either micro:bit receives a radio message (any radio message), a duck icon appears on its display, so you should only ever have 1 duck visible at any time.

from microbit import *
import radio
radio.config(group=23)
radio.on()

while True:
    message = radio.receive()
    if message:
        display.show(Image.DUCK)
    if accelerometer.was_gesture('shake'):
        display.clear()
        radio.send('duck')
