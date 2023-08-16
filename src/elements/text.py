from . import pygame


#TODO docstrings


class TextBox:
    """
    The base text box class that all other text boxes inherit from.

    This class should not be used directly.
    Instead use PolygonTextBox, RectTextBox, CircleTextBox, BorderedPolygonTextBox, BorderedRectTextBox or BorderedCircleTextBox.

    Attributes
    ----------
    surface : pygame.Surface
        the surface that the text box is drawn to
    text : str
        the text displayed on the text box
    background_colour : tuple[int]
        the colour of the text box
    font_colour : tuple[int]
        the colour of the text
    font : pygame.font.Font
        the font object used to blit text
    antialias : bool, optional
        whether the text is drawn with antialias (defaults to False)
    text_surface : pygame.Surface
        the surface used to render text
    text_rect : pygame.Rect
        the rect position that the text is drawn to

    Methods
    -------
    get_text()
        return a text surface to draw and a rect object to draw it to
    update_text()
        change the text, font colour, font size or font name of the displayed text
    blit_text()
        draw the text to the screen
    """

    def __init__(self, surface: pygame.Surface, text: str, background_colour: tuple[int], font_colour: tuple[int], font_size: int, font_name: str | None = None, antialias: bool = False) -> None:
        """Construct the necessary attributes of the TextBox object."""
        self.surface = surface
        
        self.text = text
        
        self.background_colour = background_colour
        self.font_colour = font_colour

        self.font = pygame.font.Font(font_name, font_size)

        self.antialias = antialias

        self.text_surface, self.text_rect = self.get_text()

    def get_text(self) -> tuple[pygame.Surface, pygame.Rect]:
        """Return a text surface to draw and a rect object to draw it to."""
        text_surface = self.font.render(self.text, self.antialias, self.font_colour)
        
        text_rect = text_surface.get_rect()

        if hasattr(self, "center"):
            text_rect.center = self.center
        else:
            raise Exception("TextBox class is not supposed to be used directly. Use another class like RectTextBox instead")

        return text_surface, text_rect

    def update_text(self, new_text: str | None = None, new_font_colour: tuple[int] | None = None, new_font_size: int | None = None, new_font_name: str | None = None) -> None:
        """
        Change the text, font colour, font size or font name of the displayed text.
        
        If any argument (other the new_font_name) is None, that part of the text will remain unchanged.
        """

        if new_text != None:
            self.text = new_text

        if new_font_colour != None:
            self.font_colour = new_font_colour

        if new_font_size != None:
            self.font = pygame.font.Font(new_font_name, new_font_size)

        self.text_surface, self.text_rect = self.get_text()

    def blit_text(self) -> None:
        """Draw the text to the screen."""
        self.surface.blit(self.text_surface, self.text_rect)


class PolygonTextBox(TextBox):
    """
    A text box in the shape of any polygon.

    This inherits from TextBox.

    Attributes
    ----------
    This class contains all attributes from the TextBox class, alongside these additional ones:
    points : list[tuple[int]]
        a list of the coordinates of each point on the polygon
    center : tuple[int]
        the coordinates of the center of the text box shape

    Methods
    -------
    This class contains all methods from the TextBox class, alongside these additional ones:
    get_center()
        return the center of the polygon by averaging all points
    draw() - overwritten from TextBox
        draw the text and text box to the screen
    """

    def __init__(self, surface: pygame.Surface, points: list[tuple[int]], text: str, background_colour: tuple[int], font_colour: tuple[int], font_size: int, font_name: str | None = None, antialias: bool = False) -> None:
        """Construct the necessary attributes for the PolygonTextBox object."""
        self.points = points
        self.center = self.get_center()

        super().__init__(surface, text, background_colour, font_colour, font_size, font_name, antialias)

    def get_center(self) -> tuple[int]:
        """Return the center of the polygon by averaging all points."""
        x_values = [i[0] for i in self.points]
        y_values = [i[1] for i in self.points]

        x = sum(x_values) // len(x_values)
        y = sum(y_values) // len(y_values)

        return x, y
    
    def draw(self) -> None:
        """Draw the text and text box to the screen."""
        pygame.draw.polygon(self.surface, self.background_colour, self.points)
        self.blit_text()


class RectTextBox(TextBox):
    """
    A text box in the shape of a rectangle.

    This inherits from TextBox.

    Attributes
    ----------
    This class contains all attributes from the TextBox class, alongside these additional ones:
    x : int
        the x coordinate of the center of the rectangle
    y : int
        the y coordinate of the center of the rectangle
    center : tuple[int]
        the coordinates of the center of the text box shape
    width : int
        the width (parallel to the x axis) of the rectangle
    height : int
        the height (parallel to the y axis) of the rectangle
    corner_radius : int, optional
        the radius of the rounded corners of the rectange, where -1 means no rounded corners (defaults to -1)

    Methods
    -------
    This class contains all methods from the TextBox class, alongside these additional ones:
    draw() - overwritten from TextBox
        draw the text and text box to the screen
    """

    def __init__(self, surface: pygame.Surface, x: int, y: int, width: int, height: int, text: str, background_colour: tuple[int], font_colour: tuple[int], font_size: int, font_name: str | None = None, corner_radius: int = -1, antialias: bool = False) -> None:        
        """Construct the necessary attributes for the RectTextBox object."""
        self.x = x
        self.y = y
        
        self.center = (x, y)

        self.width = width
        self.height = height

        self.corner_radius = corner_radius

        super().__init__(surface, text, background_colour, font_colour, font_size, font_name, antialias)
        
    def draw(self) -> None:
        """Draw the text and text box to the screen."""
        pygame.draw.rect(self.surface, self.background_colour, (self.x - self.width // 2, self.y - self.height // 2, self.width, self.height))

        self.blit_text()


class CircleTextBox(TextBox):
    """
    A text box in the shape of a circle.

    This inherits from TextBox.

    Attributes
    ----------
    This class contains all attributes from the TextBox class, alongside these additional ones:
    x : int
        the x coordinate of the center of the rectangle
    y : int
        the y coordinate of the center of the rectangle
    center : tuple[int]
        the coordinates of the center of the text box shape
    radius : int
        the radius of the circle

    Methods
    -------
    This class contains all methods from the TextBox class, alongside these additional ones:
    draw() - overwritten from TextBox
        draw the text and text box to the screen
    """

    def __init__(self, surface: pygame.Surface, x: int, y: int, radius: int, text: str, background_colour: tuple[int], font_colour: tuple[int], font_size: int, font_name: str | None = None, antialias: bool = False) -> None:
        """Construct the necessary attributes for the CircleTextBox object."""
        self.x = x
        self.y = y

        self.center = (x, y)

        self.radius = radius
        
        super().__init__(surface, text, background_colour, font_colour, font_size, font_name, antialias)
    
    def draw(self) -> None:
        """Draw the text and text box to the screen."""
        pygame.draw.circle(self.surface, self.background_colour, self.center, self.radius)
        self.blit_text()


class BorderedPolygonTextBox(PolygonTextBox):
    """
    A text box in the shape of any polygon with a border.

    This inherits from PolygonTextBox.

    Attributes
    ----------
    This class contains all attributes from the PolygonTextBox class, alongside these additional ones:
    border_colour : tuple[int]
        the colour of the drawn border
    border_width : int
        the width of the drawn border

    Methods
    -------
    This class contains all methods from the PolygonTextBox class, alongside these overwritten ones:
    draw() - overwritten from PolygonTextBox
        draw the text and text box with border to the screen
    """

    def __init__(self, surface: pygame.Surface, points: list[tuple[int, int]], text: str, background_colour: tuple[int], border_colour: tuple[int], border_width: int, font_colour: tuple[int], font_size: int, font_name: str | None = None, antialias: bool = False) -> None:
        """Construct the necessary attributes for the BorderedPolygonTextBox object."""
        super().__init__(surface, points, text, background_colour, font_colour, font_size, font_name, antialias)

        self.border_colour = border_colour
        self.border_width = border_width

    def draw(self) -> None:
        """Draw the text and text box with border to the screen."""
        pygame.draw.polygon(self.surface, self.background_colour, self.points)
        pygame.draw.polygon(self.surface, self.border_colour, self.points, self.border_width)

        self.blit_text()


class BorderedRectTextBox(RectTextBox):
    """
    A text box in the shape of a rectangle with a border.

    This inherits from RectTextBox.

    Attributes
    ----------
    This class contains all attributes from the RectTextBox class, alongside these additional ones:
    border_colour : tuple[int]
        the colour of the drawn border
    border_width : int
        the width of the drawn border

    Methods
    -------
    This class contains all methods from the RectTextBox class, alongside these overwritten ones:
    draw() - overwritten from RectTextBox
        draw the text and text box with border to the screen
    """
        
    def __init__(self, surface: pygame.Surface, x: int, y: int, width: int, height: int, text: str, background_colour: tuple[int], border_colour: tuple[int], border_width: int, font_colour: tuple[int], font_size: int, font_name: str | None = None, antialias: bool = False) -> None:
        """Construct the necessary attributes for the BorderedRectTextBox object."""
        super().__init__(surface, x, y, width, height, text, background_colour, font_colour, font_size, font_name, antialias)

        self.border_colour = border_colour
        self.border_width = border_width

    def draw(self) -> None:
        """Draw the text and text box with border to the screen."""
        pygame.draw.rect(self.surface, self.background_colour, (self.x - self.width // 2, self.y - self.height // 2, self.width, self.height))
        pygame.draw.rect(self.surface, self.border_colour, (self.x - self.width // 2, self.y - self.height // 2, self.width, self.height), self.border_width)

        self.blit_text()


class BorderedCircleTextBox(CircleTextBox):
    """
    A text box in the shape of a circle with a border.

    This inherits from CircleTextBox.

    Attributes
    ----------
    This class contains all attributes from the CircleTextBox class, alongside these additional ones:
    border_colour : tuple[int]
        the colour of the drawn border
    border_width : int
        the width of the drawn border

    Methods
    -------
    This class contains all methods from the CircleTextBox class, alongside these overwritten ones:
    draw() - overwritten from CircleTextBox
        draw the text and text box with border to the screen
    """
        
    def __init__(self, surface: pygame.Surface, x: int, y: int, radius: int, text: str, background_colour: tuple[int], border_colour: tuple[int], border_width: int, font_colour: tuple[int], font_size: int, font_name: str | None = None, antialias: bool = False) -> None:
        """Construct the necessary attributes for the BorderedCircleTextBox object."""
        super().__init__(surface, x, y, radius, text, background_colour, font_colour, font_size, font_name, antialias)

        self.border_colour = border_colour
        self.border_width = border_width

    def draw(self) -> None:
        """Draw the text and text box with border to the screen."""
        pygame.draw.circle(self.surface, self.background_colour, self.center, self.radius)
        pygame.draw.circle(self.surface, self.border_colour, self.center, self.radius, self.border_width)

        self.blit_text()