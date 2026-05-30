import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
from inspect import signature, currentframe
from math import pi, cos, sin, radians
from typing import Callable

_shapes = []
_ontick = {}
_key_funcs = {}
_key_hold_funcs = {}
_mouse_click_funcs = {}
_hover_funcs = {}
_dragging_funcs = {}
_dragging_shape = None
_bgcolor = "white"
_font = "Arial"

pygame.init()


class GameState:
    def __init__(self):
        self._state = {}

    def __setattr__(self, name, value):
        if name == "_state":
            super().__setattr__(name, value)
        else:
            self._state[name] = value

    def __getattr__(self, name):
        if name == "_state":
            return super().__getattribute__(name)
        return self._state.get(name, None)

    def __repr__(self):
        return f"GameState({self._state})"


game = GameState()


class Mouse:
    def __init__(self, hiding=False):
        self.hiding = hiding

    @property
    def x(self):
        return pygame.mouse.get_pos()[0]

    @property
    def y(self):
        return pygame.mouse.get_pos()[1]

    def set_hiding(self, state: bool):
        """Sets the mouse visibility"""
        self.hiding = state
        pygame.mouse.set_visible(self.hiding)


mouse = Mouse()


class Shape:
    """Base class for all drawable shapes. Do not instantiate directly."""

    def __init__(
        self, x, y, color="black", outline=False, draggable=False, visible=True
    ):
        """Initialize a shape at position (x, y).

        Args:
            x: X coordinate (pixels from left)
            y: Y coordinate (pixels from top)
            color: Color as hex string (#RRGGBB) or name (default: "black")
            outline: If True, draw outline only; if False, fill shape (default: False)
            draggable: If True, shape can be moved by mouse (default: False)
        """
        self.x = x
        self.y = y
        self.color = color
        self.outline = int(outline)
        self.draggable = draggable
        self.visible = visible
        _shapes.append(self)

    def __str__(self):
        """Return string representation showing shape type and parameters"""
        class_name = self.__class__.__name__.lower()
        sig = signature(self.__init__)
        params = [p for p in sig.parameters if p != "self"]

        values = {}
        for p in params:
            if hasattr(self, p):
                values[p] = getattr(self, p)
        return f"{class_name}: {values}"

    def rotate(self, angle):
        self.angle += angle
        self.angle %= 360


class Rect(Shape):
    def __init__(
        self,
        x: int,
        y: int,
        width: int = 10,
        height: int = 10,
        color: str = "black",
        outline: bool = False,
        draggable: bool = False,
        visible: bool = True,
    ):
        super().__init__(x, y, color, outline, draggable, visible)
        self.width = width
        self.height = height
        self.angle = 0

    @property
    def rect(self):
        return (self.x, self.y, self.width, self.height)

    def is_obj_over(self, ox=None, oy=None):
        """Check if a point is inside this rectangle.

        Args:
            ox: X coordinate (default: current mouse x)
            oy: Y coordinate (default: current mouse y)

        Returns:
            bool: True if point is inside rectangle, False otherwise
        """
        if ox == None:
            ox = pygame.mouse.get_pos()[0]
        if oy == None:
            oy = pygame.mouse.get_pos()[1]
        x_over = ox > self.x and ox < self.x + self.width
        y_over = oy > self.y and oy < self.y + self.height
        return x_over and y_over

    def get_area(self):
        """Calculate and return the area of the rectangle"""
        return self.width * self.height

    def get_perimeter(self):
        """Calculate and return the perimeter of the rectangle"""
        return (2 * self.width) + (2 * self.height)


class Circle(Shape):
    def __init__(
        self,
        x: int,
        y: int,
        radius: int = 10,
        color: str = "black",
        outline: bool = False,
        draggable: bool = False,
        visible: bool = True,
    ):
        super().__init__(x, y, color, outline, draggable, visible)
        self.radius = radius
        self.angle = 0  # this is useless but whatever

    def is_obj_over(self, ox=None, oy=None):
        """Check if a point is inside this circle.

        Args:
            ox: X coordinate (default: current mouse x)
            oy: Y coordinate (default: current mouse y)

        Returns:
            bool: True if point is inside circle, False otherwise
        """
        if ox == None:
            ox = pygame.mouse.get_pos()[0]
        if oy == None:
            oy = pygame.mouse.get_pos()[1]
        inside = (ox - self.x) ** 2 + (oy - self.y) ** 2 < self.radius**2
        return inside

    def get_area(self):
        """Calculate and return the area of the circle."""
        return pi * self.radius**2


class Polygon(Shape):
    def __init__(
        self,
        points: list[tuple],
        color: str = "black",
        outline: bool = False,
        draggable: bool = False,
        visible: bool = True,
    ):
        self.color = color
        self.points = points
        self.outline = int(outline)
        self.draggable = draggable
        self.visible = visible
        self._angle = 0
        self.original_points = list(points)
        self.around = None
        _shapes.append(self)

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value
        self._apply_rotation()

    def is_obj_over(self, ox=None, oy=None):
        """Check if a point is inside this polygon using ray casting algorithm.

        Args:
            ox: X coordinate (default: current mouse x)
            oy: Y coordinate (default: current mouse y)

        Returns:
            bool: True if point is inside polygon, False otherwise
        """
        if ox == None:
            ox = pygame.mouse.get_pos()[0]
        if oy == None:
            oy = pygame.mouse.get_pos()[1]

        n = len(self.points)
        inside = False

        p1x, p1y = self.points[0]
        for i in range(n + 1):
            p2x, p2y = self.points[i % n]
            if oy > min(p1y, p2y):
                if oy <= max(p1y, p2y):
                    if ox <= max(p1x, p2x):
                        if p1y != p2y:
                            xints = (oy - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or ox <= xints:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def get_center(self):
        """Calculate and return the center (centroid) of the polygon.

        Returns:
            tuple: (center_x, center_y) coordinates of the polygon's centroid
        """
        if not self.points:
            return (0, 0)

        avg_x = sum(point[0] for point in self.original_points) / len(
            self.original_points
        )
        avg_y = sum(point[1] for point in self.original_points) / len(
            self.original_points
        )
        return (avg_x, avg_y)

    def _apply_rotation(self):
        angle_rad = radians(self._angle)
        if self.around == None:
            cx, cy = self.get_center()
        else:
            cx, cy = self.around
        newpoints = []
        for x, y in self.original_points:
            newx = cos(angle_rad) * (x - cx) - sin(angle_rad) * (y - cy) + cx
            newy = sin(angle_rad) * (x - cx) + cos(angle_rad) * (y - cy) + cy
            newpoints.append((newx, newy))
        self.points = newpoints

    def rotate(self, angle, around=None):
        """Rotate the polygon

        Args:
            angle: how much to rotate the polygon
            around: the point to rotate the polygon around, defaults to the middle of the polygon

        """
        self.around = around
        self.angle += angle


class Line(Shape):
    def __init__(
        self,
        points: list[tuple],
        width: int = 10,
        color: str = "black",
        draggable: bool = False,
        visible: bool = True,
    ):
        self.color = color
        self.points = points
        self.width = width
        self.draggable = draggable
        self.visible = visible
        self.angle = 0
        _shapes.append(self)

    def is_obj_over(self, ox=None, oy=None):
        """Check if a point is near this line (within line width).

        Args:
            ox: X coordinate (default: current mouse x)
            oy: Y coordinate (default: current mouse y)

        Returns:
            bool: True if point is within line width, False otherwise
        """
        if ox == None:
            ox = pygame.mouse.get_pos()[0]
        if oy == None:
            oy = pygame.mouse.get_pos()[1]

        for i in range(len(self.points) - 1):
            x1, y1 = self.points[i]
            x2, y2 = self.points[i + 1]

            dist = self._distance_to_segment(ox, oy, x1, y1, x2, y2)

            if dist <= self.width / 2:
                return True

        return False

    def _distance_to_segment(self, px, py, x1, y1, x2, y2):
        """Calculate shortest distance from a point to a line segment."""
        dx = x2 - x1
        dy = y2 - y1

        if dx == 0 and dy == 0:
            return ((px - x1) ** 2 + (py - y1) ** 2) ** 0.5

        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))

        closest_x = x1 + t * dx
        closest_y = y1 + t * dy

        return ((px - closest_x) ** 2 + (py - closest_y) ** 2) ** 0.5

    def rotate(self, angle, around=None):
        """Rotate the line by angle degrees around a point.

        Args:
            angle: Rotation angle in degrees
            around: Point to rotate around (tuple of x, y). If None, rotates around center.
        """
        if around is None:
            avg_x = sum(p[0] for p in self.points) / len(self.points)
            avg_y = sum(p[1] for p in self.points) / len(self.points)
            around = (avg_x, avg_y)

        self.angle += angle
        angle_rad = radians(angle)
        cx, cy = around

        new_points = []
        for x, y in self.points:
            newx = cos(angle_rad) * (x - cx) - sin(angle_rad) * (y - cy) + cx
            newy = sin(angle_rad) * (x - cx) + cos(angle_rad) * (y - cy) + cy
            new_points.append((newx, newy))

        self.points = new_points


class Image(Shape):
    def __init__(
        self,
        x: int,
        y: int,
        img_path: str,
        width: int = None,
        height: int = None,
        draggable: bool = False,
        visible: bool = True,
    ):
        super().__init__(x, y, draggable, visible)
        self.img_path = img_path
        self.original_img = pygame.image.load(self.img_path)

        img_width, img_height = self.original_img.get_size()
        self.width = width if width is not None else img_width
        self.height = height if height is not None else img_height

        self.surface = pygame.transform.scale(
            self.original_img, (self.width, self.height)
        )

    def is_obj_over(self, ox=None, oy=None):
        """Check if a point is inside this image rectangle.

        Args:
            ox: X coordinate (default: current mouse x)
            oy: Y coordinate (default: current mouse y)

        Returns:
            bool: True if point is inside image bounds, False otherwise
        """
        if ox is None:
            ox = pygame.mouse.get_pos()[0]
        if oy is None:
            oy = pygame.mouse.get_pos()[1]

        x_over = ox > self.x and ox < self.x + self.width
        y_over = oy > self.y and oy < self.y + self.height
        return x_over and y_over


class Text(Shape):
    def __init__(
        self,
        x: int,
        y: int,
        text: str,
        color: str = "black",
        font=_font,
        size: int = 36,
        draggable: bool = False,
        visible: bool = True,
    ):
        super().__init__(x, y, color, False, draggable, visible)
        self.text = text
        self.size = size
        self.font = pygame.font.SysFont(font, size)

    @property
    def txtsurf(self):
        """Render and return the text surface for drawing on screen."""
        return self.font.render(str(self.text), True, self.color)

    def is_obj_over(self, ox=None, oy=None):
        """Check if a point is inside this text's bounding box.

        Args:
            ox: X coordinate (default: current mouse x)
            oy: Y coordinate (default: current mouse y)

        Returns:
            bool: True if point is inside text bounds, False otherwise
        """
        if ox == None:
            ox = pygame.mouse.get_pos()[0]
        if oy == None:
            oy = pygame.mouse.get_pos()[1]

        text_width = self.txtsurf.get_width()
        text_height = self.txtsurf.get_height()

        x_over = ox > self.x and ox < self.x + text_width
        y_over = oy > self.y and oy < self.y + text_height
        return x_over and y_over


class Group:
    """Container for grouping multiple shapes for batch operations.

    Allows moving, coloring, and interacting with multiple shapes as one unit.
    Implements the full Python container protocol (__len__, __iter__, etc.).
    """

    def __init__(self, *shapes: list[Shape], visible: bool = True):
        """Initialize group with optional initial shapes.

        Args:
            *shapes: Variable number of Shape objects to add initially
        """
        self.grouped = []
        self.add(*shapes)

    @property
    def color(self):
        return self._color if hasattr(self, "_color") else None

    @color.setter
    def color(self, color):
        self._color = color
        for shape in self.grouped:
            if hasattr(shape, "color"):
                shape.color = color

    @property
    def x(self):
        if not self.grouped:
            return 0
        return self.grouped[0].x

    @x.setter
    def x(self, value):
        delta = value - self.x
        for child in self.grouped:
            child.x += delta

    @property
    def y(self):
        if not self.grouped:
            return 0
        return self.grouped[0].x

    @y.setter
    def y(self, value):
        delta = value - self.y
        for child in self.grouped:
            child.y += delta

    def __getitem__(self, key):
        return self.grouped[key]

    def __len__(self):
        return len(self.grouped)

    def __iter__(self):
        return iter(self.grouped)

    def __contains__(self, item):
        return item in self.grouped

    def __setitem__(self, key, value):
        self.grouped[key] = value

    def __delitem__(self, key):
        del self.grouped[key]

    def add(self, *shapes):
        """Add one or more shapes to the group.

        Args:
            *shapes: One or more Shape objects to add

        Raises:
            TypeError: If any argument is not a Shape
        """
        for s in shapes:
            if not isinstance(s, Shape):
                raise TypeError(f"{s} must be Shape")
            self.grouped.append(s)

    def remove(self, *shapes):
        """Remove one or more shapes from the group.

        Args:
            *shapes: One or more Shape objects to remove
        """
        for s in shapes:
            self.grouped.remove(s)
            _shapes.remove(s)

    def clear(self):
        """Remove all shapes from the group."""
        self.grouped.clear()

    def is_obj_over(self, x, y):
        """Check if any shape in group contains the point.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            bool: True if any child shape contains point, False otherwise
        """
        for i in self.grouped:
            if i.is_obj_over(x, y):
                return True
        return False

    def __repr__(self):
        shapes_str = ", ".join(str(s) for s in self.grouped)
        return f"Group([{shapes_str}])"


class CollisionManager:
    """Static utility class containing collision detection for all shape combinations."""

    @staticmethod
    def rect_rect(rect1: Rect, rect2: Rect):
        """Check if two rectangles are colliding."""
        for rect in [rect1, rect2]:
            corners = [
                (rect.x, rect.y),
                (rect.x + rect.width, rect.y),
                (rect.x, rect.y + rect.height),
                (rect.x + rect.width, rect.y + rect.height),
            ]
            for other in [rect1, rect2]:
                if other is rect:
                    continue
                for point in corners:
                    if other.is_obj_over(*point):
                        return True
        return False

    @staticmethod
    def rect_circle(rect: Rect, circle: Circle):
        """Check if a rectangle and circle are colliding."""
        closest_x = max(rect.x, min(circle.x, rect.x + rect.width))
        closest_y = max(rect.y, min(circle.y, rect.y + rect.height))
        dist = ((circle.x - closest_x) ** 2 + (circle.y - closest_y) ** 2) ** 0.5
        return dist < circle.radius

    @staticmethod
    def circle_circle(circle1: Circle, circle2: Circle):
        """Check if two circles are colliding."""
        dist = ((circle1.x - circle2.x) ** 2 + (circle1.y - circle2.y) ** 2) ** 0.5
        return dist < circle1.radius + circle2.radius

    @staticmethod
    def rect_polygon(rect: Rect, polygon: Polygon):
        """Check if a rectangle and polygon are colliding."""
        corners = [
            (rect.x, rect.y),
            (rect.x + rect.width, rect.y),
            (rect.x, rect.y + rect.height),
            (rect.x + rect.width, rect.y + rect.height),
        ]
        for cx, cy in corners:
            if polygon.is_obj_over(cx, cy):
                return True
        for px, py in polygon.points:
            if rect.is_obj_over(px, py):
                return True
        return False

    @staticmethod
    def circle_polygon(circle: Circle, polygon: Polygon):
        """Check if a circle and polygon are colliding."""
        if polygon.is_obj_over(circle.x, circle.y):
            return True
        for px, py in polygon.points:
            dist = ((circle.x - px) ** 2 + (circle.y - py) ** 2) ** 0.5
            if dist < circle.radius:
                return True
        return False

    @staticmethod
    def rect_text(rect, text):
        """Check if a rectangle and text are colliding."""
        text_width = text.txtsurf.get_width()
        text_height = text.txtsurf.get_height()
        return pygame.Rect(*rect.rect).colliderect(
            pygame.Rect(text.x, text.y, text_width, text_height)
        )

    @staticmethod
    def circle_text(circle, text):
        """Check if a circle and text are colliding."""
        text_width = text.txtsurf.get_width()
        text_height = text.txtsurf.get_height()
        closest_x = max(text.x, min(circle.x, text.x + text_width))
        closest_y = max(text.y, min(circle.y, text.y + text_height))
        dist = ((circle.x - closest_x) ** 2 + (circle.y - closest_y) ** 2) ** 0.5
        return dist < circle.radius

    @staticmethod
    def rect_image(rect, image):
        """Check if a rectangle and image are colliding."""
        return pygame.Rect(*rect.rect).colliderect(
            pygame.Rect(image.x, image.y, image.width, image.height)
        )

    @staticmethod
    def circle_image(circle, image):
        """Check if a circle and image are colliding."""
        closest_x = max(image.x, min(circle.x, image.x + image.width))
        closest_y = max(image.y, min(circle.y, image.y + image.height))
        dist = ((circle.x - closest_x) ** 2 + (circle.y - closest_y) ** 2) ** 0.5
        return dist < circle.radius

    @staticmethod
    def groupcollision(group, shape):
        """Check if a group and any shape are colliding."""
        for child in group.grouped:
            if is_colliding(child, shape):
                return True
        return False

    def no_collsion_method(shape1, shape2):
        raise Exception(f"{type(shape1)} and {type(shape2)} have no collision method")


def check_args(func, name):
    """Validate that a decorator function takes no arguments.

    Args:
        func: The function to validate
        name: Name of the decorator (for error messages)

    Raises:
        ValueError: If function has any parameters
    """
    sig = signature(func)
    param_names = list(sig.parameters)
    if str(sig) != "()":
        raise ValueError(
            f'Functions defined with the @{name} decorator may not take arguments\n but "{func.__name__}" was defined with {param_names}'
        )


# decorartors like this get weird: if you want to be able to pass arguments in you need to handle 2 cases
# if theres no arguments then it just takes the function as the argument
def on_tick(target: Callable | int):
    """Decorator: call function every frame (60 times per second).

    Usage:
        @on_tick
        def update():
            pass  # Runs every frame

        @on_tick(n) #run every n ticks
        def every_n(): pass
    """
    if callable(target):
        func = target
        name = currentframe().f_code.co_name
        check_args(func, name)
        _ontick[None] = func
        return func
    else:

        def decorator(func):
            name = currentframe().f_code.co_name
            check_args(func, name)
            _ontick[target] = func
            return func

        return decorator


def on_press(target: Callable | str):
    """Decorator: call function when a key is pressed.

    Usage:
        @on_press  # Any key
        def any_key(): pass

        @on_press("space, enter")  # Specific keys
        def special(): pass
    """
    if callable(target):
        func = target
        name = currentframe().f_code.co_name
        sig = signature(func)
        param_names = list(sig.parameters)
        if len(param_names) not in [0, 1]:
            raise ValueError(
                f'Functions defined with the @{name} decorator may take 0 or 1 arguments\n but "{func.__name__}" was defined with {param_names}'
            )
        func._accepts_key = len(param_names) == 1
        _key_funcs[None] = func
        return func

    else:

        def decorator(func):
            key = target
            name = currentframe().f_code.co_name
            sig = signature(func)
            param_names = list(sig.parameters)
            if len(param_names) not in [0, 1]:
                raise ValueError(
                    f'Functions defined with the @{name} decorator may take 0 or 1 arguments\n but "{func.__name__}" was defined with {param_names}'
                )
            func._accepts_key = len(param_names) == 1

            keys = [k.strip() for k in key.split(",")]
            for k in keys:
                key_name = k if len(k) == 1 else k.upper()
                pygame_key = getattr(pygame, f"K_{key_name}")
                _key_funcs[pygame_key] = func
            return func

        return decorator


def on_hold(target: Callable | str):
    """Decorator: call function every frame while a key is held down.

    Usage:
        @on_hold("w")
        def move_up():
            pass  # Runs each frame while 'w' is held
    """
    if callable(target):
        func = target
        name = currentframe().f_code.co_name
        sig = signature(func)
        param_names = list(sig.parameters)
        if len(param_names) not in [0, 1]:
            raise ValueError(
                f'Functions defined with the @{name} decorator may take 0 or 1 arguments\n but "{func.__name__}" was defined with {param_names}'
            )
        func._accepts_key = len(param_names) == 1
        _key_hold_funcs[None] = func
        return func

    else:

        def decorator(func):
            key = target
            name = currentframe().f_code.co_name
            sig = signature(func)
            param_names = list(sig.parameters)
            if len(param_names) not in [0, 1]:
                raise ValueError(
                    f'Functions defined with the @{name} decorator may take 0 or 1 arguments\n but "{func.__name__}" was defined with {param_names}'
                )
            func._accepts_key = len(param_names) == 1

            keys = [k.strip() for k in key.split(",")]
            for k in keys:
                key_name = k if len(k) == 1 else k.upper()
                pygame_key = getattr(pygame, f"K_{key_name}")
                _key_hold_funcs[pygame_key] = func
            return func

        return decorator


def on_click(target: Callable | Shape):
    """Decorator: call function when mouse is clicked.

    Usage:
        @on_click  # Any click
        def click(): pass

        @on_click(my_shape)  # Click on specific shape
        def shape_click(): pass
    """
    if callable(target):
        name = currentframe().f_code.co_name
        check_args(target, name)
        _mouse_click_funcs[None] = target
        return target
    else:

        def decorator(func):
            name = currentframe().f_code.co_name
            check_args(func, name)
            _mouse_click_funcs[target] = func
            return func

        return decorator


def on_hover(shape: Shape):
    """Decorator: call function every frame mouse hovers over a shape.

    Usage:
        @on_hover(my_circle)
        def hover(): pass
    """

    def decorator(func: Callable):
        name = currentframe().f_code.co_name
        check_args(func, name)
        _hover_funcs[shape] = func
        return func

    return decorator


def on_drag(shape: Shape):
    """Decorator: call function every frame a draggable shape is being dragged.

    Usage:
        @on_drag(my_rect)
        def dragging(): pass
    """

    def decorator(func: Callable):
        name = currentframe().f_code.co_name
        check_args(func, name)
        _dragging_funcs[shape] = func
        return func

    return decorator


def set_bg(color: str):
    """Set the background color of the window.

    Args:
        color: Color as hex string (#RRGGBB) or name (e.g., 'white', 'red')
    """
    global _bgcolor
    _bgcolor = color


def clear_screen():
    """Remove all shapes from the screen."""
    _shapes.clear()


def erase(obj):
    """Remove a specific shape from the screen.

    Args:
        obj: The shape object to remove
    """
    _shapes.remove(obj)


def is_colliding(shape1: Shape, shape2: Shape) -> bool:
    """Check if two shapes are colliding.

    Args:
        shape1: First shape
        shape2: Second shape

    Returns:
        bool: True if shapes overlap, False otherwise
    """
    shapeName1 = shape1.__class__.__name__.lower()
    shapeName2 = shape2.__class__.__name__.lower()
    if "group" == shapeName1 or "group" == shapeName2:
        method_name = "groupcollision"
        method = getattr(CollisionManager, method_name, None)
        return method(shape1, shape2)
    method_name = f"{shapeName1}_{shapeName2}"
    method = getattr(CollisionManager, method_name, None)
    if method is None:
        method_name = f"{shapeName2}_{shapeName1}"
        method = getattr(CollisionManager, method_name, None)
        if method is None:
            raise Exception(
                f"{type(shape1).__name__} and {type(shape2).__name__} have no collision method"
            )
        return method(shape2, shape1)
    return method(shape1, shape2)


def run(
    width: int = 200,
    height: int = 200,
    resizable: bool = True,
    fps: int = 60,
    caption: str = "SG window",
):
    """Start the graphics window and begin the main game loop.

    This function blocks until the window is closed.

    Args:
        width: Window width in pixels (default: 200)
        height: Window height in pixels (default: 200)
        resizable: Whether the window can be resized by user (default: True)
        caption: Window title bar text (default: "SG window")
    """
    global _bgcolor
    ticks = 0
    if resizable:
        screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    else:
        screen = pygame.display.set_mode((width, height))

    pygame.display.set_caption(caption)
    clock = pygame.time.Clock()
    running = True

    def handle_events():
        nonlocal ticks
        nonlocal running
        global _dragging_shape

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if None in _key_funcs:
                    func = _key_funcs[None]
                    if hasattr(func, "_accepts_key") and func._accepts_key:
                        func(pygame.key.name(event.key))
                    else:
                        func()
                if event.key in _key_funcs.keys():
                    func = _key_funcs[event.key]
                    if hasattr(func, "_accepts_key") and func._accepts_key:
                        func(pygame.key.name(event.key))
                    else:
                        func()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if None in _mouse_click_funcs:
                    _mouse_click_funcs[None]()

                for shape in _shapes:
                    if shape.is_obj_over() and shape in _mouse_click_funcs:
                        _mouse_click_funcs[shape]()
                    if shape.draggable and shape.is_obj_over():
                        _dragging_shape = shape
                        break

            if event.type == pygame.MOUSEBUTTONUP:
                _dragging_shape = None

            def _move_shape(_dragging_shape):
                if _dragging_shape is not None:
                    if hasattr(_dragging_shape, "points"):
                        dx = mouse.x - _dragging_shape.points[0][0]
                        dy = mouse.y - _dragging_shape.points[0][1]
                        _dragging_shape.points = [
                            (p[0] + dx, p[1] + dy) for p in _dragging_shape.points
                        ]
                    else:
                        _dragging_shape.x = mouse.x
                        _dragging_shape.y = mouse.y
                        _dragging_funcs[_dragging_shape]()

            _move_shape(_dragging_shape)

        keys_pressed = pygame.key.get_pressed()
        for pygame_key, func in _key_hold_funcs.items():
            if pygame_key is None:
                if hasattr(func, "_accepts_key") and func._accepts_key:
                    func(pygame.key.name(event.key))
                else:
                    func()
            elif keys_pressed[pygame_key]:
                if hasattr(func, "_accepts_key") and func._accepts_key:
                    func(pygame.key.name(pygame_key))
                else:
                    func()
        for shape, func in _hover_funcs.items():
            if shape.is_obj_over(mouse.x, mouse.y):
                func()

        for every, func in _ontick.items():
            if every is None:
                func()
            else:
                if ticks % every == 0:
                    func()

    while running:
        ticks += 1
        handle_events()

        screen.fill(_bgcolor)

        for shape in _shapes:
            if not shape.visible:
                continue
            shapeName = shape.__class__.__name__.lower()
            if shapeName == "circle":
                pygame.draw.circle(
                    screen, shape.color, (shape.x, shape.y), shape.radius, shape.outline
                )
            elif shapeName == "rect":
                if shape.angle == 0:
                    pygame.draw.rect(
                        screen,
                        shape.color,
                        shape.rect,
                        shape.outline,
                    )
                else:
                    rect_surface = pygame.Surface(
                        (shape.width, shape.height), pygame.SRCALPHA
                    )
                    pygame.draw.rect(
                        rect_surface,
                        shape.color,
                        (0, 0, shape.width, shape.height),
                        shape.outline,
                    )
                    rotated_surface = pygame.transform.rotate(rect_surface, shape.angle)
                    rotated_rect = rotated_surface.get_rect(
                        center=(shape.x + shape.width // 2, shape.y + shape.height // 2)
                    )
                    screen.blit(rotated_surface, rotated_rect.topleft)

            elif shapeName == "polygon":
                pygame.draw.polygon(screen, shape.color, shape.points, shape.outline)
            elif shapeName == "line":
                for i in range(1, len(shape.points)):
                    pygame.draw.line(
                        screen,
                        shape.color,
                        shape.points[i - 1],
                        shape.points[i],
                        shape.width,
                    )
            elif shapeName == "text":
                screen.blit(shape.txtsurf, (shape.x, shape.y))
            elif shapeName == "image":
                screen.blit(shape.surface, (shape.x, shape.y))
            elif shapeName == "group":
                pass  # this stops weird edgecases while keeping good rendering

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
