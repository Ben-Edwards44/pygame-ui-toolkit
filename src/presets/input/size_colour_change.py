from . import size_change
from . import colour_change
from . import input
from . import utils
from . import pygame


stored_variables = {}


def assign_variables(text_input: input.TextInput) -> None:
    current_variables = {
        "on_select" : text_input.on_selected,
        "on_deselect" : text_input.on_deselect
    }

    stored_variables[text_input] = current_variables


def change_colour(text_input: input.TextInput, normal_event_func: callable, new_event_func: callable) -> None:
    button_object = text_input.input_button.button_object

    utils.call_func(normal_event_func, text_input)
    new_event_func(button_object)


def on_selected_func(text_input: input.TextInput) -> None:
    normal = stored_variables[text_input]["on_select"]
    new = colour_change.on_click_func

    change_colour(text_input, normal, new)


def on_deselect_func(text_input: input.TextInput) -> None:
    normal = stored_variables[text_input]["on_deselect"]
    new = colour_change.on_normal_func

    change_colour(text_input, normal, new)


def create_text_input(deselected_colour: tuple[int], selected_colour: tuple[int], normal_size: tuple[int] | int, hover_size: tuple[int] | int, click_size: tuple[int] | int, surface: pygame.Surface, x: int, y: int, font_colour: tuple[int], font_size: int, font_name: str | None = None, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, on_selected: callable = None, on_deselect: callable = None, on_text_input: callable = None, corner_radius: int = -1, text: str = "", prefix_text: str = "", min_font_size: int = 10, change_font_size: bool = True, antialias: bool = False) -> input.RectTextInput:
    text_input = input.RectTextInput(surface, x, y, deselected_colour, normal_size[0], normal_size[1], font_colour, font_size, font_name, on_click, on_hover, on_normal, on_selected, on_deselect, on_text_input, corner_radius, False, text, prefix_text, min_font_size, change_font_size, antialias)

    change_existing_text_input(text_input, deselected_colour, selected_colour, normal_size, hover_size, click_size)

    return text_input


def change_existing_text_input(text_input: input.TextInput, deselected_colour: tuple[int], selected_colour: tuple[int], normal_size: tuple[int] | int, hover_size: tuple[int] | int, click_size: tuple[int] | int) -> None:
    assign_variables(text_input)
    
    button_object = text_input.input_button.button_object

    text_input.on_selected = on_selected_func
    text_input.on_deselect = on_deselect_func

    size_change.change_existing_button(button_object, normal_size, hover_size, click_size)
    colour_change.assign_variables(button_object, deselected_colour, deselected_colour, selected_colour, None, None, None)