# 4_ex_2_sending_flash_message

# "micro:bit fireflies"



# We have to install this program on both micro:bit
# By pressing the A button of one micro:bit, the other one lights up all its
# LEDs and eventually (1 chance ouf of 9) sends a flash message back to the
# first micro:bit that will in turn lights up all its LEDs

# Cf.:
# https://microbit-micropython.readthedocs.io/en/latest/radio.html
# https://microbit-micropython.readthedocs.io/en/latest/tutorials/radio.html

# A micro:bit Firefly.
# By Nicholas H.Tollervey. Released to the public domain.
import radio
import random
from microbit import display, Image, button_a, sleep

# Create the "flash" animation frames. Can you work out how it's done?
flash = [Image().invert()*(i/9) for i in range(9, -1, -1)]

# The radio won't work unless it's switched on.
radio.on()

# Event loop.
while True:
    # Button A sends a "flash" message.
    if button_a.was_pressed():
        radio.send('flash')  # a-ha
    # Read any incoming messages.
    incoming = radio.receive()
    if incoming == 'flash':
        # If there's an incoming "flash" message display
        # the firefly flash animation after a random short
        # pause.
        sleep(random.randint(50, 350))
        display.show(flash, delay=100, wait=False)
        # Randomly re-broadcast the flash message after a
        # slight delay.
        if random.randint(0, 9) == 0:
            sleep(500)
            radio.send('flash')  # a-ha