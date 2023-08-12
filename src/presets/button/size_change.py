from . import button
from . import utils
from . import pygame


def assign_variables(normal_size: tuple[int], hover_size: tuple[int], click_size: tuple[int], on_normal: callable, on_hover: callable, on_click: callable) -> None:
    global button_normal, button_hover, button_click
    global normal_func, hover_func, click_func

    button_normal = normal_size
    button_hover = hover_size
    button_click = click_size

    normal_func = on_normal
    hover_func = on_hover
    click_func = on_click


def on_click_func(button_object: button.RectButton) -> None:
    utils.call_func(click_func, button_object)

    button_object.width = button_click[0]
    button_object.height = button_click[1]


def on_hover_func(button_object: button.RectButton) -> None:
    utils.call_func(hover_func, button_object)

    button_object.width = button_hover[0]
    button_object.height = button_hover[1]


def on_normal_func(button_object: button.RectButton) -> None:
    utils.call_func(normal_func, button_object)

    button_object.width = button_normal[0]
    button_object.height = button_normal[1]


def create_button(normal_size: tuple[int], hover_size: tuple[int], click_size: tuple[int], surface: pygame.Surface, x: int, y: int, background_colour: tuple[int], on_click: callable = None, on_hover: callable = None, on_normal: callable = None, corner_radius: int = -1) -> button.RectButton:
    """
    size variables are in the form (width, height)
    """
    
    assign_variables(normal_size, hover_size, click_size, on_normal, on_hover, on_click)

    button_object = button.RectButton(surface, x, y, background_colour, normal_size[0], normal_size[1], on_click_func, on_hover_func, on_normal_func, corner_radius, False)
    return button_object