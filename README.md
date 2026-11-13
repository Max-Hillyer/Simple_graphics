[![PyPI](https://img.shields.io/pypi/v/simple-graphics-lib)](https://pypi.org/project/simple-graphics-lib/) [![Static Badge](https://img.shields.io/badge/project-site-blue)](https://max-hillyer.github.io/Simple_graphics) 
# Simple Graphics
Simple Graphics is a lightweight Python graphics package that offers a more readable alternative to Pygame.

Simple Graphics is designed to be easy to read, allowing you to focus on your code's logic instead of graphics implementation details.

## Installation
### pip
```bash
pip install simple-graphics-lib
```

## Quick Start
```python
import simple_graphics as sg

# Create shapes
rect = sg.Rect(50, 50, 100, 100, color="blue")
circle = sg.Circle(200, 200, radius=50, color="red")

# Define event handlers
@sg.on_click(rect)
def on_rect_click():
    print("Rectangle clicked!")

@sg.on_press("space")
def on_space_press():
    print("Space pressed!")

# Run the window
run(width=400, height=400, caption="My Graphics App")
```

## Shapes

Simple Graphics supports various shapes that automatically appear on the screen when defined.

---
### Rect 
Arguments: 
| Argument | Type | Role | Default | 
| :--- | :---: | :---: | ---: | 
| x | int | The x position of the rect | None | 
| y | int | The y position of the rect | None | 
| width | int | the width of the rect | 10 | 
| height | int | the height of the rect | 10 |
| color | str | the color of the rect | "black" | 
| outline | bool | whether the rect is just an outline | False | 
| draggable | bool | whether the rect can be dragged | False | 
| visible | bool | whether the rect is drawn on screen | True | 

Methods: 
| Method | Purpose | Arguments | Returns | 
| :--- | :---: | :---: | ---: |
| is_over | determines if a point is in the rectangle | x: int, y:int | bool | 
| get_area | returns the area of the rectangle| None | int | 
| get_perimeter | returns the perimeter of the rectangle | None | int | 
| rotate | rotates the rectangle by an angle in degrees | angle: int | None |

### Circle
Arguments: 
| Argument | Type | Role | Default | 
| :--- | :---: | :---: | ---: |
| x | int | the x position of the circle | None | 
| y | int | the y position of the circle | None | 
| radius | int | the radius of the circle | 10 |
| color | str | the color of the circle | "black" | 
| outline | bool | whether the circle is just an outline | False | 
| draggable | bool | whether the circle can be dragged | False | 
| visible | bool | whether the circle is drawn on screen | True | 

Methods: 
| Method | Purpose | Arguments | Returns | 
| :--- | :---: | :---: | ---: | 
| is_over | determines if a point is in the circle | x: int, y:int | bool |
| get_area | returns the area of the circle | None | int | 

### Polygon 
Arguments: 
| Argument | Type | Role | Default | 
| :--- | :---: | :---: | ---: |
| points | list[tuple] | the vertices of the polygon | None | 
| color | str | the color of the polygon | "black" | 
| outline | bool | whther the polygon is just an outline | False | 
| draggable | bool | whether the polygon can be dragged | False | 
| visible | bool | whether the polygon is drawn on screen | True | 

Methods: 
| Method | Purpose | Arguments | Returns | 
| :--- | :---: | :---: | ---: | 
| is_over | determines if a point is in the polygon | x: int, y:int | bool |
| rotate | rotates the polygon by an angle in degrees, optionally around a point | angle: int, around: tuple | None |

### Line
Arguments: 
| Argument | Type | Role | Default | 
| :--- | :---: | :---: | ---: |
| points | list[tuple] |the points that the line will connect | None |
| width | int | the width of the line | 10 | 
| color | str | the color of the line | "black" | 
| draggable | bool | whether the line can be dragged | False | 
| visible | bool | whether the line is drawn on screen | True | 

Methods: 
| Method | Purpose | Arguments | Returns | 
| :--- | :---: | :---: | ---: | 
| is_over | determines if a point is over the line | x: int, y:int | bool |
| rotate | rotates the line by an angle in degrees, optionally around a point | angle: int, around: tuple | None |

### Text 
Note: A text alignment method is currently in development and will be available in a future release.

Arguments:
| Argument | Type | Role | Default | 
| :--- | :---: | :---: | ---: |
| x | int | the x value of the upper left corner of the text | None | 
| y | int | the y value of the upper left corner of the text | None | 
| text | str | the text of the text | None | 
| color | str | the color of the text | "black" | 
| size | int | the size of the text | 36 | 
| draggable | bool | whether the text can be dragged | False | 
| visible | bool | whether the text is drawn on screen | True | 

Methods: 
| Method | Purpose | Arguments | Returns | 
| :--- | :---: | :---: | ---: | 
| is_over | determines if a point is in the text | x: int, y:int | bool |

### Image
Arguments:
| Argument | Type | Role | Default | 
| :--- | :---: | :---: | ---: |
| x | int | the x value of the image | None | 
| y | int | the y value of the image | None | 
| img_path | str | the path to the image | None |
| width | int | the width of the image | the width from the image path | 
| height | int | the height of the image | the height from the image path | 
| draggable | bool | whether the image can be dragged | False | 
| visible | bool | whether the image is drawn on screen | True | 

Methods: 
| Method | Purpose | Arguments | Returns | 
| :--- | :---: | :---: | ---: | 
| is_over | determines if a point is in the image | x: int, y:int | bool |
| rotate | rotates the image by an angle in degrees | angle: int | None |

## Rotation

Shapes that support rotation use `rotate(angle)`, where `angle` is measured in degrees. Each call adds to the current rotation. Rectangles and images rotate around their center by default. Polygons and lines can optionally rotate around a specific `(x, y)` point.

```python
rect = Rect(100, 100, 80, 40, color="blue")
polygon = Polygon([(200, 100), (250, 150), (200, 200)], color="red")
line = Line([(50, 50), (100, 50)], width=5)

rect.rotate(45)
polygon.rotate(30)
line.rotate(90, around=(75, 50))
```

### Group
`Group` combines multiple objects so you can treat them as one shape, modify their position and color, and check collisions for all the shapes in the group at once.

The following code creates a group containing two rectangles.
```python
r1 = Rect(20, 20)
r2 = Rect(40, 40)
group = Group(r1, r2)

group.x += 10
group.y -= 10
group.color = "green"
```

Arguments:
| Argument | Type | Role | Default | 
| :--- | :---: | :---: | ---: |
| *shapes | list[Shape] | the shapes to group | None | 
| visible | bool | whether shapes in group are drawn on screen | True |

Methods:
| Method | Purpose | Arguments | Returns | 
| :--- | :---: | :---: | ---: | 
| add | appends shapes to the group | *shapes | None | 
| remove | removes shapes from the group | *shapes | None | 
| clear | clears the group | None | None | 
| is_over | checks if a point is over the group | x, y | bool | 

Examples: 
```python
r1 = Rect(20, 20)
r2 = Rect(40, 40)
group = Group(r1, r2)

c1 = Circle(100,100)
t1 = Text(300, 300, "hi")
group.add(c1, t1)

group.remove(r2, t1)
```
---

## Run 
`run()` is the main Simple Graphics function.
It creates a screen where all defined objects appear and can be interacted with.

Arguments:
| Argument | Type | Role | Default | 
| :--- | :---: | :---: | ---: | 
| width | int | The screen width in pixels | 200 | 
| height | int | the screen height in pixels | 200 | 
| resizable | bool | whether or not the screen is resizable via dragging | True | 
| caption | str | the name of the graphics window | "SG window" | 
| fps | int | the frames per second of the game | 60 | 


## Collisions 

To check whether all supplied shapes overlap, use the `is_colliding()` function:
```python 
rect1 = Rect(10, 10)
ball = Circle(10 , 5)
print(is_colliding(ball, rect1)) # True

rect2 = Rect(10, 10)
print(is_colliding(ball, rect1, rect2)) # True only if every pair overlaps
```
---
## Events 

Instead of a `for` loop, Simple Graphics handles events using decorators.
### on_tick 
The `on_tick` decorator runs the function every frame, or every specified number of frames.
The default frame rate is 60 FPS.
Functions decorated with `on_tick` may not take arguments.
```python
@on_tick #runs every frame
def main(): 
    pass

@on_tick(3) #runs every 3 frames
def every3():
    pass
run()
```

### on_press 

The `on_press` decorator runs the function whenever a specified key is pressed, or whenever any key is pressed if no key is specified.

The following function runs whenever `w` or `s` is pressed.
```python
@on_press("w,s")
def do_w():
    do_soemthing() 

run()
```

The following function runs whenever any key is pressed.
```python
@on_press
def any_key():
    do_something()

run()
```

Functions decorated with `@on_press` may take at most one argument, which receives the pressed key.
```python
@on_press 
def print_key(key):
    print(key)

run()
```

Key names are case-insensitive. Common supported names include:

| Key | Name |
| --- | --- |
| Arrow keys | `"left"`, `"right"`, `"up"`, `"down"` |
| Other keys | `"space"`, `"enter"`, `"escape"`, `"tab"`, `"backspace"` |
| Letters and numbers | `"a"` through `"z"`, `"0"` through `"9"` |

For example, use the following to respond to arrow-key input:
```python
@on_press("left")
def move_left():
    print("Left arrow pressed")

@on_hold("right")
def move_right():
    print("Right arrow is being held")

run()
```

### on_hold

The `on_hold` decorator works like `on_press`, but runs the function every frame while the key is held instead of only once.

The following function runs as long as `w` or `s` is held.
```python
@on_hold("w,s")
def do_w():
    do_soemthing() 

run()
```

The following function runs while any key is held.
```python
@on_press
def any_key():
    do_something()

run()
```

Functions decorated with `@on_hold` may take at most one argument, which receives the held key.
```python
@on_press 
def print_key(key):
    print(key)

run()
```

### on_click

Functions decorated with `on_click` run whenever the specified object is clicked, or whenever any click is detected if no object is specified.

The following function runs whenever the button rectangle is clicked.
```python
button = Rect(10, 10)
@on_click(button)
def click_button():
    print("button clicked")

run()
```

The following function runs whenever a click occurs.

```python
@on_click
def print_click():
    print("clicked!")

run()
```

### on_hover
Functions decorated with `@on_hover` run whenever the pointer is over the specified object.

The following function runs whenever the mouse is over the rectangle.
```python
r1 = Rect(200,200, 100, 100)

@on_hover(r1)
def p():
    print("hovering")

run(400,400)
```

### on_drag
Functions decorated with `@on_drag` run whenever the specified object is being dragged.

The following function runs whenever the `r1` rectangle is dragged.
```python
r1 = Rect(200,200,draggable = True)

@on_drag(r1)
def do_something():
    print("dragging r1")

run(400,400)
```
---
## The mouse
A mouse object is initialized automatically when you import Simple Graphics.

To get the mouse coordinates, use `mouse.x` and `mouse.y`.

Example:
```python
@on_tick
def main():
    print(mouse.x, mouse.y)

run()
```

## dragging 

To make a shape draggable, set the `draggable` keyword argument when initializing the object:
```python
r = Rect(250,250, draggable = True)
```
This works for all shapes, including images and text.

---
## Miscellaneous Functions

### set_bg
`set_bg()` sets the background to the specified color.

The default background color is white.
```python
set_bg("black")
``` 
changes the background color to black

### clear_screen
`clear_screen()` clears the screen.
Objects defined before the screen is cleared can no longer be interacted with.

### erase
`erase()` deletes a single object.
Erased objects can no longer be interacted with.

### gamestate object
Instead of using the `global` keyword at the top of your functions, you can assign variables as attributes of the `game` object.
```python
game.x = 10

@on_tick
def main():
    game.x += 1
```
Either approach works.
