# 1_ex_2_interact_with_LED_matrix.py


from microbit import *

x_pos = 0
y_pos = 0
display.set_pixel(x_pos,y_pos,9)

while True:
    if button_a.was_pressed(): # increase x
        display.clear()
        x_pos += 1
        if x_pos > 4: # upper bound for x_pos
            x_pos = 4
        display.set_pixel(x_pos,y_pos,9)
        sleep(100)
    if button_b.was_pressed(): # decrease x
        display.clear()
        x_pos -= 1
        if x_pos < 0: # lower bound for x_pos
            x_pos = 0
        display.set_pixel(x_pos,y_pos,9)
        sleep(100)

    if button_a.is_pressed() and button_b.is_pressed(): # increase y_pos
        # Cf.: https://microbit-challenges.readthedocs.io/en/latest/tutorials/buttons.html
        display.clear()
        y_pos += 1
        if y_pos > 4: # upper bound for y_pos
            y_pos = 4
        display.set_pixel(x_pos, y_pos, 9)
        sleep(100)


