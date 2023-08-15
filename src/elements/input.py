from . import button
from . import utils
from . import pygame


#TO DO: docstrings


class TextInput:
    def __init__(self, input_button: object, font_colour: tuple[int], font_size: int, font_name: str | None = None, on_selected: callable = None, on_deselect: callable = None, on_text_input: callable = None, start_text: str = "", prefix_text: str = "", min_font_size: int = 10, change_font_size: bool = True, antialias: bool = False) -> None:
        self.font_colour = font_colour
        self.font_name = font_name

        self.font_size = font_size
        self.og_font_size = font_size
        self.min_font_size = min_font_size

        self.on_selected = on_selected
        self.on_deselect = on_deselect
        self.on_text_input = on_text_input

        self.text = start_text
        self.prefix_text = prefix_text

        self.antialias = antialias
        self.change_font_size = change_font_size

        self.input_button = self.create_text_wrapper(input_button)
        self.normal_button_on_click = self.input_button.button_object.on_click

        self.setup_button()

        self.selected = False

    def create_text_wrapper(self, input_button: object) -> button.TextWrapper:
        if type(input_button) == button.TextWrapper:
            return input_button
        else:
            text_wrapper = button.TextWrapper(input_button, self.text, self.font_colour, self.font_size, self.font_name, self.antialias)

            return text_wrapper
        
    def setup_button(self) -> None:
        self.input_button.button_object.on_click = self.on_click
        
    def on_click(self) -> None:
        self.input_button.button_object.call_func(self.normal_button_on_click)
        self.selected = True
        utils.call_func(self.on_selected, self)

    def check_deselect(self) -> None:
        if pygame.mouse.get_pressed()[0] and not self.input_button.button_object.mouse_over():
            self.selected = False
            utils.call_func(self.on_deselect, self)

    def take_input(self, pygame_event_loop: list[pygame.event.Event]) -> None:        
        for event in pygame_event_loop:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

                utils.call_func(self.on_text_input, self.text, self)

    def text_too_large(self) -> bool:
        text_rect = self.input_button.get_text()[1]
        text_width = text_rect.width
        btn_width = self.input_button.button_object.get_width()

        return text_width > btn_width

    def update_font_size(self) -> None:
        self.font_size = self.og_font_size
        self.input_button.font = pygame.font.Font(self.font_name, self.font_size)

        while self.text_too_large() and self.font_size > self.min_font_size:
            self.font_size -= 1
            self.input_button.font = pygame.font.Font(self.font_name, self.font_size)

    def draw(self) -> None:
        self.input_button.update_text(f"{self.prefix_text}{self.text}")
        self.input_button.update()

    def update(self, pygame_event_loop: list[pygame.event.Event]) -> None:
        self.draw()
        self.check_deselect()

        if self.change_font_size:
            self.update_font_size()

        if self.selected:
            self.take_input(pygame_event_loop)


class RectTextInput(TextInput):
    def __init__(self, surface: pygame.Surface, x: int, y: int, background_colour: tuple[int],  width: int, height: int, font_colour: tuple[int], font_size: int, font_name: str | None = None, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, on_selected: callable = None, on_deselect: callable = None, on_text_input: callable = None, corner_radius: int = -1, click_once: bool = True, text: str = "", prefix_text: str = "", min_font_size: int = 10, change_font_size: bool = True, antialias: bool = False) -> None:
        input_button = self.create_button(surface, x, y, background_colour, width, height, on_click, on_hover, on_normal, corner_radius, click_once)
        
        super().__init__(input_button, font_colour, font_size, font_name, on_selected, on_deselect, on_text_input, text, prefix_text, min_font_size, change_font_size, antialias)

    def create_button(self, surface: pygame.Surface, x: int, y: int, background_colour: tuple[int], width: int, height: int, on_click: callable, on_hover: callable, on_normal: callable, corner_radius: int, click_once: bool) -> button.RectButton:
        btn = button.RectButton(surface, x, y, background_colour, width, height, on_click, on_hover, on_normal, corner_radius, click_once)

        return btn
    

class CircleTextInput(TextInput):
    def __init__(self, surface: pygame.Surface, x: int, y: int, background_colour: tuple[int],  radius: int, font_colour: tuple[int], font_size: int, font_name: str | None = None, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, on_selected: callable = None, on_deselect: callable = None, on_text_input: callable = None, click_once: bool = True, text: str = "", prefix_text: str = "", min_font_size: int = 10, change_font_size: bool = True, antialias: bool = False) -> None:
        input_button = self.create_button(surface, x, y, background_colour, radius, on_click, on_hover, on_normal, click_once)
        
        super().__init__(input_button, font_colour, font_size, font_name, on_selected, on_deselect, on_text_input, text, prefix_text, min_font_size, change_font_size, antialias)

    def create_button(self, surface: pygame.Surface, x: int, y: int, background_colour: tuple[int], radius: int, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, click_once: bool = True) -> button.CircleButton:
        btn = button.CircleButton(surface, x, y, background_colour, radius, on_click, on_hover, on_normal, click_once)

        return btn
    

class PolygonTextInput(TextInput):
    def __init__(self, surface: pygame.Surface, points: list[tuple[int]], background_colour: tuple[int], font_colour: tuple[int], font_size: int, font_name: str | None = None, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, on_selected: callable = None, on_deselect: callable = None, on_text_input: callable = None, click_once: bool = True, text: str = "", prefix_text: str = "", min_font_size: int = 10, antialias: bool = False) -> None:
        input_button = self.create_button(surface, points, background_colour, on_click, on_hover, on_normal, click_once)
        
        super().__init__(input_button, font_colour, font_size, font_name, on_selected, on_deselect, on_text_input, text, prefix_text, min_font_size, False, antialias)

    def create_button(self, surface: pygame.Surface, points: list[tuple[int]], background_colour: tuple[int], on_click: callable = None, on_hover: callable = None, on_normal: callable = None, click_once: bool = True) -> button.PolygonButton:
        btn = button.PolygonButton(surface, points, background_colour, on_click, on_hover, on_normal, click_once)

        return btn


class BorderedRectTextInput(TextInput):
    def __init__(self, surface: pygame.Surface, x: int, y: int, background_colour: tuple[int], border_colour: tuple[int], width: int, height: int, border_width: int, font_colour: tuple[int], font_size: int, font_name: str | None = None, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, on_selected: callable = None, on_deselect: callable = None, on_text_input: callable = None, corner_radius: int = -1, click_once: bool = True, text: str = "", prefix_text: str = "", min_font_size: int = 10, change_font_size: bool = True, antialias: bool = False) -> None:
        input_button = self.create_button(surface, x, y, background_colour, border_colour, width, height, border_width, on_click, on_hover, on_normal, corner_radius, click_once)
        
        super().__init__(input_button, font_colour, font_size, font_name, on_selected, on_deselect, on_text_input, text, prefix_text, min_font_size, change_font_size, antialias)

    def create_button(self, surface: pygame.Surface, x: int, y: int, background_colour: tuple[int], border_colour: tuple[int], width: int, height: int, border_width: int, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, corner_radius: int = -1, click_once: bool = True) -> button.BorderedRectButton:
        btn = button.BorderedRectButton(surface, x, y, background_colour, border_colour, width, height, border_width, on_click, on_hover, on_normal, corner_radius, click_once)

        return btn


class BorderedCircleTextInput(TextInput):
    def __init__(self, surface: pygame.Surface, x: int, y: int, background_colour: tuple[int],  border_colour: tuple[int], radius: int, border_width: int, font_colour: tuple[int], font_size: int, font_name: str | None = None, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, on_selected: callable = None, on_deselect: callable = None, on_text_input: callable = None, click_once: bool = True, text: str = "", prefix_text: str = "", min_font_size: int = 10, change_font_size: bool = True, antialias: bool = False) -> None:
        input_button = self.create_button(surface, x, y, background_colour, border_colour, radius, border_width, on_click, on_hover, on_normal, click_once)
        
        super().__init__(input_button, font_colour, font_size, font_name, on_selected, on_deselect, on_text_input, text, prefix_text, min_font_size, change_font_size, antialias)

    def create_button(self, surface: pygame.Surface, x: int, y: int, background_colour: tuple[int], border_colour: tuple[int], radius: int, border_width: int, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, click_once: bool = True) -> button.BorderedCircleButton:
        btn = button.BorderedCircleButton(surface, x, y, background_colour, border_colour, radius, border_width, on_click, on_hover, on_normal, click_once)

        return btn
    

class BorderedPolygonTextInput(TextInput):
    def __init__(self, surface: pygame.Surface, points: list[tuple[int]], background_colour: tuple[int], border_colour: tuple[int], border_width: int, font_colour: tuple[int], font_size: int, font_name: str | None = None, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, on_selected: callable = None, on_deselect: callable = None, on_text_input: callable = None, click_once: bool = True, text: str = "", prefix_text: str = "", min_font_size: int = 10, antialias: bool = False) -> None:
        input_button = self.create_button(surface, points, background_colour, border_colour, border_width, on_click, on_hover, on_normal, click_once)
        
        super().__init__(input_button, font_colour, font_size, font_name, on_selected, on_deselect, on_text_input, text, prefix_text, min_font_size, False, antialias)

    def create_button(self, surface: pygame.Surface, points: list[tuple[int]], background_colour: tuple[int], border_colour: tuple[int], border_width: int, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, click_once: bool = True) -> button.BorderedPolygonButton:
        btn = button.BorderedPolygonButton(surface, points, background_colour, border_colour, border_width, on_click, on_hover, on_normal, click_once)

        return btn