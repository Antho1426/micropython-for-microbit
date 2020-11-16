# 1_ex_1_1_press_buttons.py


from microbit import *

while True:
    if button_a.was_pressed():
        display.set_pixel(0,2,9)
        sleep(1000)
        display.clear()
    if button_b.was_pressed():
        display.set_pixel(4,2,9)
        sleep(1000)
        display.clear()
    sleep(100)
    # sleep(100) is here because otherwise the microcontroller would run too
    # fast for nothing! At any rate, we are not able to press the buttons more
    # the once every 100[µs]!