from . import button
from . import utils
from . import pygame


# TODO: change TickBoxToggle to use update_text() - don't forget about the docstrings


class Toggle:
    """
    The base class from which all other toggles inherit from.

    Unlike other base classes, this class can be used on its own.

    Attributes
    ----------
    button_object : object
        the button object for the toggle
    normal_button_on_click : callable | None
        the button's on_click function before it is changed by the Toggle class
    on_value_changed : callable | None, optional
        the function that is called once the value of the toggle is changed. If it accepts 0 args, the function is just called; if it accepts 1 arg, the toggle value is passed in; if it accepts 2 args, the toggle value and the toggle object are passed in (defaults to None)
    selected : bool
        whether the toggle is currently selected
    prev_selected : bool
        whether the toggle was selected on the previous frame

    Methods
    -------
    setup_button()
        prepare the button_object attribute
    on_button_click()
        toggle the selected attribute and call on_click function
    draw()
        draw the toggle to the screen
    update()
        update the Toggle object
    """

    def __init__(self, button_object: object, on_value_changed: callable = None, start_value: bool = False) -> None:
        """Construct the necessary attributes for the Toggle object."""
        self.button_object = button_object
        self.normal_button_on_click = self.button_object.on_click

        self.on_value_changed = on_value_changed

        self.selected = start_value
        self.prev_selected = start_value

        self.setup_button()
        
    def setup_button(self) -> None:
        """Prepare the button_object attribute."""
        self.button_object.click_once = True
        self.button_object.on_click = self.on_button_click

    def on_button_click(self) -> None:
        """Toggle the selected attribute and call on_click function."""
        self.button_object.call_func(self.normal_button_on_click)
        self.selected = not self.selected

    def draw(self) -> None:
        """Draw the toggle to the screen."""
        self.button_object.update()

    def update(self) -> None:
        """
        Update the Toggle object.

        This should be called once per frame.
        """
        self.draw()

        if self.selected != self.prev_selected:
            utils.call_func(self.on_value_changed, self.selected, self)
            self.prev_selected = self.selected


class TextToggle(Toggle):
    """
    A toggle with text.

    Inherits from Toggle

    Attributes
    ----------
    all attributes from Toggle
    text : str
        the text displayed on the toggle button
    text_x : int
        the x coordinate of the center of the text
    text_y : int
        the y coordinate of the center of the text
    font_colour : tuple[int]
        the colour of the displayed text
    font : pygame.Surface
        the pygame surface object used to render text
    antialias : bool
        whether the text is displayed with antialias

    Methods
    -------
    get_text()
        return a text surface and a rect object for text
    blit_text()
        draw text to the screen
    draw()
        draw the text and toggle to the screen
    """

    def __init__(self, button_object: object, text: str, text_x: int, text_y: int, font_colour: tuple[int], font_size: int, font_name: str | None = None, on_value_changed: callable = None, start_value: bool = False, antialias: bool = False) -> None:
        """Construct the necessary attributes for the TextToggle object."""
        super().__init__(button_object, on_value_changed, start_value)

        self.text = text

        self.text_x = text_x
        self.text_y = text_y

        self.font_colour = font_colour
        self.font = pygame.font.Font(font_name, font_size)

        self.antialias = antialias

    def get_text(self) -> tuple[pygame.Surface, pygame.Rect]:
        """Return a text surface and a rect object for text."""
        text_surf = self.font.render(self.text, self.antialias, self.font_colour, self.button_object.background_colour)
        text_rect = text_surf.get_rect()
        text_rect.center = (self.text_x, self.text_y)

        return text_surf, text_rect
    
    def blit_text(self) -> None:
        """Draw text to the screen."""
        surf, rect = self.get_text()
        self.button_object.surface.blit(surf, rect)

    def draw(self) -> None:
        """Draw the text and toggle to the screen."""
        self.button_object.update()
        self.blit_text()


class TickBox(Toggle):
    """
    A tick box without text.

    Inherits from Toggle.

    Attributes
    ----------
    all attributes from Toggle
    surface : pygame.Surface
        the surface that the toggle is drawn to
    tick_thickness : int
        the thickness, or line stroke, of the drawn tick
    tick_colour : tuple[int]
        the colour of the drawn tick

    Methods
    -------
    all methods from Toggle
    draw_tick()
        draw the tick to the screen
    draw()
        draw the tick box and - if appropriate - the tick to the screen
    """

    def __init__(self, surface: pygame.Surface, tick_thickness: int, tick_colour: tuple[int], x: int, y: int, background_colour: tuple[int], side_length: int, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, corner_radius: int = -1, on_value_changed: callable = None, start_value: bool = False) -> None:
        """Construct the necessary attributes for the TickBox object."""
        button_object = button.RectButton(surface, x, y, background_colour, side_length, side_length, on_click, on_hover, on_normal, corner_radius, True)
        
        self.surface = surface

        self.tick_thickness = tick_thickness
        self.tick_colour = tick_colour

        super().__init__(button_object, on_value_changed, start_value)
    
    def draw_tick(self) -> None:
        """Draw the tick to the screen."""
        width = self.button_object.width
        height = self.button_object.height

        x = self.button_object.x - width // 2
        y = self.button_object.y - height // 2

        left = (x + int(width * 0.2), y + int(height * 0.6))
        middle = (x + int(width * 0.4), y + int(height * 0.9))
        right = (x + int(width * 0.9), y + int(height * 0.2))

        pygame.draw.line(self.surface, self.tick_colour, left, middle, self.tick_thickness)
        pygame.draw.line(self.surface, self.tick_colour, middle, right, self.tick_thickness)

    def draw(self) -> None:
        """Draw the tick box and - if appropriate - the tick to the screen."""
        self.button_object.update()

        if self.selected:
            self.draw_tick()


class TickBoxToggle:
    """
    A tick box toggle with text.

    Attributes
    ----------
    surface : pygame.Surface
        the surface that the toggle is drawn upon
    x : int
        the x coordinate of the toggle
    y : int
        the y coordinate of the toggle
    width : int
        the width of the toggle
    height : int
        the height of the toggle
    outer_box_colour : tuple[int]
        the colour of the outer box (the text box)
    outer_box_corner_radius : int, optional
        the radius of the rounded corners of the outer box, where -1 means no rounded corners (defaults to -1)
    text_to_right : bool, optional
        whether the text is drawn to the right of the tick box (defaults to True)
    tick_box : TickBox
        the tick box object for the toggle
    text_surface : pygame.Surface
        the surface object used to render text
    text_rect : pygame.Rect
        the rect position that the text is drawn to

    Methods
    -------
    create_tick_box(tick_thickness: int, tick_colour: tuple[int], background_colour: tuple[int], dist_from_edge: int, height_offset: int, on_click: callable, on_hover: callable, on_normal: callable, on_value_changed: callable, corner_radius: int, start_value: bool)
        return the tick box object with the appropriate size and position
    find_text_pos()
        return the x, y position of the text
    get_text()
        return the text surface and rect objects to draw text
    draw()
        draw the outer box, tick box and text to the screen
    update()
        update the TickBoxToggle object
    """

    def __init__(self, surface: pygame.Surface, tick_thickness: int, tick_colour: tuple[int], tick_box_colour: tuple[int], outer_box_colour: tuple[int], x: int, y: int, width: int, height: int, text: str, font_colour: tuple[int], font_size: int, font_name: str | None = None, dist_from_edge: int = 5, height_offset: int = 10, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, on_value_changed: callable = None, inner_corner_radius: int = -1, outer_corner_radius: int = -1, start_value: bool = False, text_to_right: bool = True, antialias: bool = False) -> None:
        """Construct the necessary attributes for the TickBoxToggle object."""
        self.surface = surface

        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.outer_box_colour = outer_box_colour
        self.outer_corner_radius = outer_corner_radius

        self.text_to_right = text_to_right

        self.tick_box = self.create_tick_box(tick_thickness, tick_colour, tick_box_colour, dist_from_edge, height_offset, on_click, on_hover, on_normal, on_value_changed, inner_corner_radius, start_value)
        self.text_surface, self.text_rect = self.get_text(text, font_name, font_size, font_colour, antialias)

    def create_tick_box(self, tick_thickness: int, tick_colour: tuple[int], background_colour: tuple[int], dist_from_edge: int, height_offset: int, on_click: callable, on_hover: callable, on_normal: callable, on_value_changed: callable, corner_radius: int, start_value: bool) -> TickBox:
        """Return the tick box object with the appropriate size and position."""
        new_height = self.height - height_offset

        if self.text_to_right:
            new_x = (self.x - self.width // 2) + (new_height // 2) + dist_from_edge
        else:
            new_x = (self.x + self.width // 2) - (new_height // 2) - dist_from_edge
        
        return TickBox(self.surface, tick_thickness, tick_colour, new_x, self.y, background_colour, new_height, on_click, on_hover, on_normal, corner_radius, on_value_changed, start_value)
    
    def find_text_pos(self) -> tuple[int, int]: 
        """Return the x, y position of the text."""    
        dist_to_center = self.tick_box.button_object.width // 2

        if self.text_to_right:
            x1 = self.x + self.width // 2
            x2 = self.tick_box.button_object.x + dist_to_center
        else:
            x1 = self.x - self.width // 2
            x2 = self.tick_box.button_object.x - dist_to_center

        x = (x1 + x2) // 2
        y = self.tick_box.button_object.y

        return (x, y)
    
    def get_text(self, text: str, font_name: str | None, font_size: int, font_colour: tuple[int], antialias: bool) -> tuple[pygame.Surface, pygame.Rect]:
        """Return the text surface and rect objects to draw text."""
        font = pygame.font.Font(font_name, font_size)
        
        text_surf = font.render(text, antialias, font_colour, self.outer_box_colour)
        text_rect = text_surf.get_rect()

        text_pos = self.find_text_pos()
        text_rect.center = text_pos

        return text_surf, text_rect

    def draw(self) -> None:
        """Draw the outer box, tick box and text to the screen."""
        outer_rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
        pygame.draw.rect(self.surface, self.outer_box_colour, outer_rect, border_radius=self.outer_corner_radius)

        self.surface.blit(self.text_surface, self.text_rect)

        self.tick_box.draw()

    def update(self) -> None:
        """
        Update the TickBoxToggle object.

        This should be called once per frame.
        """

        self.tick_box.update()
        self.draw()