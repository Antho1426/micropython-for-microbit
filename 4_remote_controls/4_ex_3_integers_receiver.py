# 4_ex_3_integers_receiver.py





from microbit import *
import radio
radio.config(group=23)
# The radio won't work unless it's switched on.
radio.on()


# # Default value of the incoming_data
# incoming_data = '.'

# Event loop
while True:
    incoming_data = radio.receive() # receiving a string

    if (incoming_data) and not (';' in incoming_data): # checking if we have received a single data
        display.clear()
        display.scroll(incoming_data)
    elif (incoming_data) and (';' in incoming_data): # checking if we have received two data
        x_accel = float(incoming_data.split(";")[0])
        y_accel = float(incoming_data.split(";")[1])
        display.clear()
        display.show(Image.YES)
        sleep(100)
        print('x_accel and y_accel of transmitter µbit: ', x_accel, y_accel)
        # ls /dev/cu.*
        # screen /dev/cu.usbmodem... 115200    (screen /dev/cu.usbmodem14102 115200)
    else:
        display.clear()
        display.show(Image.NO)
        sleep(100)
