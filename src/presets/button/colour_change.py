from . import button
from . import pygame


stored_variables = {}


def assign_variables(button_object: button.RectButton, normal_colour: tuple[int], hover_colour: tuple[int], click_colour: tuple[int], on_normal: callable, on_hover: callable, on_click: callable) -> None:
    current_variables = {
        "normal_colour" : normal_colour,
        "hover_colour" : hover_colour,
        "click_colour" : click_colour,

        "on_normal" : on_normal,
        "on_hover" : on_hover,
        "on_click" : on_click
    }

    stored_variables[button_object] = current_variables


def update_button_colour(button_object: button.RectButton, event_type: str) -> None:
    variables = stored_variables[button_object]

    button_object.call_func(variables[f"on_{event_type}"])

    button_object.background_colour = variables[f"{event_type}_colour"]


def on_click_func(button_object: button.RectButton) -> None:
    update_button_colour(button_object, "click")


def on_hover_func(button_object: button.RectButton) -> None:
    update_button_colour(button_object, "hover")


def on_normal_func(button_object: button.RectButton) -> None:
    update_button_colour(button_object, "normal")


def create_button(normal_colour: tuple[int], hover_colour: tuple[int], click_colour: tuple[int], surface: pygame.Surface, x: int, y: int, width: int, height: int, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, corner_radius: int = -1) -> button.RectButton:
    button_object = button.RectButton(surface, x, y, normal_colour, width, height, on_click_func, on_hover_func, on_normal_func, corner_radius, False)
    
    assign_variables(button_object, normal_colour, hover_colour, click_colour, on_normal, on_hover, on_click)

    return button_object


def change_existing_button(button_object: button.PolygonButton, normal_colour: tuple[int], hover_colour: tuple[int], click_colour: tuple[int]):
    on_click = button_object.on_click
    on_hover = button_object.on_hover
    on_normal = button_object.on_normal
    
    button_object.on_click = on_click_func
    button_object.on_hover = on_hover_func
    button_object.on_normal = on_normal_func

    button_object.click_once = False

    assign_variables(button_object, normal_colour, hover_colour, click_colour, on_normal, on_hover, on_click)