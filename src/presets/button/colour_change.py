from . import button
from . import utils
from . import pygame


def assign_variables(normal_colour: tuple[int], hover_colour: tuple[int], click_colour: tuple[int], on_normal: callable, on_hover: callable, on_click: callable) -> None:
    global button_normal, button_hover, button_click
    global normal_func, hover_func, click_func

    button_normal = normal_colour
    button_hover = hover_colour
    button_click = click_colour

    normal_func = on_normal
    hover_func = on_hover
    click_func = on_click


def on_click_func(button_object: button.RectButton) -> None:
    utils.call_func(click_func, button_object)

    button_object.background_colour = button_click


def on_hover_func(button_object: button.RectButton) -> None:
    utils.call_func(hover_func, button_object)

    button_object.background_colour = button_hover


def on_normal_func(button_object: button.RectButton) -> None:
    utils.call_func(normal_func, button_object)

    button_object.background_colour = button_normal


def create_button(normal_colour: tuple[int], hover_colour: tuple[int], click_colour: tuple[int], surface: pygame.Surface, x: int, y: int, width: int, height: int, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, corner_radius: int = -1) -> button.RectButton:
    assign_variables(normal_colour, hover_colour, click_colour, on_normal, on_hover, on_click)

    button_object = button.RectButton(surface, x, y, normal_colour, width, height, on_click_func, on_hover_func, on_normal_func, corner_radius, False)
    return button_object