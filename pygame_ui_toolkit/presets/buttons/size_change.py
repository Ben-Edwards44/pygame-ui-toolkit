from pygame_ui_toolkit.elements import button
from pygame_ui_toolkit import pygame


stored_variables = {}


def assign_variables(button_object: button.Button, normal_size: tuple[int], hover_size: tuple[int], click_size: tuple[int], on_normal: callable, on_hover: callable, on_click: callable) -> None:
    """Assign variables that need to be used later to a global dict with the button object as the key."""
    
    current_variables = {
        "normal_size" : normal_size,
        "hover_size" : hover_size,
        "click_size" : click_size,

        "on_normal" : on_normal,
        "on_hover" : on_hover,
        "on_click" : on_click
    }

    stored_variables[button_object] = current_variables


def update_button_size(button_object: button.Button, event_type: str) -> None:
    """
    Change the size of a button.
    
    An exception is raised if an unsupported button (e.g. PolygonButton is used).
    """
    
    variables = stored_variables[button_object]

    button_object.call_func(variables[f"on_{event_type}"])

    size = variables[f"{event_type}_size"]

    t = type(button_object)

    if t == button.RectButton or t == button.BorderedRectButton:
        button_object.width = size[0]
        button_object.height = size[1]
    elif t == button.CircleButton or t == button.BorderedCircleButton:
        button_object.radius = size
    else:
        raise Exception("Unsupported button type for a size change. Use any rect or circle buttons only.")


def on_click_func(button_object: button.Button) -> None:
    update_button_size(button_object, "click")


def on_hover_func(button_object: button.Button) -> None:
    update_button_size(button_object, "hover")


def on_normal_func(button_object: button.Button) -> None:
    update_button_size(button_object, "normal")


def create_button(normal_size: tuple[int], hover_size: tuple[int], click_size: tuple[int], surface: pygame.Surface, x: int, y: int, background_colour: tuple[int], on_click: callable = None, on_hover: callable = None, on_normal: callable = None, corner_radius: int = -1) -> button.RectButton:
    """
    Return a new RectButton that will automatically change size when clicked or hovered.
    
    Ensure to call the button's update() method each frame.

    Notes
    -----
    normal_size, hover_size and click_size should be provided as a tuple in the form (width, height):
    - e.g. a value of (100, 50) would result in a button with width 100 and height 50
    """

    button_object = button.RectButton(surface, x, y, background_colour, normal_size[0], normal_size[1], on_click_func, on_hover_func, on_normal_func, corner_radius, False)
    
    assign_variables(button_object, normal_size, hover_size, click_size, on_normal, on_hover, on_click)

    return button_object


def change_existing_button(button_object: object, normal_size: tuple[int] | int, hover_size: tuple[int] | int, click_size: tuple[int] | int) -> None:
    """
    Update an existing button to make it automatically change size when clicked or hovered.

    PolygonButton and BorderedPolygonButton types are not supported.

    Notes
    -----
    - this will change the click_once attribute to False
    - if button_object is a RectButton or BorderedRectButton then normal_size, hover_size and click_size should be a tuple in the form (width, height)
    - if button_object is a CircleButton or BorderedCircleButton then normal_size, hover_size and click_size should be a single int corresponding to the radius
    """
    
    on_click = button_object.on_click
    on_hover = button_object.on_hover
    on_normal = button_object.on_normal
    
    button_object.on_click = on_click_func
    button_object.on_hover = on_hover_func
    button_object.on_normal = on_normal_func

    button_object.click_once = False

    assign_variables(button_object, normal_size, hover_size, click_size, on_normal, on_hover, on_click)