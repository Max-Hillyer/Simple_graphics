import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
from inspect import signature, currentframe
from math import pi
from typing import Callable

_shapes = []
_ontick = []
_key_funcs = {}
_key_hold_funcs = {}
_mouse_click_funcs = {}
_bgcolor = "white"
_font = "Arial"

pygame.init()


class Mouse:
    @property
    def x(self):
        return pygame.mouse.get_pos()[0]

    @property
    def y(self):
        return pygame.mouse.get_pos()[1]


mouse = Mouse()


class Shape:
    def __init__(self, x, y, color="black", outline=False):
        self.x = x
        self.y = y
        self.color = color
        self.outline = int(outline)
        _shapes.append(self)

    def __str__(self):
        return self.__class__.__name__.lower()


class Rect(Shape):
    def __init__(
        self,
        x: int,
        y: int,
        width: int = 10,
        height: int = 10,
        color: str = "black",
        outline: bool = False,
    ):
        super().__init__(x, y, color, outline)
        self.width = width
        self.height = height

    @property
    def rect(self):
        return (self.x, self.y, self.width, self.height)

    def is_obj_over(self, ox=None, oy=None):
        if ox == None:
            ox = pygame.mouse.get_pos()[0]
        if oy == None:
            oy = pygame.mouse.get_pos()[1]
        x_over = ox > self.x and ox < self.x + self.width
        y_over = oy > self.y and oy < self.y + self.height
        return x_over and y_over

    def get_area(self):
        return self.width * self.height

    def get_perimeter(self):
        return (2 * self.width) + (2 * self.height)


class Circle(Shape):
    def __init__(
        self,
        x: int,
        y: int,
        radius: int = 10,
        color: str = "black",
        outline: bool = False,
    ):
        super().__init__(x, y, color, outline)
        self.radius = radius

    def is_obj_over(self, ox=None, oy=None):
        if ox == None:
            ox = pygame.mouse.get_pos()[0]
        if oy == None:
            oy = pygame.mouse.get_pos()[1]
        inside = (ox - self.x) ** 2 + (oy - self.y) ** 2 < self.radius**2
        return inside

    def get_area(self):
        return pi * self.radius**2


class Polygon(Shape):
    def __init__(
        self, points: list[tuple], color: str = "black", outline: bool = False
    ):
        self.color = color
        self.points = points
        self.outline = int(outline)
        _shapes.append(self)

    def is_obj_over(self, ox=None, oy=None):
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


class Line(Shape):
    def __init__(self, points: list[tuple], width: int = 10, color: str = "black"):
        self.color = color
        self.points = points
        self.width = width
        _shapes.append(self)

    def is_obj_over(self, ox=None, oy=None):
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
        dx = x2 - x1
        dy = y2 - y1

        if dx == 0 and dy == 0:
            return ((px - x1) ** 2 + (py - y1) ** 2) ** 0.5

        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))

        closest_x = x1 + t * dx
        closest_y = y1 + t * dy

        return ((px - closest_x) ** 2 + (py - closest_y) ** 2) ** 0.5


class Image(Shape):
    def __init__(
        self, x: int, y: int, img_path: str, width: int = None, height: int = None
    ):
        super().__init__(x, y)
        self.img_path = img_path
        self.original_img = pygame.image.load(self.img_path)

        img_width, img_height = self.original_img.get_size()
        self.width = width if width is not None else img_width
        self.height = height if height is not None else img_height

        self.surface = pygame.transform.scale(
            self.original_img, (self.width, self.height)
        )

    def is_obj_over(self, ox=None, oy=None):
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
    ):
        super().__init__(x, y, color)
        self.text = text
        self.size = size
        self.font = pygame.font.SysFont(font, size)

    @property
    def txtsurf(self):
        return self.font.render(str(self.text), True, self.color)

    def is_obj_over(self, ox=None, oy=None):
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
    def __init__(self, *shapes: list[Shape]):
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

    def add(self, *shapes):
        for s in shapes:
            if not isinstance(s, Shape):
                raise TypeError(f"{s} must be Shape")
            self.grouped.append(s)

    def remove(self, *shapes):
        for s in shapes:
            self.grouped.remove(s)
            _shapes.remove(s)

    def clear(self):
        self.grouped.clear()

    def is_obj_over(self, x, y):
        for i in self.grouped:
            if i.is_obj_over(x, y):
                return True
        return False

    def __str__(self):
        return "group"


class CollisionManager:
    @staticmethod
    def rect_rect(rect1: Rect, rect2: Rect):
        return pygame.Rect(*rect1.rect).colliderect(pygame.Rect(*rect2.rect))

    @staticmethod
    def rect_circle(rect: Rect, circle: Circle):
        closest_x = max(rect.x, min(circle.x, rect.x + rect.width))
        closest_y = max(rect.y, min(circle.y, rect.y + rect.height))
        dist = ((circle.x - closest_x) ** 2 + (circle.y - closest_y) ** 2) ** 0.5
        return dist < circle.radius

    @staticmethod
    def circle_circle(circle1: Circle, circle2: Circle):
        dist = ((circle1.x - circle2.x) ** 2 + (circle1.y - circle2.y) ** 2) ** 0.5
        return dist < circle1.radius + circle2.radius

    @staticmethod
    def rect_polygon(rect: Rect, polygon: Polygon):
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
        if polygon.is_obj_over(circle.x, circle.y):
            return True
        for px, py in polygon.points:
            dist = ((circle.x - px) ** 2 + (circle.y - py) ** 2) ** 0.5
            if dist < circle.radius:
                return True
        return False

    @staticmethod
    def rect_text(rect, text):
        text_width = text.txtsurf.get_width()
        text_height = text.txtsurf.get_height()
        return pygame.Rect(*rect.rect).colliderect(
            pygame.Rect(text.x, text.y, text_width, text_height)
        )

    @staticmethod
    def circle_text(circle, text):
        text_width = text.txtsurf.get_width()
        text_height = text.txtsurf.get_height()
        closest_x = max(text.x, min(circle.x, text.x + text_width))
        closest_y = max(text.y, min(circle.y, text.y + text_height))
        dist = ((circle.x - closest_x) ** 2 + (circle.y - closest_y) ** 2) ** 0.5
        return dist < circle.radius

    @staticmethod
    def rect_image(rect, image):
        return pygame.Rect(*rect.rect).colliderect(
            pygame.Rect(image.x, image.y, image.width, image.height)
        )

    @staticmethod
    def circle_image(circle, image):
        closest_x = max(image.x, min(circle.x, image.x + image.width))
        closest_y = max(image.y, min(circle.y, image.y + image.height))
        dist = ((circle.x - closest_x) ** 2 + (circle.y - closest_y) ** 2) ** 0.5
        return dist < circle.radius

    @staticmethod
    def groupcollision(group, shape):
        for child in group.grouped:
            if is_colliding(child, shape):
                return True
        return False

    def no_collsion_method(shape1, shape2):
        raise Exception(f"{type(shape1)} and {type(shape2)} have no collision method")


def check_args(func, name):
    sig = signature(func)
    param_names = list(sig.parameters)
    if str(sig) != "()":
        raise ValueError(
            f'Functions defined with the @{name} decorator may not take arguments\n but "{func.__name__}" was defined with {param_names}'
        )


# decorartors like this get weird: if you want to be able to pass arguments in you need to handle 2 cases
# if theres no arguments then it just takes the function as the argument
def on_tick(func: Callable):
    name = currentframe().f_code.co_name
    check_args(func, name)
    _ontick.append(func)
    return func


def on_press(target: Callable | str):
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


def set_bg(color: str):
    global _bgcolor
    _bgcolor = color


def clear_screen():
    _shapes.clear()


def erase(obj):
    _shapes.remove(obj)


def is_colliding(shape1: Shape, shape2: Shape) -> bool:
    if "group" == str(shape1) or "group" == str(shape2):
        method_name = "groupcollision"
        method = getattr(CollisionManager, method_name, None)
        return method(shape1, shape2)
    method_name = f"{str(shape1)}_{str(shape2)}"
    method = getattr(CollisionManager, method_name, None)
    if method is None:
        method_name = f"{str(shape2)}_{str(shape1)}"
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
    caption: str = "SG window",
):

    global _bgcolor

    if resizable:
        screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    else:
        screen = pygame.display.set_mode((width, height))

    pygame.display.set_caption(caption)
    clock = pygame.time.Clock()
    running = True

    def handle_events():
        nonlocal running

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

        for func in _ontick:
            func()

    while running:
        handle_events()

        screen.fill(_bgcolor)

        for shape in _shapes:
            if str(shape) == "circle":
                pygame.draw.circle(
                    screen, shape.color, (shape.x, shape.y), shape.radius, shape.outline
                )
            elif str(shape) == "rect":
                pygame.draw.rect(
                    screen,
                    shape.color,
                    shape.rect,
                    shape.outline,
                )
            elif str(shape) == "polygon":
                pygame.draw.polygon(screen, shape.color, shape.points, shape.outline)
            elif str(shape) == "line":
                for i in range(1, len(shape.points)):
                    pygame.draw.line(
                        screen,
                        shape.color,
                        shape.points[i - 1],
                        shape.points[i],
                        shape.width,
                    )
            elif str(shape) == "text":
                screen.blit(shape.txtsurf, (shape.x, shape.y))
            elif str(shape) == "image":
                screen.blit(shape.surface, (shape.x, shape.y))
            elif str(shape) == "group":
                pass  # this stops weird edgecases while keeping good rendering

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
