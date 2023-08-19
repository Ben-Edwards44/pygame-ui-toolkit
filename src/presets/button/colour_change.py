from . import button
from . import pygame


stored_variables = {}


def assign_variables(button_object: button.Button, normal_colour: tuple[int], hover_colour: tuple[int], click_colour: tuple[int], on_normal: callable, on_hover: callable, on_click: callable) -> None:
    """Assign variables that need to be used later to a global dict with the slider object as the key."""
    
    current_variables = {
        "normal_colour" : normal_colour,
        "hover_colour" : hover_colour,
        "click_colour" : click_colour,

        "on_normal" : on_normal,
        "on_hover" : on_hover,
        "on_click" : on_click
    }

    stored_variables[button_object] = current_variables


def update_button_colour(button_object: button.Button, event_type: str) -> None:
    """Change the background colour of the button."""

    variables = stored_variables[button_object]

    button_object.call_func(variables[f"on_{event_type}"])

    button_object.background_colour = variables[f"{event_type}_colour"]


def on_click_func(button_object: button.Button) -> None:
    update_button_colour(button_object, "click")


def on_hover_func(button_object: button.Button) -> None:
    update_button_colour(button_object, "hover")


def on_normal_func(button_object: button.Button) -> None:
    update_button_colour(button_object, "normal")


def create_button(normal_colour: tuple[int], hover_colour: tuple[int], click_colour: tuple[int], surface: pygame.Surface, x: int, y: int, width: int, height: int, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, corner_radius: int = -1) -> button.RectButton:
    """
    Return a new RectButton that will automatically change colour when clicked or hovered.
    
    Ensure to call the button's update() method each frame.
    """

    button_object = button.RectButton(surface, x, y, normal_colour, width, height, on_click_func, on_hover_func, on_normal_func, corner_radius, False)
    
    assign_variables(button_object, normal_colour, hover_colour, click_colour, on_normal, on_hover, on_click)

    return button_object


def change_existing_button(button_object: button.PolygonButton, normal_colour: tuple[int], hover_colour: tuple[int], click_colour: tuple[int]) -> None:
    """
    Update an existing button to make it automatically change colour when clicked or hovered.

    Any button type (other than the base Button class) is supported.

    Note: this will change the click_once attribute to False.
    """

    on_click = button_object.on_click
    on_hover = button_object.on_hover
    on_normal = button_object.on_normal
    
    button_object.on_click = on_click_func
    button_object.on_hover = on_hover_func
    button_object.on_normal = on_normal_func

    button_object.click_once = False

    assign_variables(button_object, normal_colour, hover_colour, click_colour, on_normal, on_hover, on_click)