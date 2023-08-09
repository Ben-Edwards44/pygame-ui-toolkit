from . import button
from . import utils
from . import pygame


# TODO: base toggle class - [setup text wrapper button, update], (possibly) seperate classes for each button, default tick/cross


class Toggle:
    def __init__(self, button_object: object, text: str = "", on_value_changed: callable = None) -> None:
        pass

    def setup_button(self) ->