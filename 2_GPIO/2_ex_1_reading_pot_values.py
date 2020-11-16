# 2_ex_1_reading_pot_values.py


from microbit import *
# Exercise 1: (~ 10-15 minutes)

# Exercise 1.1:
#--------
# while True:
#     value = pin0.read_analog()
#     display.scroll(value)
#     sleep(100)
#--------




# Setup:
# - Set the potentiometer to pin0 of the micro:bit




# Exercise 1.2:
#------- first part to copy-paste
def map_value(value_to_rescale):
    mapped_value = int(0 + value_to_rescale*(25 - 0)/(972 - 0))
    return mapped_value

def displayPositiveNumber(value):
    display.clear()
    mapped_value = map_value(value)
    if mapped_value <= 25:
        for i in range(mapped_value):
            display.set_pixel(i%5,int(i/5),9)
    else: # in case we are out of bounds
        display.show(Image.CONFUSED)
#------- second part to copy-paste
while True:
    value = pin0.read_analog()
    displayPositiveNumber(value)
    sleep(100)
