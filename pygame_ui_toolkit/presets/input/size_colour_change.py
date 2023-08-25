from pygame_ui_toolkit.presets.buttons import size_change
from pygame_ui_toolkit.presets.buttons import colour_change
from pygame_ui_toolkit.elements import input
from pygame_ui_toolkit import utils
from pygame_ui_toolkit import pygame


stored_variables = {}


def assign_variables(text_input: input.TextInput) -> None:
    """Assign variables that need to be used later to a global dict with the input object as the key."""

    current_variables = {
        "on_select" : text_input.on_selected,
        "on_deselect" : text_input.on_deselect
    }

    stored_variables[text_input] = current_variables


def change_colour(text_input: input.TextInput, normal_event_func: callable, new_event_func: callable) -> None:
    """Change the colour of the text input button object."""
    button_object = text_input.input_button.button_object

    utils.call_func(normal_event_func, text_input)
    new_event_func(button_object)


def on_selected_func(text_input: input.TextInput) -> None:
    """The function called when the input is selected."""
    normal = stored_variables[text_input]["on_select"]
    new = colour_change.on_click_func

    change_colour(text_input, normal, new)


def on_deselect_func(text_input: input.TextInput) -> None:
    """The function called when the input is deselected."""
    normal = stored_variables[text_input]["on_deselect"]
    new = colour_change.on_normal_func

    change_colour(text_input, normal, new)


def create_text_input(deselected_colour: tuple[int], selected_colour: tuple[int], normal_size: tuple[int] | int, hover_size: tuple[int] | int, click_size: tuple[int] | int, surface: pygame.Surface, x: int, y: int, font_colour: tuple[int], font_size: int, font_name: str | None = None, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, on_selected: callable = None, on_deselect: callable = None, on_text_input: callable = None, corner_radius: int = -1, text: str = "", prefix_text: str = "", min_font_size: int = 10, change_font_size: bool = True, antialias: bool = False) -> input.RectTextInput:
    """
    Return a new RectTextInput that will automatically change colour when selcted and change size when clicked or hovered.

    Ensure to call the input's update() method each frame.

    Notes
    -----
    normal_size, hover_size and click_size should be provided as a tuple in the form (width, height)
    - e.g. a value of (100, 50) would result in a text input with width 100 and height 50
    """

    text_input = input.RectTextInput(surface, x, y, deselected_colour, normal_size[0], normal_size[1], font_colour, font_size, font_name, on_click, on_hover, on_normal, on_selected, on_deselect, on_text_input, corner_radius, False, text, prefix_text, min_font_size, change_font_size, antialias)

    change_existing_text_input(text_input, deselected_colour, selected_colour, normal_size, hover_size, click_size)

    return text_input


def change_existing_text_input(text_input: input.TextInput, deselected_colour: tuple[int], selected_colour: tuple[int], normal_size: tuple[int] | int, hover_size: tuple[int] | int, click_size: tuple[int] | int) -> None:
    """
    Update a RectTextInput that will automatically change colour when selcted and change size when clicked or hovered.

    PolygonTextInput and BorderedPolygonTextInput types are not supported.
    
    Notes
    -----
    - if text_input is a RectTextInput or BorderedRectTextInput then normal_size, hover_size and click_size should be a tuple in the form (width, height)
    - if text_input is a CircleTextInput or BorderedCircleTextInput then normal_size, hover_size and click_size should be a single int corresponding to the radius
    """
    
    assign_variables(text_input)
    
    button_object = text_input.input_button.button_object

    text_input.on_selected = on_selected_func
    text_input.on_deselect = on_deselect_func

    size_change.change_existing_button(button_object, normal_size, hover_size, click_size)
    colour_change.assign_variables(button_object, deselected_colour, deselected_colour, selected_colour, None, None, None)