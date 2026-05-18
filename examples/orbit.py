from simple_graphics import *
import math

set_bg("#111111")

planets = [
    {"x": 300, "y": 300, "vx": 0.012, "vy": -0.0432, "mass": 1000, "circle": Circle(300, 300, radius=10, color="#ff9c7a")},
    {"x": 300, "y": 400, "vx": -2.4, "vy": 0, "mass": 5, "circle": Circle(300, 400, radius=2, color="#ff9c7a")},
    {"x": 550, "y": 300, "vx": 0, "vy": 2, "mass": 20, "circle": Circle(550, 300, radius=3, color="#ff9c7a")},
    {"x": 565, "y": 300, "vx": 0, "vy": 3.2, "mass": 1, "circle": Circle(565, 300, radius=1, color="#ff9c7a")},
]

@on_tick
def simulate():
    for p in planets:
        ax, ay = 0, 0
        for other in planets:
            if p is other:
                continue
            dx, dy = other["x"] - p["x"], other["y"] - p["y"]
            dist = math.sqrt(dx**2 + dy**2)
            if dist > 1:
                acc = other["mass"] / (dist ** 2)
                ax += acc * dx / dist
                ay += acc * dy / dist
        
        p["vx"] += ax
        p["vy"] += ay
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["circle"].x = p["x"]
        p["circle"].y = p["y"]

run(width=600, height=600, caption="Orbital Mechanics")
