from . import slider
from . import pygame


#NOTE: pygame font background colour can be none, use dicts in presets to allow multiple different objects per preset


stored_variables = {}


def assign_variables(slider_object: slider.HorizontalSlider | slider.VerticalSlider, surface: pygame.Surface, font_name: str | None, font_size: int, font_colour: tuple[int], antialias: bool, x: int, y: int, int_only: bool) -> None:
    current_variables = {
        "surface" : surface,

        "font" : pygame.font.Font(font_name, font_size),
        "font_colour" : font_colour,
        "antialias" : antialias,

        "text_x" : x,
        "text_y" : y,

        "use_int" : int_only
    }
    
    stored_variables[slider_object] = current_variables

    on_value_changed(slider_object.value, slider_object)


def on_value_changed(value: float, slider_object: slider.HorizontalSlider | slider.VerticalSlider) -> None:
    variables = stored_variables[slider_object]
    
    if variables["use_int"]:
        value = str(int(value))
    else:
        value = f"{value :.1f}"

    text_surface = variables["font"].render(value, variables["antialias"], variables["font_colour"])

    text_rect = text_surface.get_rect()
    text_rect.center = (variables["text_x"], variables["text_y"])

    variables["text_surface"] = text_surface
    variables["text_rect"] = text_rect

    variables["surface"].blit(text_surface, text_rect)


def get_slider(is_horizontal: bool, surface: pygame.Surface, length: int, width: int, x: int, y: int, min_value: float, max_value: float, start_value: float, slider_colour: tuple[int], slider_button: object | None):
    if is_horizontal:
        slider_object = slider.HorizontalSlider(surface, length, width, x, y, min_value, max_value, start_value, slider_colour, on_value_changed, slider_button)
    else:
        slider_object = slider.VerticalSlider(surface, length, width, x, y, min_value, max_value, start_value, slider_colour, on_value_changed, slider_button)

    return slider_object


def blit_slider_text(slider_object: slider.HorizontalSlider | slider.VerticalSlider) -> None:
    """
    Should be called once per frame
    """
    
    variables = stored_variables[slider_object]

    variables["surface"].blit(variables["text_surface"], variables["text_rect"])


def create_slider_text(surface: pygame.Surface, slider_x: int, slider_y: int, text_x: int, text_y: int, slider_length: int, slider_width: int, min_value: float, max_value: float, start_value: float, slider_colour: tuple[int], font_name: str | None, font_size: int, font_colour: tuple[int], antialias: bool = False, horizontal_slider: bool = True, int_only: bool = False, slider_button: object | None = None) -> slider.HorizontalSlider | slider.VerticalSlider:
    slider_object = get_slider(horizontal_slider, surface, slider_length, slider_width, slider_x, slider_y, min_value, max_value, start_value, slider_colour, slider_button)
    
    assign_variables(slider_object, surface, font_name, font_size, font_colour, antialias, text_x, text_y, int_only)
    
    return slider_object