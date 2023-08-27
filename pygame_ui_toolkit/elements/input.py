from pygame_ui_toolkit.elements import button
from pygame_ui_toolkit import utils
from pygame_ui_toolkit import pygame


class TextInput:
    """
    The base class for all text inputs.

    This class can be used on its own, although the input_button object must be made manually.

    Attributes
    ----------
    font_colour : tuple[int]
        the colour of the displayed text
    font_name : str
        the name of, or path to, the font of the displayed text
    font_size : int
        the size of the displayed text
    og_font_size : int
        the origional font size, before it is changed in the update_font_size() method
    min_font_size : int
        the minimum font size
    on_selected : callable | None, optional
        the function called every frame when the input is selected, self is passed in as the first argument (defaults to None)
    on_deselect : callable | None, optional
        the function called every frame when the input is not selected, self is passed in as the first argument (defaults to None)
    on_text_input : callable | None, optional
        the fucntion called when text is inputted into the input. The inputted text is passed into the first argument and self is passed into the second argument (defaults to None)
    text : str
        the text that has been inputted into the input
    prefix_text : str, optional
        text displayed before the inputted text on the input (defaults to "")
    antialias : bool, optional
        whether the text is drawn with antialias (defaults to False)
    change_font_size : bool, optional
        whether the font size is automatically updated when text gets too wide (defaults to True)
    input_button : button.TextWrapper
        the button text wrapper object that handles detecting events such as clicks
    normal_button_on_click : callable | None
        the input_button on_click attribute before it is changed
    selected : bool
        whether the text input is currently selected

    Methods
    -------
    create_text_wrapper(input_button: object)
        return a button.TextWrapper object
    setup_button()
        change the input button on_click attribute
    on_click()
        set selected to True and call necessary functions
    check_deselect()
        check whether mouse is outside of button and is clicking
    take_input(pygame_event_loop: pygame.event.Event)
        loop through event loop and append any key presses to self.text
    text_too_large()
        return whether the text overfits the input button
    update_font_size()
        shrink text until it fits the input button
    draw()
        draw the input button and text to the screen
    update()
        update the TextInput object
    """

    def __init__(self, input_button: object, font_colour: tuple[int], font_size: int, font_name: str | None = None, on_selected: callable = None, on_deselect: callable = None, on_text_input: callable = None, start_text: str = "", prefix_text: str = "", min_font_size: int = 10, change_font_size: bool = True, antialias: bool = False) -> None:
        """Construct the necessary attributes for the TextWrapper object."""
        self.font_colour = font_colour
        self.font_name = font_name

        self.font_size = font_size
        self.og_font_size = font_size
        self.min_font_size = min_font_size

        self.on_selected = on_selected
        self.on_deselect = on_deselect
        self.on_text_input = on_text_input

        self.text = start_text
        self.prefix_text = prefix_text

        self.antialias = antialias
        self.change_font_size = change_font_size

        self.input_button = self.create_text_wrapper(input_button)
        self.normal_button_on_click = self.input_button.button_object.on_click

        self.setup_button()

        self.selected = False

    def create_text_wrapper(self, input_button: object) -> button.TextWrapper:
        """Return a button.TextWrapper object."""
        if type(input_button) == button.TextWrapper:
            return input_button
        else:
            text_wrapper = button.TextWrapper(input_button, self.text, self.font_colour, self.font_size, self.font_name, self.antialias)

            return text_wrapper
        
    def setup_button(self) -> None:
        """Change the input button on_click attribute."""
        self.input_button.button_object.on_click = self.on_click
        
    def on_click(self) -> None:
        """Set selected to True and call necessary functions."""
        self.input_button.button_object.call_func(self.normal_button_on_click)
        self.selected = True
        utils.call_func(self.on_selected, self)

    def check_deselect(self) -> None:
        """Check whether mouse is outside of button and is clicking."""
        if pygame.mouse.get_pressed()[0] and not self.input_button.button_object.mouse_over():
            self.selected = False
            utils.call_func(self.on_deselect, self)

    def take_input(self, pygame_event_loop: list[pygame.event.Event]) -> None:
        """Loop through event loop and append any key presses to self.text."""     
        for event in pygame_event_loop:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

                utils.call_func(self.on_text_input, self.text, self)

    def text_too_large(self) -> bool:
        """Return whether the text overfits the input button."""
        text_rect = self.input_button.get_text()[1]
        text_width = text_rect.width
        btn_width = self.input_button.button_object.get_width()

        return text_width > btn_width

    def update_font_size(self) -> None:
        """Shrink text until it fits the input button."""
        self.font_size = self.og_font_size
        self.input_button.font = pygame.font.Font(self.font_name, self.font_size)

        while self.text_too_large() and self.font_size > self.min_font_size:
            self.font_size -= 1
            self.input_button.font = pygame.font.Font(self.font_name, self.font_size)

    def draw(self) -> None:
        """Draw the input button and text to the screen."""
        self.input_button.update_text(f"{self.prefix_text}{self.text}", self.font_colour, self.font_size, self.font_name)
        self.input_button.update()

    def update(self, pygame_event_loop: list[pygame.event.Event]) -> None:
        """
        Update the TextInput object.

        This should be called once per frame.
        """
        self.check_deselect()

        if self.change_font_size:
            self.update_font_size()

        if self.selected:
            self.take_input(pygame_event_loop)

        self.draw()


class RectTextInput(TextInput):
    """
    A text input in the shape of a rectangle.

    Inherits from TextInput

    Attributes
    ----------
    all attributes from TextInput

    Methods
    -------
    all methods from TextInput
    create_button(surface: pygame.Surface, x: int, y: int, background_colour: tuple[int], width: int, height: int, on_click: callable, on_hover: callable, on_normal: callable, corner_radius: int, click_once: bool)
        return a button object with the appropriate shape
    """

    def __init__(self, surface: pygame.Surface, x: int, y: int, background_colour: tuple[int],  width: int, height: int, font_colour: tuple[int], font_size: int, font_name: str | None = None, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, on_selected: callable = None, on_deselect: callable = None, on_text_input: callable = None, corner_radius: int = -1, click_once: bool = True, text: str = "", prefix_text: str = "", min_font_size: int = 10, change_font_size: bool = True, antialias: bool = False) -> None:
        """Construct the necessary attributes for the RectTextInput object."""
        input_button = self.create_button(surface, x, y, background_colour, width, height, on_click, on_hover, on_normal, corner_radius, click_once)
        
        super().__init__(input_button, font_colour, font_size, font_name, on_selected, on_deselect, on_text_input, text, prefix_text, min_font_size, change_font_size, antialias)

    def create_button(self, surface: pygame.Surface, x: int, y: int, background_colour: tuple[int], width: int, height: int, on_click: callable, on_hover: callable, on_normal: callable, corner_radius: int, click_once: bool) -> button.RectButton:
        """Return a button object with the appropriate shape."""
        btn = button.RectButton(surface, x, y, background_colour, width, height, on_click, on_hover, on_normal, corner_radius, click_once)

        return btn
    

class CircleTextInput(TextInput):
    """
    A text input in the shape of a circle.

    Inherits from TextInput.

    Attributes
    ----------
    all attributes from TextInput

    Methods
    -------
    all methods from TextInput
    create_button(surface: pygame.Surface, x: int, y: int, background_colour: tuple[int], width: int, height: int, on_click: callable, on_hover: callable, on_normal: callable, corner_radius: int, click_once: bool)
        return a button object with the appropriate shape
    """
    
    def __init__(self, surface: pygame.Surface, x: int, y: int, background_colour: tuple[int],  radius: int, font_colour: tuple[int], font_size: int, font_name: str | None = None, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, on_selected: callable = None, on_deselect: callable = None, on_text_input: callable = None, click_once: bool = True, text: str = "", prefix_text: str = "", min_font_size: int = 10, change_font_size: bool = True, antialias: bool = False) -> None:
        """Construct the necessary attributes for the CircleTextInput object."""
        input_button = self.create_button(surface, x, y, background_colour, radius, on_click, on_hover, on_normal, click_once)
        
        super().__init__(input_button, font_colour, font_size, font_name, on_selected, on_deselect, on_text_input, text, prefix_text, min_font_size, change_font_size, antialias)

    def create_button(self, surface: pygame.Surface, x: int, y: int, background_colour: tuple[int], radius: int, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, click_once: bool = True) -> button.CircleButton:
        """Return a button object with the appropriate shape."""
        btn = button.CircleButton(surface, x, y, background_colour, radius, on_click, on_hover, on_normal, click_once)

        return btn
    

class PolygonTextInput(TextInput):
    """
    A text input in the shape of any convex polygon.
    Concave polygons are not supported and will result in unexpected behaviour.

    Inherits from TextInput.

    Attributes
    ----------
    all attributes from TextInput

    Methods
    -------
    all methods from TextInput
    create_button(surface: pygame.Surface, x: int, y: int, background_colour: tuple[int], width: int, height: int, on_click: callable, on_hover: callable, on_normal: callable, corner_radius: int, click_once: bool)
        return a button object with the appropriate shape
    """
    
    def __init__(self, surface: pygame.Surface, points: list[tuple[int]], background_colour: tuple[int], font_colour: tuple[int], font_size: int, font_name: str | None = None, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, on_selected: callable = None, on_deselect: callable = None, on_text_input: callable = None, click_once: bool = True, text: str = "", prefix_text: str = "", min_font_size: int = 10, antialias: bool = False) -> None:
        """Construct the necessary attributes for the PolygonTextInput object."""
        input_button = self.create_button(surface, points, background_colour, on_click, on_hover, on_normal, click_once)
        
        super().__init__(input_button, font_colour, font_size, font_name, on_selected, on_deselect, on_text_input, text, prefix_text, min_font_size, False, antialias)

    def create_button(self, surface: pygame.Surface, points: list[tuple[int]], background_colour: tuple[int], on_click: callable = None, on_hover: callable = None, on_normal: callable = None, click_once: bool = True) -> button.PolygonButton:
        """Return a button object with the appropriate shape."""
        btn = button.PolygonButton(surface, points, background_colour, on_click, on_hover, on_normal, click_once)

        return btn


class BorderedRectTextInput(TextInput):
    """
    A text input in the shape of a rectangle with a border.

    Inherits from TextInput.

    Attributes
    ----------
    all attributes from TextInput

    Methods
    -------
    all methods from TextInput
    create_button(surface: pygame.Surface, x: int, y: int, background_colour: tuple[int], width: int, height: int, on_click: callable, on_hover: callable, on_normal: callable, corner_radius: int, click_once: bool)
        return a button object with the appropriate shape
    """

    def __init__(self, surface: pygame.Surface, x: int, y: int, background_colour: tuple[int], border_colour: tuple[int], width: int, height: int, border_width: int, font_colour: tuple[int], font_size: int, font_name: str | None = None, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, on_selected: callable = None, on_deselect: callable = None, on_text_input: callable = None, corner_radius: int = -1, click_once: bool = True, text: str = "", prefix_text: str = "", min_font_size: int = 10, change_font_size: bool = True, antialias: bool = False) -> None:
        """Construct the necessary attributes for the BorderedRectTextInput object."""
        input_button = self.create_button(surface, x, y, background_colour, border_colour, width, height, border_width, on_click, on_hover, on_normal, corner_radius, click_once)
        
        super().__init__(input_button, font_colour, font_size, font_name, on_selected, on_deselect, on_text_input, text, prefix_text, min_font_size, change_font_size, antialias)

    def create_button(self, surface: pygame.Surface, x: int, y: int, background_colour: tuple[int], border_colour: tuple[int], width: int, height: int, border_width: int, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, corner_radius: int = -1, click_once: bool = True) -> button.BorderedRectButton:
        """Return a button object with the appropriate shape."""
        btn = button.BorderedRectButton(surface, x, y, background_colour, border_colour, width, height, border_width, on_click, on_hover, on_normal, corner_radius, click_once)

        return btn


class BorderedCircleTextInput(TextInput):
    """
    A text input in the shape of a circle with a border.

    Inherits from TextInput.

    Attributes
    ----------
    all attributes from TextInput

    Methods
    -------
    all methods from TextInput
    create_button(surface: pygame.Surface, x: int, y: int, background_colour: tuple[int], width: int, height: int, on_click: callable, on_hover: callable, on_normal: callable, corner_radius: int, click_once: bool)
        return a button object with the appropriate shape
    """

    def __init__(self, surface: pygame.Surface, x: int, y: int, background_colour: tuple[int],  border_colour: tuple[int], radius: int, border_width: int, font_colour: tuple[int], font_size: int, font_name: str | None = None, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, on_selected: callable = None, on_deselect: callable = None, on_text_input: callable = None, click_once: bool = True, text: str = "", prefix_text: str = "", min_font_size: int = 10, change_font_size: bool = True, antialias: bool = False) -> None:
        """Construct the necessary attributes for the BorderedCircleTextInput object."""
        input_button = self.create_button(surface, x, y, background_colour, border_colour, radius, border_width, on_click, on_hover, on_normal, click_once)
        
        super().__init__(input_button, font_colour, font_size, font_name, on_selected, on_deselect, on_text_input, text, prefix_text, min_font_size, change_font_size, antialias)

    def create_button(self, surface: pygame.Surface, x: int, y: int, background_colour: tuple[int], border_colour: tuple[int], radius: int, border_width: int, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, click_once: bool = True) -> button.BorderedCircleButton:
        """Return a button object with the appropriate shape."""
        btn = button.BorderedCircleButton(surface, x, y, background_colour, border_colour, radius, border_width, on_click, on_hover, on_normal, click_once)

        return btn
    

class BorderedPolygonTextInput(TextInput):
    """
    A text input in the shape of any convex polygon with a border.
    Concave polygons are not supported and will result in unexpected behaviour.

    Inherits from TextInput.

    Attributes
    ----------
    all attributes from TextInput

    Methods
    -------
    all methods from TextInput
    create_button(surface: pygame.Surface, x: int, y: int, background_colour: tuple[int], width: int, height: int, on_click: callable, on_hover: callable, on_normal: callable, corner_radius: int, click_once: bool)
        return a button object with the appropriate shape
    """

    def __init__(self, surface: pygame.Surface, points: list[tuple[int]], background_colour: tuple[int], border_colour: tuple[int], border_width: int, font_colour: tuple[int], font_size: int, font_name: str | None = None, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, on_selected: callable = None, on_deselect: callable = None, on_text_input: callable = None, click_once: bool = True, text: str = "", prefix_text: str = "", min_font_size: int = 10, antialias: bool = False) -> None:
        """Construct the necessary attributes for the BorderedPolygonTextInput object."""
        input_button = self.create_button(surface, points, background_colour, border_colour, border_width, on_click, on_hover, on_normal, click_once)
        
        super().__init__(input_button, font_colour, font_size, font_name, on_selected, on_deselect, on_text_input, text, prefix_text, min_font_size, False, antialias)

    def create_button(self, surface: pygame.Surface, points: list[tuple[int]], background_colour: tuple[int], border_colour: tuple[int], border_width: int, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, click_once: bool = True) -> button.BorderedPolygonButton:
        """Return a button object with the appropriate shape."""
        btn = button.BorderedPolygonButton(surface, points, background_colour, border_colour, border_width, on_click, on_hover, on_normal, click_once)

        return btn