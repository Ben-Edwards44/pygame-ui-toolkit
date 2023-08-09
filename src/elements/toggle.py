from . import button
from . import utils
from . import pygame


# TODO: base toggle class - [update], (possibly) seperate classes for each button, default tick/cross


class Toggle:
    def __init__(self, button_object: object, font_colour: tuple[int], font_size: int, font_name: str | None = None, text: str = "",  on_value_changed: callable = None, start_value: bool = False, antialias: bool = False) -> None:
        self.button_object = self.create_text_wrapper(button_object, text, font_colour, font_size, font_name, antialias)
        self.normal_button_on_click = self.button_object.button_object.on_click

        self.text = text

        self.selected = start_value

    def create_text_wrapper(self, button_object: object, text: str, font_colour: tuple[int], font_size: int, font_name: str | None, antialias: bool) -> button.TextWrapper:
        if type(button_object) == button.TextWrapper:
            return button_object
        else:
            text_wrapper = button.TextWrapper(button_object, text, font_colour, font_size, font_name, antialias)
            return text_wrapper
        
    def setup_button(self) -> None:
        self.button_object.button_object.click_once = True
        self.button_object.button_object.on_click = self.on_button_click
        self.button_object.text = self.text

    def on_button_click(self) -> None:
        self.button_object.button_object.call_func(self.normal_button_on_click)
        self.selected = not self.selected

    def draw(self) -> None:
        self.button_object.update()

    def update(self) -> None:
        self.draw()