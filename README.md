[![PyPI](https://img.shields.io/pypi/v/simple-graphics-lib)](https://pypi.org/project/simple-graphics-lib/)
# Simple Graphics
--- 
simple graphics is a lightweight python graphics package that offers a more readable alternative to pygame

simple graphics is meant to be extremely readable, allowing you to focus on the logic of your code instead of graphic specifics 

## Installation
### pip
```bash
pip install simple-graphics-lib
```

## Quick Start
```python
from simple_graphics import *

# Create shapes
rect = Rect(50, 50, 100, 100, color="blue")
circle = Circle(200, 200, radius=50, color="red")

# Define event handlers
@on_click(rect)
def on_rect_click():
    print("Rectangle clicked!")

@on_press("space")
def on_space_press():
    print("Space pressed!")

# Run the window
run(width=400, height=400, caption="My Graphics App")
```

## Shapes

Simple Graphics offers support for various shapes, that will automatically appear on the screen when defined

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
| is_obj_over | determines if a point is in the rectangle | x: int, y:int | bool | 
| get_area | returns the area of the rectangle| None | int | 
| get_perimeter | returns the perimeter of the rectangle | None | int | 

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
| is_obj_over | determines if a point is in the circle | x: int, y:int | bool |
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
| is_obj_over | determines if a point is in the polygon | x: int, y:int | bool |

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
| is_obj_over | determines if a point is over the line | x: int, y:int | bool |

### Text 
Arguments:
| Argument | Type | Role | Default | 
| :--- | :---: | :---: | ---: |
| x | int | the x value of the text | None | 
| y | int | the y value of the text | None | 
| text | str | the text of the text | None | 
| color | str | the color of the text | "black" | 
| size | int | the size of the text | 36 | 
| draggable | bool | whether the text can be dragged | False | 
| visible | bool | whether the text is drawn on screen | True | 

Methods: 
| Method | Purpose | Arguments | Returns | 
| :--- | :---: | :---: | ---: | 
| is_obj_over | determines if a point is in the text | x: int, y:int | bool |

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
| is_obj_over | determines if a point is in the image | x: int, y:int | bool |

### Group
Group groups a bunch of objects together, so you can treat them all as one shape, modifying x,y and color and checking for collisions for every shape in the group at once

the below code creates a group of two rectangles
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
| is_obj_over | checks if a point is over the group | x, y | bool | 

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
`run()` is Simple Graphics main function. 
it creates a screen where all defined objects appear and can be interacted with. 

Arguments:
| Argument | Type | Role | Default | 
| :--- | :---: | :---: | ---: | 
| width | int | The screen width in pixels | 200 | 
| height | int | the screen height in pixels | 200 | 
| resizable | bool | whether or not the screen is resizable via dragging | True | 
| caption | str | the name of the graphics window | "SG window" | 


## Collisions 

to check for a collision between 2 shapes, use the `is_colliding()` method: 
```python 
rect1 = Rect(10, 10)
ball = Circle(10 , 5)
print(is_colliding(ball, rect1)) # True
```
---
## Events 

Instead of a for loop, Simple Graphics handles events using decorators

### on_tick 
The `on_tick` decorator runs the function every frame
The default framerate is 60 FPS
Functions with the `on_tick` decorator may not take arguments
```python
@on_tick 
def main(): 
    do_something()

run()
```

### on_press 

the `on_press` runs the decorator whenever a specified button is pressed, or when any button is pressed if none are specified

The function below will run whenever w or s is pressed
```python
@on_press("w,s")
def do_w():
    do_soemthing() 

run()
```

The function below will run whenever any key is pressed 
```python
@on_press
def any_key():
    do_something()

run()
```

Functions with the `@on_press` decorator may only take 1 argument, which will show up as the key pressed
```python
@on_press 
def print_key(key):
    print(key)

run()
```

### on_hold

the `on_hold` decorator functions exactly like the `on_press` decorator, but the function runs every frame for as long as the key is held, instead of just once

The function below will run for as long as w or s is pressed
```python
@on_hold("w,s")
def do_w():
    do_soemthing() 

run()
```

The function below will run while any key is pressed 
```python
@on_press
def any_key():
    do_something()

run()
```

Functions with the `@on_hold` decorator may only take 1 argument, which will show up as the key held
```python
@on_press 
def print_key(key):
    print(key)

run()
```

### on_click

functions defined with the `on_click` decorator will run whenever the specified object is clicked, or whenever any click is detected if none is specified

the function below will run whenever the button rect is clicked
```python
button = Rect(10, 10)
@on_click(button)
def click_button():
    print("button clicked")

run()
```

the function below will run when there is any click at all

```python
@on_click
def print_click():
    print("clicked!")

run()
```

### on_hover
functions defined with the `@on_hover` decorator will run whenever the specified object is being hovered over

the function below will run whenever the mouse is over the rectangle 
```python
r1 = Rect(200,200, 100, 100)

@on_hover(r1)
def p():
    print("hovering")

run(400,400)
```

### on_drag
functions defined with the `@on_drag` decorator will run whenever the specified object is being dragged

the function below will run whenevr the r1 rect is being dragged
```python
r1 = Rect(200,200,draggable = True)

@on_drag(r1)
def do_something():
    print("dragging r1")

run(400,400)
```
---
## The mouse
A mouse object is already initialized in the Simple Graphics import 

to get mouse coordinates, simply use `mouse.x` and `mouse.y`

Example: 
```python
@on_tick
def main():
    print(mouse.x, mouse.y)

run()
```

## dragging 

to make a shape draggable, add the keyword argument to the object initialization: 
```python
r = Rect(250,250, draggable = True)
```
this works for all shapes including images and text

---
## Miscellaneous Functions

### set_bg
`set_bg()` simply sets the background to the specified color

the default background color is white
```python
set_bg("black")
``` 
changes the background color to black

### clear_screen
`clear_screen()` clears the screen. 
objects defined before a screen clear can no longer be interacted with

### erase
`erase()` deletes a single object
erased objects can no longer be invoked
