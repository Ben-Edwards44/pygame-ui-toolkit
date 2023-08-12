from . import button
from . import utils
from . import pygame


#TO DO: docstrings, (possibly) slider with value text


class Slider:
    def __init__(self, surface: pygame.Surface, length: int, width: int, x: int, y: int, min_value: float, max_value: float, start_value: float, slider_colour: tuple[int], on_value_changed: callable = None, slider_button: object | None = None, button_colour: tuple[int] = (255, 255, 255), button_width: int = 20, button_height: int = 20) -> None:
        self.surface = surface
        
        self.length = length
        self.width = width

        self.x = x
        self.y = y

        self.min_value = min_value
        self.max_value = max_value
        self.value = start_value
        self.prev_value = start_value

        self.slider_colour = slider_colour

        self.on_value_changed = on_value_changed

        if slider_button == None:
            self.slider_button = self.default_button(button_colour, button_width, button_height)
        else:
            self.slider_button = slider_button

        self.normal_button_on_click = self.slider_button.on_click

        self.check_start_in_range(min_value, max_value, start_value)
        self.setup_button()

    def check_start_in_range(self, min_value: float, max_value: float, value: float) -> None:
        if value < min_value:
            raise Exception("Start value less than min value")
        elif value > max_value:
            raise Exception("Start value greater than max value")

    def default_button(self, colour: tuple[int], width: int, height: int) -> button.RectButton:
        btn = button.RectButton(self.surface, 0, 0, colour, width, height)

        return btn

    def setup_button(self) -> None:
        self.slider_button.click_once = False
        self.slider_button.on_click = self.on_slider_button_click

        x, y = self.get_button_pos(self.value)

        self.slider_button.x = int(x)
        self.slider_button.y = int(y)

    def on_slider_button_click(self) -> None:
        self.slider_button.call_func(self.normal_button_on_click)

        x, y = pygame.mouse.get_pos()

        self.slider_button.x = x
        self.slider_button.y = y

        self.clamp_button_pos()

        self.value = self.get_value()

    def update(self) -> None:
        self.draw()
        self.slider_button.update()

        if self.value != self.prev_value:
            utils.call_func(self.on_value_changed, self.value)

            self.prev_value = self.value

    
class HorizontalSlider(Slider):
    def __init__(self, surface: pygame.Surface, length: int, height: int, x: int, y: int, min_value: float, max_value: float, start_value: float, slider_colour: tuple[int], on_value_changed: callable = None, slider_button: object | None = None, button_colour: tuple[int] = (255, 255, 255), button_width: int = 10, button_height: int = 20) -> None:
        super().__init__(surface, length, height, x, y, min_value, max_value, start_value, slider_colour, on_value_changed, slider_button, button_colour, button_width, button_height)

    def get_button_pos(self, value: float) -> tuple[int]:
        value_range = self.max_value - self.min_value
        proportion = (value - self.min_value) / value_range
        dist_from_left = self.length * proportion

        min_x = self.x - self.length // 2

        return min_x + dist_from_left, self.y

    def clamp_button_pos(self) -> None:
        min_x = self.x - self.length // 2
        max_x = self.x + self.length // 2

        if self.slider_button.x < min_x:
            self.slider_button.x = min_x
        elif self.slider_button.x > max_x:
            self.slider_button.x = max_x

        self.slider_button.y = self.y

    def get_value(self) -> float:
        dist_from_left = self.slider_button.x - (self.x - self.length // 2)
        proportion = dist_from_left / self.length
        range = self.max_value - self.min_value

        return self.min_value + proportion * range
    
    def draw(self) -> None:
        rect = pygame.Rect(self.x - self.length // 2, self.y - self.width // 2, self.length, self.width)
        pygame.draw.rect(self.surface, self.slider_colour, rect)


class VerticalSlider(Slider):
    def __init__(self, surface: pygame.Surface, length: int, width: int, x: int, y: int, min_value: float, max_value: float, start_value: float, slider_colour: tuple[int], on_value_changed: callable = None, slider_button: object | None = None, button_colour: tuple[int] = (255, 255, 255), button_width: int = 20, button_height: int = 10) -> None:
        super().__init__(surface, length, width, x, y, min_value, max_value, start_value, slider_colour, on_value_changed, slider_button, button_colour, button_width, button_height)

    def get_button_pos(self, value: float) -> tuple[int]:
        value_range = self.max_value - self.min_value
        proportion = (value - self.min_value) / value_range
        dist_from_top = self.length * proportion

        min_y = self.y - self.length // 2

        return self.x, min_y + dist_from_top

    def clamp_button_pos(self) -> None:
        min_y = self.y - self.length // 2
        max_y = self.y + self.length // 2

        if self.slider_button.y < min_y:
            self.slider_button.y = min_y
        elif self.slider_button.y > max_y:
            self.slider_button.y = max_y

        self.slider_button.x = self.x

    def get_value(self) -> float:
        dist_from_top = self.slider_button.y - (self.y - self.length // 2)
        proportion = dist_from_top / self.length
        range = self.max_value - self.min_value
        value = self.min_value + proportion * range

        return self.max_value - value
    
    def draw(self) -> None:
        rect = pygame.Rect(self.x - self.width // 2, self.y - self.length // 2, self.width, self.length)
        pygame.draw.rect(self.surface, self.slider_colour, rect)