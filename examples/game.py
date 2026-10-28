from random import Random

from simple_graphics import *


SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

GRASS = "#8abf8a"
GRASS_LIGHT = "#a8d39b"
GRASS_DARK = "#6aa375"
WATER = "#5c9fba"
WATER_LIGHT = "#83c3cf"
PATH = "#d8bd83"
PATH_LIGHT = "#ead39c"
BARK = "#6d4937"
LEAF_DARK = "#2e6f4d"
LEAF = "#438b58"
ROCK = "#71858a"
ROCK_LIGHT = "#a8c0bd"
INK = "#203f3c"
GOLD = "#f3c65e"
GOLD_LIGHT = "#ffe49a"

randomizer = Random(11)


world = Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, color=GRASS)

path = Line(
    [(0, 475), (170, 475), (285, 390), (430, 390), (565, 300), (760, 300), (900, 220)],
    width=76,
    color=PATH,
)
path_highlight = Line(
    [(0, 468), (170, 468), (285, 383), (430, 383), (565, 293), (760, 293), (900, 213)],
    width=4,
    color=PATH_LIGHT,
)

pond = Polygon(
    [(540, 30), (790, 18), (900, 95), (900, 210), (770, 250), (610, 190), (500, 100)],
    color=WATER,
)
pond_shine = Line([(600, 75), (720, 58), (820, 91)], width=5, color=WATER_LIGHT)
pond_shine_two = Line([(675, 125), (815, 145)], width=3, color=WATER_LIGHT)


world_walls = [
    Rect(-20, -20, SCREEN_WIDTH + 40, 20, visible=False),
    Rect(-20, SCREEN_HEIGHT, SCREEN_WIDTH + 40, 20, visible=False),
    Rect(-20, -20, 20, SCREEN_HEIGHT + 40, visible=False),
    Rect(SCREEN_WIDTH, -20, 20, SCREEN_HEIGHT + 40, visible=False),
    Polygon(
        [
            (540, 30),
            (790, 18),
            (900, 95),
            (900, 210),
            (770, 250),
            (610, 190),
            (500, 100),
        ],
        visible=False,
    ),
]


def make_tree(x, y, scale=1):
    trunk = Rect(
        x - int(8 * scale),
        y + int(22 * scale),
        int(16 * scale),
        int(28 * scale),
        color=BARK,
    )
    Circle(x, y + int(8 * scale), int(29 * scale), color=LEAF_DARK)
    Circle(x - int(18 * scale), y + int(18 * scale), int(22 * scale), color=LEAF)
    Circle(x + int(17 * scale), y + int(17 * scale), int(23 * scale), color=LEAF)
    Circle(x, y - int(8 * scale), int(25 * scale), color=LEAF)
    Circle(x - int(8 * scale), y - int(15 * scale), int(8 * scale), color=GRASS_LIGHT)
    return Rect(
        x - int(10 * scale),
        y + int(18 * scale),
        int(20 * scale),
        int(35 * scale),
        visible=False,
    )


def make_rock(x, y, size):
    Polygon(
        [
            (x - size, y + size // 2),
            (x - size // 2, y - size),
            (x + size, y - size // 2),
            (x + size // 2, y + size),
            (x - size // 2, y + size),
        ],
        color=ROCK,
    )
    Polygon(
        [(x - size // 2, y - size), (x + size, y - size // 2), (x, y - size // 3)],
        color=ROCK_LIGHT,
    )
    return Circle(x, y, size, visible=False)


obstacles = list(world_walls)
for tree_x, tree_y, tree_scale in [
    (90, 100, 1.0),
    (180, 160, 0.8),
    (320, 95, 1.1),
    (405, 180, 0.75),
    (815, 365, 1.1),
    (700, 470, 0.9),
    (470, 520, 0.8),
    (115, 330, 0.75),
]:
    obstacles.append(make_tree(tree_x, tree_y, tree_scale))

for rock_x, rock_y, rock_size in [
    (245, 270, 15),
    (370, 475, 12),
    (760, 390, 18),
    (455, 80, 11),
]:
    obstacles.append(make_rock(rock_x, rock_y, rock_size))

for _ in range(24):
    grass_x = randomizer.randint(25, SCREEN_WIDTH - 25)
    grass_y = randomizer.randint(25, SCREEN_HEIGHT - 25)
    Line(
        [(grass_x, grass_y + 5), (grass_x + 3, grass_y - 5)],
        width=2,
        color=GRASS_DARK,
    )


goal_glow = Circle(470, 280, 32, color="#f6d982", outline=2)
goal = Circle(470, 280, 12, color=GOLD, visible=False)
goal_flame = Polygon(
    [(470, 261), (478, 278), (470, 286), (462, 278)],
    color=GOLD_LIGHT,
    visible=False,
)

firefly_positions = [(145, 250), (350, 285), (690, 430)]
fireflies = []
for firefly_x, firefly_y in firefly_positions:
    glow = Circle(firefly_x, firefly_y, 15, color="#d9f29a", outline=2)
    light = Circle(firefly_x, firefly_y, 5, color=GOLD_LIGHT)
    fireflies.append((glow, light))

player_shadow = Circle(220, 445, 18, color="#5f956d")
player = Circle(220, 434, 14, color="#d75d4c")
player_face = Circle(220, 430, 7, color="#f3c6a1")
player_hat = Polygon([(207, 428), (220, 414), (233, 428)], color="#274e50")

hud_title = Text(22, 18, "MEADOWLIGHT", color=INK, size=25)
hud_hint = Text(
    24, 50, "WASD / ARROWS  MOVE     COLLECT THE FIREFLIES", color=INK, size=13
)
score_text = Text(720, 24, "LIGHT 0 / 3", color=INK, size=16)
status = Text(24, SCREEN_HEIGHT - 31, "The path is quiet tonight.", color=INK, size=15)

player_x = 220
player_y = 434
collected_fireflies = 0
won = False


def collides_at(x, y):
    player.x = x
    player.y = y
    return any(is_colliding(player, obstacle) for obstacle in obstacles)


def move_player(dx, dy):
    global player_x, player_y

    next_x = player_x + dx
    if not collides_at(next_x, player_y):
        player_x = next_x

    next_y = player_y + dy
    if not collides_at(player_x, next_y):
        player_y = next_y

    player.x = player_x
    player.y = player_y
    player_shadow.x = player_x
    player_shadow.y = player_y + 11
    player_face.x = player_x
    player_face.y = player_y - 4
    player_hat.points = [
        (player_x - 13, player_y - 6),
        (player_x, player_y - 20),
        (player_x + 13, player_y - 6),
    ]


@on_hold("w,up")
def walk_up():
    move_player(0, -4)


@on_hold("s,down")
def walk_down():
    move_player(0, 4)


@on_hold("a,left")
def walk_left():
    move_player(-4, 0)


@on_hold("d,right")
def walk_right():
    move_player(4, 0)


@on_tick
def update_game():
    global collected_fireflies, won

    for glow, light in fireflies[:]:
        if is_colliding(player, glow):
            erase(glow)
            erase(light)
            fireflies.remove((glow, light))
            collected_fireflies += 1
            score_text.text = f"LIGHT {collected_fireflies} / 3"

    if collected_fireflies == 3 and not goal.visible:
        goal.visible = True
        goal_flame.visible = True
        status.text = "The lantern is awake. Find it by the pond."

    if not won and goal.visible and is_colliding(player, goal):
        won = True
        status.text = "You found the lantern. The meadow is awake."
        status.color = "#8b5a24"
    elif not won and collected_fireflies < 3:
        status.text = f"Find the fireflies. {3 - collected_fireflies} remain."
    elif not won:
        distance_x = player.x - goal.x
        distance_y = player.y - goal.y
        distance = (distance_x * distance_x + distance_y * distance_y) ** 0.5
        if distance < 130:
            status.text = "The lantern is close."
        else:
            status.text = "The path is quiet tonight."


set_bg(GRASS)
run(
    width=SCREEN_WIDTH,
    height=SCREEN_HEIGHT,
    caption="Meadowlight - a Simple Graphics exploration game",
    resizable=False,
    fps=60,
)
