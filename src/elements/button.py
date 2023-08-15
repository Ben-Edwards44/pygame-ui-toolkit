from . import pygame
from . import utils


class Button:
    """
    The base class that all other button classes inherit from.

    This class should not be used directly. 
    Instead use RectButton, CircleButton, PolygonButton, BorderedRectButton, BorderedCircleButton, or BorderedPolygonButton.

    Attributes
    ----------
    surface : pygame.Surface
        the surface that the button is drawn onto
    x : int
        the x position of the center of the button
    y : int
        the y position of the center of the button
    on_click : callable | None, optional
        the function that is called when the button is clicked. If the function accepts 1 argument, self is passed into it (defaults to None)
    on_hover : callable | None, optional
        the function that is called when the button is hovered over. If the function accepts 1 argument, self is passed into it (defaults to None)
    on_normal : callable | None, optional
        the function that is called when the button is neither clicked or hovered over. If the function accepts 1 argument, self is passed into it (defaults to None)
    click_once : bool, optional
        if True, the on_click and on_hover functions will be called once per click or hover event, otherwise they will be called every ferame the button is clicked or hovered (defaults to True)
    
    Methods
    -------
    update_clicked(currently_clicked: bool)
        update the clicked attribute.
    update_hovered(currently_hovered: bool)
        update the hovered attribute.
    call_func(func: callable)
        call utils.call_func(func, self).
    check_click()
        return whether the button is ciurrently being clicked.
    check_hover()
        return whether the button is being hovered over.
    update()
        draw the button and call the on_click, on_hover and on_normal functions where appropriate.
    """

    def __init__(self, surface: pygame.Surface, x: int, y: int, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, click_once: bool = True) -> None:
        """Construct the necessary attributes for the Button object"""
        self.surface = surface

        self.x = x
        self.y = y

        self.on_click = on_click
        self.on_hover = on_hover
        self.on_normal = on_normal

        self.click_once = click_once

        self.clicked = False
        self.hovered = False

    def update_clicked(self, currently_clicked: bool) -> bool:
        """
        Update the clicked attribute.
        
        Parameters
        ----------

        currently_clicked : bool
            whether the mouse is currently over the button and the mouse button is pressed

        Returns
        -------
        bool
            whether on_click should be called
        """
        if not self.click_once:
            self.clicked = currently_clicked
            return currently_clicked
        
        if not currently_clicked:
            self.clicked = False
            return False
        
        if self.clicked:
            return False
        else:
            self.clicked = True
            return True
        
    def update_hovered(self, currently_hovered: bool) -> bool:
        """
        Update the hovered attribute.
        
        Parameters
        ----------

        currently_hovered : bool
            whether the mouse is currently over the button

        Returns
        -------
        bool
            whether on_hover should be called
        """
        if not self.click_once:
            self.hovered = currently_hovered
            return currently_hovered
        
        if not currently_hovered:
            self.hovered = False
            return False
        
        if self.hovered:
            return False
        else:
            self.hovered = True
            return True

    get_pos = lambda self: (self.x, self.y)

    def call_func(self, func: callable) -> None:
        """Call utils.call_func(func, self)."""
        if func == None:
            return
        else:
            utils.call_func(func, self)
        
    def check_click(self) -> bool:
        """Return whether the button is ciurrently being clicked."""
        mouse_over = self.mouse_over()
        mouse_down = pygame.mouse.get_pressed(3)[0]

        click = mouse_over and mouse_down

        return self.update_clicked(click)
    
    def check_hover(self) -> bool:
        """Return whether the button is currently being hovered over."""
        mouse_over = self.mouse_over()

        return self.update_hovered(mouse_over)
    
    def update(self) -> None:
        """
        Draw the button and call the on_click, on_hover and on_normal functions where appropriate.

        This should be called once per frame.

        An exception is raised if the button object does not contain the nessesary methods.
        """
        self.draw()
        
        if not hasattr(self, "check_click") or not hasattr(self, "check_hover"):
            raise Exception("Base Button class should not be used by itself. Use another class like RectButton instead")

        if self.check_click():
            self.call_func(self.on_click)
        elif self.check_hover():
            self.call_func(self.on_hover)
        else:
            self.call_func(self.on_normal)


class RectButton(Button):
    """
    A rectangular button.

    This inherits from the Button class.

    Attributes
    ----------
    This class inherits from Button, so contains all the attributes that Button does.
    It also contains these additional attributes:
    background_colour : tuple[int]
        the colour of the button
    width : int
        the width (parallel to the x axis) of the button
    corner_radius : int, optional
        the radius of the circles on the rounded corners of the rectangle where -1 means sharp edges and not rounded corners (defaults to -1)
    
    Methods
    -------
    This class inherits from Button, so contains all the metehods that Button does.
    It also contains these additional methods:
    mouse_over()
        return whether the mouse is colliding with, or within the region of, the button rectangle
    draw()
        draw a rectangle with the appropriate width, height, position and colour
    """

    def __init__(self, surface: pygame.Surface, x: int, y: int, background_colour: tuple[int], width: int, height: int, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, corner_radius: int = -1, click_once: bool = True) -> None:
        """Construct the necessary attributes for the RectButton object"""
        super().__init__(surface, x, y, on_click, on_hover, on_normal, click_once)

        self.width = width
        self.height = height

        self.background_colour = background_colour

        self.corner_radius = corner_radius

    def mouse_over(self) -> bool:
        """Return whether the mouse is colliding with, or within the region of, the button rectangle"""
        x, y = pygame.mouse.get_pos()

        min_x = self.x - self.width // 2
        max_x = self.x + self.width // 2
        min_y = self.y - self.height // 2
        max_y = self.y + self.height // 2

        return min_x <= x <= max_x and min_y <= y <= max_y
    
    def draw(self) -> None:
        """Draw a rectangle with the appropriate width, height, position and colour"""
        rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
        pygame.draw.rect(self.surface, self.background_colour, rect, border_radius=self.corner_radius)

    get_width = lambda self: self.width


class CircleButton(Button):
    """
    A circular button.

    This inherits from the Button class.

    Attributes
    ----------
    This class inherits from Button, so contains all the attributes that Button does.
    It also contains these additional attributes:
    background_colour : tuple[int]
        the colour of the button
    radius : int
        the radius of the circle
        
    Methods
    -------
    This class inherits from Button, so contains all the metehods that Button does.
    It also contains these additional methods:
    mouse_over()
        return whether the mouse position is within the circle
    draw()
        draw a circle with the appropriate radius, position and colour
    """

    def __init__(self, surface: pygame.Surface, x: int, y: int, background_colour: tuple[int], radius: int, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, click_once: bool = True) -> None:
        """Construct the nessesary attributes for the CircleButton object"""
        super().__init__(surface, x, y, on_click, on_hover, on_normal, click_once)

        self.background_colour = background_colour

        self.radius = radius
        self.radius_sq = radius**2

    def mouse_over(self) -> bool:
        """Return whether the mouse position is within the circle"""
        x, y = pygame.mouse.get_pos()

        dist_sq = (x - self.x)**2 + (y - self.y)**2

        return dist_sq < self.radius_sq
    
    def draw(self) -> None:
        """Draw a circle with the appropriate radius, position and colour"""
        center = self.get_pos()
        pygame.draw.circle(self.surface, self.background_colour, center, self.radius)

    get_width = lambda self: self.radius * 2


class PolygonButton(Button):
    """
    A button in the shape of any convex polygon.
    Convex polygons are **not** supported and will result in unexpected behaviour.

    This inherits from the Button class.

    Attributes
    ----------
    This class inherits from Button, so contains all the attributes that Button does.
    It also contains these additional attributes:
    background_colour: tuple[int]
        the colour of the button
    points : list[tuple[int]]
        a list of x, y coordinates that correspond to each point on the polygon
        
    Methods
    -------
    This class inherits from Button, so contains all the metehods that Button does.
    It also contains these additional methods:
    get_center(points: list[tuple[int]])
        return the center of the polygon by averaging the position of each point
    get_inequalities(points: list[tuple[int]], center_x: int, center_y: int)
        return a list of inequalities that describe the button region
    mouse_over()
        return whether the mouse position is within the polygon using inequalities
    draw()
        draw a polygon with the appropriate points and colour
    """

    def __init__(self, surface: pygame.Surface, points: list[tuple[int]], background_colour: tuple[int], on_click: callable = None, on_hover: callable = None, on_normal: callable = None, click_once: bool = True) -> None:
        """Construct the necessary attributes for the PolygonButton object"""
        x, y = self.get_center(points)
        
        super().__init__(surface, x, y, on_click, on_hover, on_normal, click_once)

        self.points = points
        self.background_colour = background_colour

        self.inequalities = self.get_inequalities(points, x, y)

    def get_center(self, points: list[tuple[int]]) -> tuple[int]:
        """
        Return the center of the polygon by averaging the position of each point.

        Parameters
        ----------
        points : list[tuple[int]]
            a list of x, y coordinates that correspond to each point on the polygon

        Returns
        -------
        tuple[int]
            x, y coordinates to describe the center of the polygon
        """
        x_values = [i[0] for i in points]
        y_values = [i[1] for i in points]

        x = sum(x_values) // len(x_values)
        y = sum(y_values) // len(y_values)

        return x, y
    
    def get_inequalities(self, points: list[tuple[int]], center_x: int, center_y: int) -> list[tuple[float, float, bool]]:
        """
        Return a list of inequalities that describe the button region.

        Parameters
        ----------
        points : list[tuple[int]]
            a list of x, y coordinates that correspond to each point on the polygon
        center_x : int
            the x coordinate of the center of the polygon
        center_y : int
            the y coordinate of the center of the polygon

        Returns
        -------
        list[tuple[float, float, bool]]
            a list of linear inequalities in the form: line_gradient, y_intercept, greater_than (each line is interpreted as having the equation y=mx + c)
        """
        inequalities = []
        for i, x in enumerate(points):
            try:
                m = (x[1] - points[i - 1][1]) / (x[0] - points[i - 1][0])
            except ZeroDivisionError:
                m = 1e10

            c = x[1] - m * x[0]
            greater_than = (m * center_x + c) < center_y

            inequalities.append((m, c, greater_than))

        return inequalities

    def mouse_over(self) -> None:
        """Return whether the mouse position is within the polygon using inequalities."""
        x, y = pygame.mouse.get_pos()

        for m, c, greater_than in self.inequalities:
            intersect_y = m * x + c
            actual_greater_than = intersect_y < y

            if actual_greater_than != greater_than:
                return False
            
        return True
    
    def draw(self) -> None:
        """Draw a polygon with the appropriate points and colour."""
        pygame.draw.polygon(self.surface, self.background_colour, self.points)


class ImageButton(RectButton):
    """
    A button as an image.

    This inherits from the RectButton class.

    Attributes
    ----------
    This class inherits from RectButton, so contains all the attributes that RectButton does.
    It also contains these additional attributes:
    image_path : str
        the file path to the desired image
    image : pygame.Surface
        the image of the button in a form useable for pygame

    Methods
    -------
    This class inherits from RectButton, so contains all the methods that RectButton does.
    It also contains these additional methods:
    setup_image()
        return a pygame Surface object for the button's image

    The following methods are overwritten:
    draw()
        blit the image to the screen
    """

    def __init__(self, surface: pygame.Surface, x: int, y: int, width: int, height: int, image_path: str, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, click_once: bool = True) -> None:
        """Construct the necessary attributes for the ImageButton object"""
        super().__init__(surface, x, y, None, width, height, on_click, on_hover, on_normal, -1, click_once)

        self.image_path = image_path
        self.image = self.setup_image()

    def setup_image(self) -> pygame.Surface:
        """Return a pygame Surface object for the button's image."""
        image = pygame.image.load(self.image_path)
        scaled_image = pygame.transform.scale(image, (self.width, self.height))

        return scaled_image

    def draw(self) -> None:
        """Blit the image to the screen."""
        image_x = self.x - self.width // 2
        image_y = self.y - self.height // 2

        self.surface.blit(self.image, (image_x, image_y))


class BorderedRectButton(RectButton):
    """
    A rectangluar button with a border.

    This inherits from the RectButton class.

    Attributes
    ----------
    This class inherits from RectButton, so contains all the attributes that RectButton does.
    It also contains these additional attributes:
    border_colour : tuple[int]
        the colour of the border
    border_width : int
        the width, or thickness, of the border

    Methods
    -------
    This class inherits from RectButton, so contains all the methods that RectButton does.
    The following methods are overwritten:
    draw()
        draw a rectangle and border
    """

    def __init__(self, surface: pygame.Surface, x: int, y: int, background_colour: tuple[int], border_colour: tuple[int], width: int, height: int, border_width: int, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, corner_radius: int = -1, click_once: bool = True) -> None:
        """Construct the necessary attributes for the BorderedRectButton object."""
        super().__init__(surface, x, y, background_colour, width, height, on_click, on_hover, on_normal, corner_radius, click_once)

        self.border_colour = border_colour
        self.border_width = border_width

    def draw(self) -> None:
        """Draw a rectangle and border."""
        rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

        pygame.draw.rect(self.surface, self.background_colour, rect, border_radius=self.corner_radius)
        pygame.draw.rect(self.surface, self.border_colour, rect, self.border_width, self.corner_radius)


class BorderedCircleButton(CircleButton):
    """
    A circular button with a border.

    This inherits from the CircleButton class.

    Attributes
    ----------
    This class inherits from CircleButton, so contains all the attributes that CircleButton does.
    It also contains these additional attributes:
    border_colour : tuple[int]
        the colour of the border
    border_width : int
        the width, or thickness, of the border

    Methods
    -------
    This class inherits from CircleButton, so contains all the methods that CircleButton does.
    The following methods are overwritten:
    draw()
        draw a circle and border
    """

    def __init__(self, surface: pygame.Surface, x: int, y: int, background_colour: tuple[int], border_colour: tuple[int], radius: int, border_width: int, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, click_once: bool = True) -> None:
        """Construct the necessary attributes for the BorderedCircleButton object."""
        super().__init__(surface, x, y, background_colour, radius, on_click, on_hover, on_normal, click_once)

        self.border_colour = border_colour
        self.border_width = border_width

    def draw(self) -> None:
        """Draw a circle and border."""
        pygame.draw.circle(self.surface, self.background_colour, self.get_pos(), self.radius)
        pygame.draw.circle(self.surface, self.border_colour, self.get_pos(), self.radius, self.border_width)


class BorderedPolygonButton(PolygonButton):
    """
    A polygon button with a border.

    This inherits from the PolygonButton class.

    Attributes
    ----------
    This class inherits from PolygonButton, so contains all the attributes that PolygonButton does.
    It also contains these additional attributes:
    border_colour : tuple[int]
        the colour of the border
    border_width : int
        the width, or thickness, of the border

    Methods
    -------
    This class inherits from PolygonButton, so contains all the methods that PolygonButton does.
    The following methods are overwritten:
    draw()
        draw a polygon and border
    """
    def __init__(self, surface: pygame.Surface, points: list[tuple[int]], background_colour: tuple[int], border_colour: tuple[int], border_width: int, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, click_once: bool = True) -> None:
        """Construct the necessary attributes for the BorderedPolygonButton object."""
        super().__init__(surface, points, background_colour, on_click, on_hover, on_normal, click_once)

        self.border_colour = border_colour
        self.border_width = border_width

    def draw(self) -> None:
        """Draw a polygon and border."""
        pygame.draw.polygon(self.surface, self.background_colour, self.points)
        pygame.draw.polygon(self.surface, self.border_colour, self.points, self.border_width)


class TextWrapper:
    """
    A wrapper object that allows text to be drawn on top of button objects.

    All buttons other than PolygonButton and BorderedPolygonButton are supported.

    Attributes
    ----------
    button_object : RectButton | CircleButton | BorderedCircleButton | BorderedRectButton
        the button object that text will be drawn upon
    text : str
        the text displayed
    font_colour : tuple[int]
        the colour of the displayed text
    font : pygame.font.Font
        the font object used to blit text
    font_name : str | None, optional
        the name of the font used (defaults to None)
    antialias : bool, optional
        whether the text is drawn with antialias (defaults to False)
    text_surface : pygame.Surface
        the surface used to render text
    text_rect : pygame.Rect
        the rect position that the text is drawn to

    Methods
    -------
    get_text()
        return a text surface and rect object to blit text
    blit_text()
        draw text to the screen
    update_text(new_text: str | None = None, new_font_colour: tuple[int] | None = None, new_font_size: int | None = None, new_font_name: str | None = None)
        change the text, font_colour, font attributes of the object
    update()
        update the TextWrapper object
    """

    def __init__(self, button_object: RectButton | CircleButton | BorderedCircleButton | BorderedRectButton, text: str, font_colour: tuple[int], font_size: int, font_name: str | None = None, antialias: bool = False) -> None:
        """Construct necessary attributes for TextWrapper object."""
        self.button_object = button_object
        
        self.text = text
        self.font_colour = font_colour
        self.font = pygame.font.Font(font_name, font_size)

        self.antialias = antialias

        self.text_surface, self.text_rect = self.get_text()

    def get_text(self) -> tuple[pygame.Surface, pygame.Rect]:
        """Return a text surface and rect object to blit text."""
        text_surf = self.font.render(self.text, self.antialias, self.font_colour, self.button_object.background_colour)
        text_rect = text_surf.get_rect()
        text_rect.center = self.button_object.get_pos()

        return text_surf, text_rect
    
    def blit_text(self) -> None:
        """Draw text to the screen."""
        self.button_object.surface.blit(self.text_surface, self.text_rect)

    def update_text(self, new_text: str | None = None, new_font_colour: tuple[int] | None = None, new_font_size: int | None = None, new_font_name: str | None = None) -> None:
        """Change the text, font_colour, font attributes of the object."""

        if new_text != None:
            self.text = new_text

        if new_font_colour != None:
            self.font_colour = new_font_colour

        if new_font_size != None:
            self.font = pygame.font.Font(new_font_name, new_font_size)

        self.text_surface, self.text_rect = self.get_text()

    def draw(self) -> None:
        """Draw button object and blit text on top."""
        self.button_object.update()
        self.blit_text()
        
    def update(self) -> None:
        """
        Update the text wrapper button.
        
        This should be called once per frame.
        """

        self.draw()