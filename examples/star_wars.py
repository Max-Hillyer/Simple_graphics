from simple_graphics import *

set_bg("black")

blue_text = Text(
    100,
    260,
    "A long time ago in a galaxy far, far away...",
    color="#63a4ff",
    size=28,
    wrap_at= 300,
    visible=False,
)

crawl = Text(
    80,
    680,
    "It is a period of civil wars in the galaxy. "
    "A brave alliance of underground freedom fighters has challenged "
    "the tyranny and oppression of the awesome GALACTIC EMPIRE.\n\n"
    "Striking from a fortress hidden among the billion stars of the galaxy, "
    "rebel spaceships have won their first victory in a battle with the "
    "powerful Imperial Starfleet.\n\n"
    "The EMPIRE fears that another defeat could bring a thousand more "
    "solar systems into the rebellion, and Imperial control over the galaxy "
    "would be lost forever.",
    color="#ffe81f",
    size=27,
    wrap_at=440,
    visible=False,
)

frame = 0

@on_press('r')
def restart():
    global frame 
    frame = 0
    crawl.visible = False
    crawl.y = 600

@on_tick
def animate_opening():
    global frame
    frame += 1

    if frame < 180:
        blue_text.visible = frame > 10
    else:
        blue_text.visible = False
        crawl.visible = True
        
        crawl.y -= 1


run(600, 600, fps=60)