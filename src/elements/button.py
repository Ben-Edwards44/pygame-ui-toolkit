from . import pygame
from . import utils


#TO DO: docstrings


class Button:
    def __init__(self, surface: pygame.Surface, x: int, y: int, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, click_once: bool = True) -> None:
        self.surface = surface

        self.x = x
        self.y = y

        self.on_click = on_click
        self.on_hover = on_hover
        self.on_normal = on_normal

        self.click_once = click_once

        self.clicked = False
        self.hovered = False

    def update_clicked(self, currently_clicked: bool) -> bool:
        if not self.click_once:
            self.clicked = currently_clicked
            return currently_clicked
        
        if not currently_clicked:
            self.clicked = False
            return False
        
        if self.clicked:
            return False
        else:
            self.clicked = True
            return True
        
    def update_hovered(self, currently_hovered: bool) -> bool:
        if not self.click_once:
            self.hovered = currently_hovered
            return currently_hovered
        
        if not currently_hovered:
            self.hovered = False
            return False
        
        if self.hovered:
            return False
        else:
            self.hovered = True
            return True

    get_pos = lambda self: (self.x, self.y)

    def call_func(self, func: callable) -> None:
        if func == None:
            return
        else:
            utils.call_func(func, self)
        
    def check_click(self) -> bool:
        mouse_over = self.mouse_over()
        mouse_down = pygame.mouse.get_pressed(3)[0]

        click = mouse_over and mouse_down

        return self.update_clicked(click)
    
    def check_hover(self) -> bool:
        mouse_over = self.mouse_over()

        return self.update_hovered(mouse_over)
    
    def update(self) -> None:
        self.draw()

        if self.check_click():
            self.call_func(self.on_click)
        elif self.check_hover():
            self.call_func(self.on_hover)
        else:
            self.call_func(self.on_normal)


class RectButton(Button):
    def __init__(self, surface: pygame.Surface, x: int, y: int, background_colour: tuple[int], width: int, height: int, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, corner_radius: int = -1, click_once: bool = True) -> None:
        super().__init__(surface, x, y, on_click, on_hover, on_normal, click_once)

        self.width = width
        self.height = height

        self.background_colour = background_colour

        self.corner_radius = corner_radius

    def mouse_over(self) -> bool:
        x, y = pygame.mouse.get_pos()

        min_x = self.x - self.width // 2
        max_x = self.x + self.width // 2
        min_y = self.y - self.height // 2
        max_y = self.y + self.height // 2

        return min_x <= x <= max_x and min_y <= y <= max_y
    
    def draw(self) -> None:
        rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
        pygame.draw.rect(self.surface, self.background_colour, rect, border_radius=self.corner_radius)

    get_width = lambda self: self.width


class CircleButton(Button):
    def __init__(self, surface: pygame.Surface, x: int, y: int, background_colour: tuple[int], radius: int, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, click_once: bool = True) -> None:
        super().__init__(surface, x, y, on_click, on_hover, on_normal, click_once)

        self.background_colour = background_colour

        self.radius = radius
        self.radius_sq = radius**2

    def mouse_over(self) -> bool:
        x, y = pygame.mouse.get_pos()

        dist_sq = (x - self.x)**2 + (y - self.y)**2

        return dist_sq < self.radius_sq
    
    def draw(self) -> None:
        center = self.get_pos()
        pygame.draw.circle(self.surface, self.background_colour, center, self.radius)

    get_width = lambda self: self.radius * 2


class PolygonButton(Button):
    def __init__(self, surface: pygame.Surface, points: list[tuple[int]], background_colour: tuple[int], on_click: callable = None, on_hover: callable = None, on_normal: callable = None, click_once: bool = True) -> None:
        x, y = self.get_center(points)
        
        super().__init__(surface, x, y, on_click, on_hover, on_normal, click_once)

        self.points = points
        self.background_colour = background_colour

        self.inequalities = self.get_inequalities(points, x, y)

    def get_center(self, points: list[tuple[int]]) -> tuple[int]:
        x_values = [i[0] for i in points]
        y_values = [i[1] for i in points]

        x = sum(x_values) // len(x_values)
        y = sum(y_values) // len(y_values)

        return x, y
    
    def get_inequalities(self, points: list[tuple[int]], center_x: int, center_y: int) -> list[tuple[float, float, bool]]:
        inequalities = []
        for i, x in enumerate(points):
            try:
                m = (x[1] - points[i - 1][1]) / (x[0] - points[i - 1][0])
            except ZeroDivisionError:
                m = 1e10

            c = x[1] - m * x[0]
            greater_than = (m * center_x + c) < center_y

            inequalities.append((m, c, greater_than))

        return inequalities

    def mouse_over(self) -> None:
        x, y = pygame.mouse.get_pos()

        for m, c, greater_than in self.inequalities:
            intersect_y = m * x + c
            actual_greater_than = intersect_y < y

            if actual_greater_than != greater_than:
                return False
            
        return True
    
    def draw(self) -> None:
        pygame.draw.polygon(self.surface, self.background_colour, self.points)


class ImageButton(RectButton):
    def __init__(self, surface: pygame.Surface, x: int, y: int, width: int, height: int, image_path: str, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, click_once: bool = True) -> None:
        super().__init__(surface, x, y, None, width, height, on_click, on_hover, on_normal, -1, click_once)

        self.image_path = image_path

        self.setup_image()

    def setup_image(self) -> None:
        image = pygame.image.load(self.image_path)
        scaled_image = pygame.transform.scale(image, (self.width, self.height))

        self.image = scaled_image

    def draw(self) -> None:
        image_x = self.x - self.width // 2
        image_y = self.y - self.height // 2

        self.surface.blit(self.image, (image_x, image_y))


class BorderedRectButton(RectButton):
    def __init__(self, surface: pygame.Surface, x: int, y: int, background_colour: tuple[int], border_colour: tuple[int], width: int, height: int, border_width: int, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, corner_radius: int = -1, click_once: bool = True) -> None:
        super().__init__(surface, x, y, background_colour, width, height, on_click, on_hover, on_normal, corner_radius, click_once)

        self.border_colour = border_colour
        self.border_width = border_width

    def draw(self) -> None:
        rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

        pygame.draw.rect(self.surface, self.background_colour, rect, border_radius=self.corner_radius)
        pygame.draw.rect(self.surface, self.border_colour, rect, self.border_width, self.corner_radius)


class BorderedCircleButton(CircleButton):
    def __init__(self, surface: pygame.Surface, x: int, y: int, background_colour: tuple[int], border_colour: tuple[int], radius: int, border_width: int, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, click_once: bool = True) -> None:
        super().__init__(surface, x, y, background_colour, radius, on_click, on_hover, on_normal, click_once)

        self.border_colour = border_colour
        self.border_width = border_width

    def draw(self) -> None:
        pygame.draw.circle(self.surface, self.background_colour, self.get_pos(), self.radius)
        pygame.draw.circle(self.surface, self.border_colour, self.get_pos(), self.radius, self.border_width)


class BorderedPolygonButton(PolygonButton):
    def __init__(self, surface: pygame.Surface, points: list[tuple[int]], background_colour: tuple[int], border_colour: tuple[int], border_width: int, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, click_once: bool = True) -> None:
        super().__init__(surface, points, background_colour, on_click, on_hover, on_normal, click_once)

        self.border_colour = border_colour
        self.border_width = border_width

    def draw(self) -> None:
        pygame.draw.polygon(self.surface, self.background_colour, self.points)
        pygame.draw.polygon(self.surface, self.border_colour, self.points, self.border_width)


class TextWrapper:
    def __init__(self, button_object: RectButton | CircleButton | BorderedCircleButton | BorderedRectButton, text: str, font_colour: tuple[int], font_size: int, font_name: str | None = None, antialias: bool = False) -> None:
        self.button_object = button_object
        
        self.text = text
        self.font_colour = font_colour
        self.font = pygame.font.Font(font_name, font_size)

        self.antialias = antialias

    def get_text(self) -> tuple[pygame.Surface, pygame.Rect]:
        text_surf = self.font.render(self.text, self.antialias, self.font_colour, self.button_object.background_colour)
        text_rect = text_surf.get_rect()
        text_rect.center = self.button_object.get_pos()

        return text_surf, text_rect
    
    def blit_text(self) -> None:
        surf, rect = self.get_text()
        self.button_object.surface.blit(surf, rect)

    def draw(self) -> None:
        self.button_object.update()
        self.blit_text()
        
    def update(self) -> None:
        self.draw()