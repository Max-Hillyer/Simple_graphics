from simple_graphics import *
import random

GRID_WIDTH = 50
GRID_HEIGHT = 40
CELL_SIZE = 12

grid = [[False] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

cells = []
for y in range(GRID_HEIGHT):
    row = []
    for x in range(GRID_WIDTH):
        cell = Rect(
            x * CELL_SIZE,
            y * CELL_SIZE,
            CELL_SIZE - 1,
            CELL_SIZE - 1,
            color="#ffffff",
            visible=grid[y][x],
        )
        row.append(cell)
    cells.append(row)

paused = True
generation = 0


def count_neighbors(x, y):
    count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx = (x + dx) % GRID_WIDTH
            ny = (y + dy) % GRID_HEIGHT
            if grid[ny][nx]:
                count += 1
    return count


def update_game():
    global grid, generation
    new_grid = [[False] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            neighbors = count_neighbors(x, y)
            alive = grid[y][x]

            if alive and neighbors in [2, 3]:
                new_grid[y][x] = True
            elif not alive and neighbors == 3:
                new_grid[y][x] = True

    grid = new_grid
    generation += 1

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            cells[y][x].visible = grid[y][x]


@on_tick
def main():
    if not paused:
        update_game()


@on_press("space")
def toggle_pause():
    global paused
    paused = not paused


@on_press("r")
def reset():
    global grid, paused, generation
    paused = False
    generation = 0
    grid = [
        [
            random.choice([True, False]) if random.random() < 0.3 else False
            for _ in range(GRID_WIDTH)
        ]
        for _ in range(GRID_HEIGHT)
    ]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            cells[y][x].visible = grid[y][x]


@on_click
def manual_toggle():
    global grid
    x = mouse.x // CELL_SIZE
    y = mouse.y // CELL_SIZE
    if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
        grid[y][x] = not grid[y][x]
        cells[y][x].visible = grid[y][x]


set_bg("#000000")
run(
    width=GRID_WIDTH * CELL_SIZE,
    height=GRID_HEIGHT * CELL_SIZE,
    caption="Conway's Game of Life - Space: Pause/Play | R: Reset | Click: Toggle Cell",
)
