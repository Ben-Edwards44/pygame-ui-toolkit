from . import toggle
from . import button
from . import utils
from . import pygame


#TODO: docstrings


class Option:
    def __init__(self, parent_dropdown: object, text_wrapper: button.TextWrapper, start_active: bool = False) -> None:
        self.parent_dropdown = parent_dropdown
        
        self.text_wrapper = text_wrapper
        self.normal_button_on_click = text_wrapper.button_object.on_click

        self.active = start_active

        self.setup_button()

    def setup_button(self) -> None:
        self.text_wrapper.button_object.on_click = self.on_button_click

    def on_button_click(self) -> None:
        self.text_wrapper.button_object.call_func(self.normal_button_on_click)

        self.parent_dropdown.option_selected(self)

    def update(self) -> None:
        if self.active:
            self.text_wrapper.update()


class Dropdown(toggle.Toggle):
    def __init__(self, button_object: object, option_buttons: list[object], option_names: list[str], font_colour: tuple[int], font_size: int, font_name: str | None = None, on_option_changed: callable = None, initial_option: int = 0, start_active: bool = False, antialias: bool = False) -> None:
        self.font_colour = font_colour
        self.font_size = font_size
        self.font_name = font_name

        self.on_option_changed = on_option_changed

        self.antialias = antialias
        
        self.options = self.create_options(option_buttons, option_names, start_active)

        self.selected_option = self.options[initial_option]

        self.text_wrapper = button.TextWrapper(button_object, self.selected_option.text_wrapper.text, font_colour, font_size, font_name, antialias)

        super().__init__(button_object, self.on_value_changed, False)

    def create_options(self, option_buttons: list[object], option_names: list[str], start_active: bool) -> list[Option]:
        options = []
        for i, x in enumerate(option_buttons):
            text = option_names[i]

            text_wrapper = button.TextWrapper(x, text, self.font_colour, self.font_size, self.font_name, self.antialias)
            option = Option(self, text_wrapper, start_active)

            options.append(option)

        return options

    def on_value_changed(self, value: bool) -> None:
        for i in self.options:
            i.active = value

    def option_selected(self, option: Option) -> None:
        self.selected_option = option
        self.selected = False

        self.text_wrapper.update_text(option.text_wrapper.text, self.font_colour, self.font_size, self.font_name)

        utils.call_func(self.on_option_changed, option, self)

    def update(self) -> None:
        self.text_wrapper.update()

        for i in self.options:
            i.update()

        if self.selected != self.prev_selected:
            utils.call_func(self.on_value_changed, self.selected)
            self.prev_selected = self.selected


class RectDropdown(Dropdown):
    def __init__(self, surface: pygame.Surface, option_names: list[str], x: int, y: int, background_colour: tuple[int], width: int, height: int, font_colour: tuple[int], font_size: int, font_name: str | None = None, y_offset: int = 10, on_option_changed: callable = None, initial_option: int = 0, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, corner_radius: int = -1, start_active: bool = False, antialias: bool = False) -> None:
        button_object = button.RectButton(surface, x, y, background_colour, width, height, on_click, on_hover, on_normal, corner_radius)
        option_buttons = self.create_buttons(surface, len(option_names), x, y, background_colour, width, height, y_offset, on_click, on_hover, on_normal, corner_radius)

        super().__init__(button_object, option_buttons, option_names, font_colour, font_size, font_name, on_option_changed, initial_option, start_active, antialias)

    def create_buttons(self, surface: pygame.Surface, num_options: int, x: int, y: int, colour: tuple[int], width: int, height: int, y_offset: int, on_click: callable, on_hover: callable, on_normal: callable, corner_radius: int) -> list[button.RectButton]:
        buttons = []
        for i in range(1, num_options + 1):
            new_y = y + i * (height + y_offset)

            btn = button.RectButton(surface, x, new_y, colour, width, height, on_click, on_hover, on_normal, corner_radius)
            buttons.append(btn)
            
        return buttons
    

class CircleDropdown(Dropdown):
    def __init__(self, surface: pygame.Surface, option_names: list[str], x: int, y: int, background_colour: tuple[int], radius: int, font_colour: tuple[int], font_size: int, font_name: str | None = None, y_offset: int = 10, on_option_changed: callable = None, initial_option: int = 0, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, start_active: bool = False, antialias: bool = False) -> None:
        button_object = button.CircleButton(surface, x, y, background_colour, radius, on_click, on_hover, on_normal)
        option_buttons = self.create_buttons(surface, len(option_names), x, y, background_colour, radius, y_offset, on_click, on_hover, on_normal)

        super().__init__(button_object, option_buttons, option_names, font_colour, font_size, font_name, on_option_changed, initial_option, start_active, antialias)

    def create_buttons(self, surface: pygame.Surface, num_options: int, x: int, y: int, colour: tuple[int], radius: int, y_offset: int, on_click: callable, on_hover: callable, on_normal: callable) -> list[button.RectButton]:
        buttons = []
        for i in range(1, num_options + 1):
            new_y = y + i * (2 * radius + y_offset)

            btn = button.CircleButton(surface, x, new_y, colour, radius, on_click, on_hover, on_normal)
            buttons.append(btn)
            
        return buttons
    

class BorderedRectDropdown(Dropdown):
    def __init__(self, surface: pygame.Surface, option_names: list[str], x: int, y: int, background_colour: tuple[int], border_colour: tuple[int], width: int, height: int, border_width: int, font_colour: tuple[int], font_size: int, font_name: str | None = None, y_offset: int = 10, on_option_changed: callable = None, initial_option: int = 0, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, corner_radius: int = -1, start_active: bool = False, antialias: bool = False) -> None:
        button_object = button.BorderedRectButton(surface, x, y, background_colour, border_colour, width, height, border_width, on_click, on_hover, on_normal, corner_radius)
        option_buttons = self.create_buttons(surface, len(option_names), x, y, background_colour, border_colour, width, height, border_width, y_offset, on_click, on_hover, on_normal, corner_radius)

        super().__init__(button_object, option_buttons, option_names, font_colour, font_size, font_name, on_option_changed, initial_option, start_active, antialias)

    def create_buttons(self, surface: pygame.Surface, num_options: int, x: int, y: int, background_colour: tuple[int], border_colour: tuple[int], width: int, height: int, border_width: tuple[int], y_offset: int, on_click: callable, on_hover: callable, on_normal: callable, corner_radius: int) -> list[button.RectButton]:
        buttons = []
        for i in range(1, num_options + 1):
            new_y = y + i * (height + y_offset)

            btn = button.BorderedRectButton(surface, x, new_y, background_colour, border_colour, width, height, border_width, on_click, on_hover, on_normal, corner_radius)
            buttons.append(btn)
            
        return buttons
    

class BorderedCircleDropdown(Dropdown):
    def __init__(self, surface: pygame.Surface, option_names: list[str], x: int, y: int, background_colour: tuple[int], border_colour: tuple[int], radius: int, border_width: int, font_colour: tuple[int], font_size: int, font_name: str | None = None, y_offset: int = 10, on_option_changed: callable = None, initial_option: int = 0, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, start_active: bool = False, antialias: bool = False) -> None:
        button_object = button.BorderedCircleButton(surface, x, y, background_colour, border_colour, radius, border_width, on_click, on_hover, on_normal)
        option_buttons = self.create_buttons(surface, len(option_names), x, y, background_colour, border_colour, radius, border_width, y_offset, on_click, on_hover, on_normal)

        super().__init__(button_object, option_buttons, option_names, font_colour, font_size, font_name, on_option_changed, initial_option, start_active, antialias)

    def create_buttons(self, surface: pygame.Surface, num_options: int, x: int, y: int, background_colour: tuple[int], border_colour: tuple[int], radius: int, border_width: int, y_offset: int, on_click: callable, on_hover: callable, on_normal: callable) -> list[button.RectButton]:
        buttons = []
        for i in range(1, num_options + 1):
            new_y = y + i * (2 * radius + y_offset)

            btn = button.BorderedCircleButton(surface, x, new_y, background_colour, border_colour, radius, border_width, on_click, on_hover, on_normal)
            buttons.append(btn)
            
        return buttons