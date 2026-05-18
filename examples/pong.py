from simple_graphics import *
import random

screenwidth, screenheight = 800, 600

p1 = Rect(10, screenheight // 2, height=100, draggable= True )
p2 = Rect(screenwidth - 20, screenheight // 2, height=100, draggable= True)
ball = Circle(screenwidth // 2, screenheight // 2)
vx = random.choice([-5, 5])
vy = random.choice([-5, 5])


@on_hold("up,down")
def move_p2(key):
    if key == "up":
        p2.y -= 10
    else:
        p2.y += 10


@on_hold("w,s")
def move_p2(key):
    if key == "w":
        p1.y -= 10
    else:
        p1.y += 10


@on_tick
def main():
    global vx, vy
    ball.x += vx
    ball.y += vy

    if ball.y < 0 or ball.y > screenheight:
        vy *= -1

    if is_colliding(ball, p1):
        ball.x += 4 
        vx *= -1
    elif is_colliding(ball, p2):
        ball.x -= 4
        vx *= -1

    if ball.x > screenwidth or ball.x < 0:
        ball.x = screenwidth // 2
        ball.y = screenheight // 2
        vx = random.choice([-5, 5])
        vy = random.choice([-5, 5])


run(screenwidth, screenheight)
