from . import button
from . import pygame


stored_variables = {}


def assign_variables(button_object: button.RectButton, normal_size: tuple[int], hover_size: tuple[int], click_size: tuple[int], on_normal: callable, on_hover: callable, on_click: callable) -> None:
    current_variables = {
        "normal_size" : normal_size,
        "hover_size" : hover_size,
        "click_size" : click_size,

        "on_normal" : on_normal,
        "on_hover" : on_hover,
        "on_click" : on_click
    }

    stored_variables[button_object] = current_variables


def update_button_size(button_object: button.RectButton, event_type: str) -> None:
    variables = stored_variables[button_object]

    button_object.call_func(variables[f"on_{event_type}"])

    size = variables[f"{event_type}_size"]
    button_object.width = size[0]
    button_object.height = size[1]


def on_click_func(button_object: button.RectButton) -> None:
    update_button_size(button_object, "click")


def on_hover_func(button_object: button.RectButton) -> None:
    update_button_size(button_object, "hover")


def on_normal_func(button_object: button.RectButton) -> None:
    update_button_size(button_object, "normal")


def create_button(normal_size: tuple[int], hover_size: tuple[int], click_size: tuple[int], surface: pygame.Surface, x: int, y: int, background_colour: tuple[int], on_click: callable = None, on_hover: callable = None, on_normal: callable = None, corner_radius: int = -1) -> button.RectButton:
    """
    size variables are in the form (width, height)
    """
    button_object = button.RectButton(surface, x, y, background_colour, normal_size[0], normal_size[1], on_click_func, on_hover_func, on_normal_func, corner_radius, False)
    
    assign_variables(button_object, normal_size, hover_size, click_size, on_normal, on_hover, on_click)

    return button_object