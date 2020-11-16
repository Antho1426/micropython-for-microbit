# 1_ex_3_display_positive_number.py


from microbit import *

def displayPositiveNumber(d):
    display.clear()
    if d <= 25:
        for i in range(d):
            display.set_pixel(i%5,int(i/5),9)
    else: # in case we are out of bounds
        display.show(Image.CONFUSED)

displayPositiveNumber(13)