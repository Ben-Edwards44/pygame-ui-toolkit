from pygame_ui_toolkit.elements import button
from pygame_ui_toolkit import utils
from pygame_ui_toolkit import pygame


class Slider:
    """
    The base slider class that both HorizontalSlider and VerticalSlider inherit from.

    Do not use this class on its own.
    Instead, use either HorizontalSlider or VerticalSlider.

    Attributes
    ----------
    surface : pygame.Surface
        the surface which the slider is drawn to
    length : int
        the length of the long side of the slider
    width : int
        the length of the short side of the slider
    x : int
        the x coordinate of the slider's position
    y : int
        the y coordinate of the slider's position
    min_value : float
        the minimum value the slider can be
    max_value : float
        the maximum value the slider can be
    value : float
        the current slider value
    prev_value : float
        the value of the slider before it is changed
    slider_colour : tuple[int]
        the colour of the slider
    on_value_changed : callable | None, optional
        the function that is called when the slider value is changed. If it accepts 1 argument, the slider value is passed in. If it accepts 2 arguments, the slider value and self are passed in (defaults to None)
    slider_buton : object
        an object from the button module that acts as the clickable button in the slider
    normal_button_on_click : callable | None
        the button object's on_click function before it was changed in setup_button()

    Methods
    -------
    check_start_in_range(self, min_value: float, max_value: float, value: float)
        raise an exception if the value is outside of the range
    setup_button()
        prepare the slider button object for use
    on_slider_button_click()
        call the normal_button_on_click() and update button pos to mouse pos
    update()
        draw slider to the screen, update the slider button object and call on_value_changed if necessary
    """

    def __init__(self, surface: pygame.Surface, length: int, width: int, x: int, y: int, min_value: float, max_value: float, start_value: float, slider_colour: tuple[int], on_value_changed: callable = None, slider_button: object | None = None, button_colour: tuple[int] = (255, 255, 255), button_radius: int | None = None) -> None:
        """Construct the necessary attributes for the Slider object."""
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
            if button_radius == None:
                button_radius = width

            self.slider_button = button.CircleButton(surface, 0, 0, button_colour, button_radius)
        else:
            self.slider_button = slider_button

        self.normal_button_on_click = self.slider_button.on_click

        self.check_start_in_range(min_value, max_value, start_value)
        self.setup_button()

    def check_start_in_range(self, min_value: float, max_value: float, value: float) -> None:
        """Raise an exception if the value is outside of the range."""
        if value < min_value:
            raise Exception("Start value less than min value")
        elif value > max_value:
            raise Exception("Start value greater than max value")

    def setup_button(self) -> None:
        """Prepare the slider button object for use."""
        self.slider_button.click_once = False
        self.slider_button.on_click = self.on_slider_button_click

        x, y = self.get_button_pos(self.value)

        self.slider_button.x = int(x)
        self.slider_button.y = int(y)

    def on_slider_button_click(self) -> None:
        """Call the normal_button_on_click() and update button pos to mouse pos."""
        self.slider_button.call_func(self.normal_button_on_click)

        x, y = pygame.mouse.get_pos()

        self.slider_button.x = x
        self.slider_button.y = y

        self.clamp_button_pos()

        self.value = self.get_value()

    def update(self) -> None:
        """
        Draw slider to the screen, update the slider button object and call on_value_changed if necessary.

        This should be called once per frame.
        """
        self.draw()
        self.slider_button.update()

        if self.value != self.prev_value:
            utils.call_func(self.on_value_changed, self.value, self)

            self.prev_value = self.value

    
class HorizontalSlider(Slider):
    """
    A horizontal slider.

    This inherits from the Slider class.

    Attributes
    ----------
    All attributes are the same as the base Slider class.

    Methods
    -------
    All methods from the base Slider class
    Additional methods:
    get_button_pos()
        get the starting position of the slider button
    clamp_button_pos()
        change the button position so that it is within the slider region
    get_value()
        calculate the slider value based on the current button position
    draw()
        draw the slider bar to the screen
    """

    def __init__(self, surface: pygame.Surface, length: int, height: int, x: int, y: int, min_value: float, max_value: float, start_value: float, slider_colour: tuple[int], on_value_changed: callable = None, slider_button: object | None = None, button_colour: tuple[int] = (255, 255, 255), button_radius: int | None = None) -> None:
        """Call __init__ from parent Slider class."""
        super().__init__(surface, length, height, x, y, min_value, max_value, start_value, slider_colour, on_value_changed, slider_button, button_colour, button_radius)

    def get_button_pos(self, value: float) -> tuple[int]:
        """Get the starting position of the slider button."""
        value_range = self.max_value - self.min_value
        proportion = (value - self.min_value) / value_range
        dist_from_left = self.length * proportion

        min_x = self.x - self.length // 2

        return min_x + dist_from_left, self.y

    def clamp_button_pos(self) -> None:
        """Change the button position so that it is within the slider region."""
        min_x = self.x - self.length // 2
        max_x = self.x + self.length // 2

        if self.slider_button.x < min_x:
            self.slider_button.x = min_x
        elif self.slider_button.x > max_x:
            self.slider_button.x = max_x

        self.slider_button.y = self.y

    def get_value(self) -> float:
        """Calculate the slider value based on the current button position."""
        dist_from_left = self.slider_button.x - (self.x - self.length // 2)
        proportion = dist_from_left / self.length
        range = self.max_value - self.min_value

        return self.min_value + proportion * range
    
    def draw(self) -> None:
        """Draw the slider bar to the screen."""
        rect = pygame.Rect(self.x - self.length // 2, self.y - self.width // 2, self.length, self.width)
        pygame.draw.rect(self.surface, self.slider_colour, rect)


class VerticalSlider(Slider):
    """
    A vertical slider.

    This inherits from the Slider class.

    Attributes
    ----------
    All attributes are the same as the base Slider class.

    Methods
    -------
    All methods from the base Slider class
    Additional methods:
    get_button_pos()
        get the starting position of the slider button
    clamp_button_pos()
        change the button position so that it is within the slider region
    get_value()
        calculate the slider value based on the current button position
    draw()
        draw the slider bar to the screen
    """

    def __init__(self, surface: pygame.Surface, length: int, width: int, x: int, y: int, min_value: float, max_value: float, start_value: float, slider_colour: tuple[int], on_value_changed: callable = None, slider_button: object | None = None, button_colour: tuple[int] = (255, 255, 255), button_radius: int | None = None) -> None:
        """Call __init__ from parent Slider class."""
        super().__init__(surface, length, width, x, y, min_value, max_value, start_value, slider_colour, on_value_changed, slider_button, button_colour, button_radius)

    def get_button_pos(self, value: float) -> tuple[int]:
        """Get the starting position of the slider button."""
        value_range = self.max_value - self.min_value
        proportion = (value - self.min_value) / value_range
        dist_from_top = self.length * proportion

        min_y = self.y - self.length // 2

        return self.x, min_y + dist_from_top

    def clamp_button_pos(self) -> None:
        """Change the button position so that it is within the slider region."""
        min_y = self.y - self.length // 2
        max_y = self.y + self.length // 2

        if self.slider_button.y < min_y:
            self.slider_button.y = min_y
        elif self.slider_button.y > max_y:
            self.slider_button.y = max_y

        self.slider_button.x = self.x

    def get_value(self) -> float:
        """Calculate the slider value based on the current button position."""
        dist_from_top = self.slider_button.y - (self.y - self.length // 2)
        proportion = dist_from_top / self.length
        range = self.max_value - self.min_value
        value = self.min_value + proportion * range

        return self.max_value - value
    
    def draw(self) -> None:
        """Draw the slider bar to the screen."""
        rect = pygame.Rect(self.x - self.width // 2, self.y - self.length // 2, self.width, self.length)
        pygame.draw.rect(self.surface, self.slider_colour, rect)