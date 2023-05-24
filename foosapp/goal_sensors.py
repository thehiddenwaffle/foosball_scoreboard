from gpiozero import Button

left_goal_switch = Button(2)
right_goal_switch = Button(3)


def bind_on_goal_scored_left(funct):
    left_goal_switch.when_pressed = funct


def bind_on_goal_scored_right(funct):
    right_goal_switch.when_pressed = funct
