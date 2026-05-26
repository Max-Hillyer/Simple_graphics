from simple_graphics import *
from datetime import datetime
from math import sin, cos, radians

SCREEN_SIZE = 600
CENTER_X = SCREEN_SIZE // 2
CENTER_Y = SCREEN_SIZE // 2
CLOCK_RADIUS = 150

clock_face = Circle(CENTER_X, CENTER_Y, CLOCK_RADIUS, color="#ffffff", outline=2)

center_dot = Circle(CENTER_X, CENTER_Y, 8, color="#000000")

hour_markers = []
for i in range(12):
    angle = radians(i * 30 - 90)
    x1 = CENTER_X + CLOCK_RADIUS * 0.85 * cos(angle)
    y1 = CENTER_Y + CLOCK_RADIUS * 0.85 * sin(angle)
    x2 = CENTER_X + CLOCK_RADIUS * 0.75 * cos(angle)
    y2 = CENTER_Y + CLOCK_RADIUS * 0.75 * sin(angle)

    marker = Line([(x1, y1), (x2, y2)], width=3, color="#000000")
    hour_markers.append(marker)

hour_numbers = []
for i in range(1, 13):
    angle = radians(i * 30 - 90)
    x = CENTER_X + CLOCK_RADIUS * 0.65 * cos(angle) - 8
    y = CENTER_Y + CLOCK_RADIUS * 0.65 * sin(angle) - 12

    num_text = Text(x, y, str(i), size=18, color="#000000")
    hour_numbers.append(num_text)

hour_hand = Line([(CENTER_X, CENTER_Y), (CENTER_X, CENTER_Y)], width=8, color="#000000")
minute_hand = Line(
    [(CENTER_X, CENTER_Y), (CENTER_X, CENTER_Y)], width=5, color="#000000"
)
second_hand = Line(
    [(CENTER_X, CENTER_Y), (CENTER_X, CENTER_Y)], width=2, color="#ff0000"
)


def update_hand(hand, length, angle):
    angle_rad = radians(angle - 90)
    end_x = CENTER_X + length * cos(angle_rad)
    end_y = CENTER_Y + length * sin(angle_rad)
    hand.points = [(CENTER_X, CENTER_Y), (end_x, end_y)]


@on_tick
def update_clock():
    now = datetime.now()

    hours = now.hour % 12
    hour_angle = hours * 30 + (now.minute / 60) * 30

    minute_angle = now.minute * 6 + (now.second / 60) * 6

    second_angle = now.second * 6 + (now.microsecond / 1000000) * 6

    update_hand(hour_hand, 60, hour_angle)
    update_hand(minute_hand, 90, minute_angle)
    update_hand(second_hand, 100, second_angle)


time_display = None


@on_tick(5)
def update_time_display():
    global time_display
    if time_display:
        erase(time_display)

    now = datetime.now()
    time_str = now.strftime("%H:%M:%S")
    time_display = Text(
        CENTER_X - 50, SCREEN_SIZE - 50, time_str, size=24, color="#000000"
    )


set_bg("#f0f0f0")
run(SCREEN_SIZE, SCREEN_SIZE, caption="Clock", resizable=False)
