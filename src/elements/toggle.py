from . import button
from . import utils
from . import pygame


# TODO: (possibly) seperate classes for each button, docstrings, use dist_from_edge instead of dist_from_center


class Toggle:
    def __init__(self, button_object: object, on_value_changed: callable = None, start_value: bool = False) -> None:
        self.button_object = button_object
        self.normal_button_on_click = self.button_object.on_click

        self.on_value_changed = on_value_changed

        self.selected = start_value
        self.prev_selected = start_value

        self.setup_button()
        
    def setup_button(self) -> None:
        self.button_object.click_once = True
        self.button_object.on_click = self.on_button_click

    def on_button_click(self) -> None:
        self.button_object.call_func(self.normal_button_on_click)
        self.selected = not self.selected

    def draw(self) -> None:
        self.button_object.update()

    def update(self) -> None:
        self.draw()

        if self.selected != self.prev_selected:
            utils.call_func(self.on_value_changed, self.selected)
            self.prev_selected = self.selected


class TextToggle(Toggle):
    def __init__(self, button_object: object, text: str, text_x: int, text_y: int, font_colour: tuple[int], font_size: int, font_name: str | None = None, on_value_changed: callable = None, start_value: bool = False, antialias: bool = False) -> None:
        super().__init__(button_object, on_value_changed, start_value)

        self.text = text

        self.text_x = text_x
        self.text_y = text_y

        self.font_colour = font_colour
        self.font = pygame.font.Font(font_name, font_size)

        self.antialias = antialias

    def get_text(self) -> tuple[pygame.Surface, pygame.Rect]:
        text_surf = self.font.render(self.text, self.antialias, self.font_colour, self.button_object.background_colour)
        text_rect = text_surf.get_rect()
        text_rect.center = (self.text_x, self.text_y)

        return text_surf, text_rect
    
    def blit_text(self) -> None:
        surf, rect = self.get_text()
        self.button_object.surface.blit(surf, rect)

    def draw(self) -> None:
        self.button_object.update()
        self.blit_text()


class TickBox(Toggle):
    def __init__(self, surface: pygame.Surface, tick_thickness: int, tick_colour: tuple[int], x: int, y: int, background_colour: tuple[int], side_length: int, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, corner_radius: int = -1, on_value_changed: callable = None, start_value: bool = False) -> None:
        self.button_object = button.RectButton(surface, x, y, background_colour, side_length, side_length, on_click, on_hover, on_normal, corner_radius, True)
        
        self.surface = surface

        self.tick_thickness = tick_thickness
        self.tick_colour = tick_colour

        super().__init__(self.button_object, on_value_changed, start_value)
    
    def draw_tick(self) -> None:
        width = self.button_object.width
        height = self.button_object.height

        x = self.button_object.x - width // 2
        y = self.button_object.y - height // 2

        left = (x + int(width * 0.2), y + int(height * 0.6))
        middle = (x + int(width * 0.4), y + int(height * 0.9))
        right = (x + int(width * 0.9), y + int(height * 0.2))

        pygame.draw.line(self.surface, self.tick_colour, left, middle, self.tick_thickness)
        pygame.draw.line(self.surface, self.tick_colour, middle, right, self.tick_thickness)

    def draw(self) -> None:
        self.button_object.update()

        if self.selected:
            self.draw_tick()


class TickBoxToggle:
    def __init__(self, surface: pygame.Surface, tick_thickness: int, tick_colour: tuple[int], tick_box_colour: tuple[int], outer_box_colour: tuple[int], x: int, y: int, width: int, height: int, text: str, font_colour: tuple[int], font_size: int, font_name: str | None = None, dist_from_edge: int = 5, height_offset: int = 10, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, on_value_changed: callable = None, inner_corner_radius: int = -1, outer_corner_radius: int = -1, start_value: bool = False, text_to_right: bool = True, antialias: bool = False) -> None:
        self.surface = surface

        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.outer_box_colour = outer_box_colour
        self.outer_corner_radius = outer_corner_radius

        self.text_to_right = text_to_right

        self.tick_box = self.create_tick_box(tick_thickness, tick_colour, tick_box_colour, dist_from_edge, height_offset, on_click, on_hover, on_normal, on_value_changed, inner_corner_radius, start_value)
        self.text_surface, self.text_rect = self.get_text(text, font_name, font_size, font_colour, antialias)

    def create_tick_box(self, tick_thickness: int, tick_colour: tuple[int], background_colour: tuple[int], dist_from_edge: int, height_offset: int, on_click: callable, on_hover: callable, on_normal: callable, on_value_changed: callable, corner_radius: int, start_value: bool) -> TickBox:
        new_height = self.height - height_offset

        if self.text_to_right:
            new_x = (self.x - self.width // 2) + (new_height // 2) + dist_from_edge
        else:
            new_x = (self.x + self.width // 2) - (new_height // 2) - dist_from_edge
        
        return TickBox(self.surface, tick_thickness, tick_colour, new_x, self.y, background_colour, new_height, on_click, on_hover, on_normal, corner_radius, on_value_changed, start_value)
    
    def find_text_pos(self) -> tuple[int, int]:        
        dist_to_center = self.tick_box.button_object.width // 2

        if self.text_to_right:
            x1 = self.x + self.width // 2
            x2 = self.tick_box.button_object.x + dist_to_center
        else:
            x1 = self.x - self.width // 2
            x2 = self.tick_box.button_object.x - dist_to_center

        x = (x1 + x2) // 2
        y = self.tick_box.button_object.y

        return (x, y)
    
    def get_text(self, text: str, font_name: str | None, font_size: int, font_colour: tuple[int], antialias: bool) -> tuple[pygame.Surface, pygame.Rect]:
        font = pygame.font.Font(font_name, font_size)
        
        text_surf = font.render(text, antialias, font_colour, self.outer_box_colour)
        text_rect = text_surf.get_rect()

        text_pos = self.find_text_pos()
        text_rect.center = text_pos

        return text_surf, text_rect

    def draw(self) -> None:
        outer_rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
        pygame.draw.rect(self.surface, self.outer_box_colour, outer_rect, border_radius=self.outer_corner_radius)

        self.surface.blit(self.text_surface, self.text_rect)

        self.tick_box.draw()

    def update(self) -> None:
        self.tick_box.update()
        self.draw()