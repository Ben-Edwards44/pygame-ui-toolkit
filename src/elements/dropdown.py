from . import toggle
from . import button
from . import utils
from . import pygame


class Option:
    """
    An individual option for the dropdown menu.

    Attributes
    ----------
    parent_dropdown : object
        the dropdown menu object that this option is a part of
    text_wrapper : button.TextWrapper
        the button text wrapper oboject that provides the button functionality, like on click events
    normal_button_on_click : callable
        the text wrapper button's on_click function before it is changed by the Option class
    active : bool
        whether or not this option should be displayed and updated

    Methods
    -------
    setup_button()
        prepare the text_wrapper attribute
    on_button_click()
        call normal_button_on_click and select this option
    update()
        update the object
    """

    def __init__(self, parent_dropdown: object, text_wrapper: button.TextWrapper, start_active: bool = False) -> None:
        """Construct the necessary attributes for the Option object."""
        self.parent_dropdown = parent_dropdown
        
        self.text_wrapper = text_wrapper
        self.normal_button_on_click = text_wrapper.button_object.on_click

        self.active = start_active

        self.setup_button()

    def setup_button(self) -> None:
        """Prepare the text_wrapper attribute."""
        self.text_wrapper.button_object.on_click = self.on_button_click

    def on_button_click(self) -> None:
        """Call normal_button_on_click and select this option."""
        self.text_wrapper.button_object.call_func(self.normal_button_on_click)

        self.parent_dropdown.option_selected(self)

    def update(self) -> None:
        """
        Update the object.
        
        This should be called once per frame.
        """
        if self.active:
            self.text_wrapper.update()


class Dropdown(toggle.Toggle):
    """
    The class from which all dropdown menus inherit from.

    This class should not be used on its own.
    Instead use RectDropdown, CircleDropdown, BorderedRectDropdown or BorderedCircleDropdown.

    Inherits from toggle.Toggle.

    Attributes
    ----------
    all attributes from toggle.Toggle
    font_colour : tuple[int]
        the colour of displayed text
    font_size : int
        the size of displayed text
    font_name : str | None, optional
        the path to, or name of, the font used to display text (defaults to None)
    on_option_changed : callable, optional
        the function called once the option is changed. If it accepts 1 argument, the option is passed in; if it accepts 2 arguments, the option and the dropdown object are passed in; if no arguments are accepted, the function is just called (default ot None)
    antialias : bool, optional
        whether th text is drawn with antialias
    options : lsit[Option]
        a list of all options in the dropdown menu
    selected_option : Option
        the currently selected option object
    text_wrapper : button.TextWrapper
        the button text wrapper oboject that provides the button functionality, like on click events

    Methods
    -------
    all methods from toggle.Toggle
    create_options(option_buttons: list[object], option_names: list[str], start_active: bool)
        return a list of Option objects when given a list of their names and button objects
    on_value_changed(value: bool)
        update the active attribute of each option
    option_selected(option: Option)
        change selected option and update text
    update()
        update the dropdown object
    """

    def __init__(self, button_object: object, option_buttons: list[object], option_names: list[str], font_colour: tuple[int], font_size: int, font_name: str | None = None, on_option_changed: callable = None, initial_option: int = 0, start_active: bool = False, antialias: bool = False) -> None:
        """Construct the necessary attributes for the Dropdown object."""
        self.font_colour = font_colour
        self.font_size = font_size
        self.font_name = font_name

        self.on_option_changed = on_option_changed

        self.antialias = antialias
        
        self.options = self.create_options(option_buttons, option_names, start_active)

        self.selected_option = self.options[initial_option]

        self.text_wrapper = button.TextWrapper(button_object, self.selected_option.text_wrapper.text, font_colour, font_size, font_name, antialias)

        super().__init__(button_object, self.on_value_changed, False)

    def create_options(self, option_buttons: list[object], option_names: list[str], start_active: bool) -> list[Option]:
        """Return a list of Option objects when given a list of their names and button objects."""
        options = []
        for i, x in enumerate(option_buttons):
            text = option_names[i]

            text_wrapper = button.TextWrapper(x, text, self.font_colour, self.font_size, self.font_name, self.antialias)
            option = Option(self, text_wrapper, start_active)

            options.append(option)

        return options

    def on_value_changed(self, value: bool) -> None:
        """Update the active attribute of each option."""
        for i in self.options:
            i.active = value

    def option_selected(self, option: Option) -> None:
        """Change selected option and update text."""
        self.selected_option = option
        self.selected = False

        self.text_wrapper.update_text(option.text_wrapper.text, self.font_colour, self.font_size, self.font_name)

        utils.call_func(self.on_option_changed, option, self)

    def update(self) -> None:
        """
        Update the dropdown object.

        This should be called once per frame.
        """
        self.text_wrapper.update()

        for i in self.options:
            i.update()

        if self.selected != self.prev_selected:
            utils.call_func(self.on_value_changed, self.selected)
            self.prev_selected = self.selected


class RectDropdown(Dropdown):
    """
    A dropdown menu with rectangular options.

    Inherits from Dropdown.

    Attributes
    ----------
    all attributes from Dropdown
    button_object : button.RectButton
        the button object for the main dropdown button
    option_buttons : list[button.RectButton]
        a list of the button objects for each of the options in the dropdown menu

    Methods
    -------
    all methods from Dropdown
    create_buttons(surface: pygame.Surface, num_options: int, x: int, y: int, colour: tuple[int], width: int, height: int, y_offset: int, on_click: callable, on_hover: callable, on_normal: callable, corner_radius: int)
        create the button objects for each of the options in the dropdown menu
    """

    def __init__(self, surface: pygame.Surface, option_names: list[str], x: int, y: int, background_colour: tuple[int], width: int, height: int, font_colour: tuple[int], font_size: int, font_name: str | None = None, y_offset: int = 10, on_option_changed: callable = None, initial_option: int = 0, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, corner_radius: int = -1, start_active: bool = False, antialias: bool = False) -> None:
        """Construct the necessary attributes for the RectDropdown object."""
        button_object = button.RectButton(surface, x, y, background_colour, width, height, on_click, on_hover, on_normal, corner_radius)
        option_buttons = self.create_buttons(surface, len(option_names), x, y, background_colour, width, height, y_offset, on_click, on_hover, on_normal, corner_radius)

        super().__init__(button_object, option_buttons, option_names, font_colour, font_size, font_name, on_option_changed, initial_option, start_active, antialias)

    def create_buttons(self, surface: pygame.Surface, num_options: int, x: int, y: int, colour: tuple[int], width: int, height: int, y_offset: int, on_click: callable, on_hover: callable, on_normal: callable, corner_radius: int) -> list[button.RectButton]:
        """Create the button objects for each of the options in the dropdown menu."""
        buttons = []
        for i in range(1, num_options + 1):
            new_y = y + i * (height + y_offset)

            btn = button.RectButton(surface, x, new_y, colour, width, height, on_click, on_hover, on_normal, corner_radius)
            buttons.append(btn)
            
        return buttons
    

class CircleDropdown(Dropdown):
    """
    A dropdown menu with circular options.

    Inherits from Dropdown.

    Attributes
    ----------
    all attributes from Dropdown
    button_object : button.RectButton
        the button object for the main dropdown button
    option_buttons : list[button.RectButton]
        a list of the button objects for each of the options in the dropdown menu

    Methods
    -------
    all methods from Dropdown
    create_buttons(surface: pygame.Surface, num_options: int, x: int, y: int, colour: tuple[int], width: int, height: int, y_offset: int, on_click: callable, on_hover: callable, on_normal: callable, corner_radius: int)
        create the button objects for each of the options in the dropdown menu
    """

    def __init__(self, surface: pygame.Surface, option_names: list[str], x: int, y: int, background_colour: tuple[int], radius: int, font_colour: tuple[int], font_size: int, font_name: str | None = None, y_offset: int = 10, on_option_changed: callable = None, initial_option: int = 0, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, start_active: bool = False, antialias: bool = False) -> None:
        """Construct the necessary attributes for the CircleDropdown object."""
        button_object = button.CircleButton(surface, x, y, background_colour, radius, on_click, on_hover, on_normal)
        option_buttons = self.create_buttons(surface, len(option_names), x, y, background_colour, radius, y_offset, on_click, on_hover, on_normal)

        super().__init__(button_object, option_buttons, option_names, font_colour, font_size, font_name, on_option_changed, initial_option, start_active, antialias)

    def create_buttons(self, surface: pygame.Surface, num_options: int, x: int, y: int, colour: tuple[int], radius: int, y_offset: int, on_click: callable, on_hover: callable, on_normal: callable) -> list[button.RectButton]:
        """Create the button objects for each of the options in the dropdown menu."""
        buttons = []
        for i in range(1, num_options + 1):
            new_y = y + i * (2 * radius + y_offset)

            btn = button.CircleButton(surface, x, new_y, colour, radius, on_click, on_hover, on_normal)
            buttons.append(btn)
            
        return buttons
    

class BorderedRectDropdown(Dropdown):
    """
    A dropdown menu with rectangular options with borders.

    Inherits from Dropdown.

    Attributes
    ----------
    all attributes from Dropdown
    button_object : button.RectButton
        the button object for the main dropdown button
    option_buttons : list[button.RectButton]
        a list of the button objects for each of the options in the dropdown menu

    Methods
    -------
    all methods from Dropdown
    create_buttons(surface: pygame.Surface, num_options: int, x: int, y: int, colour: tuple[int], width: int, height: int, y_offset: int, on_click: callable, on_hover: callable, on_normal: callable, corner_radius: int)
        create the button objects for each of the options in the dropdown menu
    """

    def __init__(self, surface: pygame.Surface, option_names: list[str], x: int, y: int, background_colour: tuple[int], border_colour: tuple[int], width: int, height: int, border_width: int, font_colour: tuple[int], font_size: int, font_name: str | None = None, y_offset: int = 10, on_option_changed: callable = None, initial_option: int = 0, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, corner_radius: int = -1, start_active: bool = False, antialias: bool = False) -> None:
        """Construct the necessary attributes for the BorderedRectDropdown object."""
        button_object = button.BorderedRectButton(surface, x, y, background_colour, border_colour, width, height, border_width, on_click, on_hover, on_normal, corner_radius)
        option_buttons = self.create_buttons(surface, len(option_names), x, y, background_colour, border_colour, width, height, border_width, y_offset, on_click, on_hover, on_normal, corner_radius)

        super().__init__(button_object, option_buttons, option_names, font_colour, font_size, font_name, on_option_changed, initial_option, start_active, antialias)

    def create_buttons(self, surface: pygame.Surface, num_options: int, x: int, y: int, background_colour: tuple[int], border_colour: tuple[int], width: int, height: int, border_width: tuple[int], y_offset: int, on_click: callable, on_hover: callable, on_normal: callable, corner_radius: int) -> list[button.RectButton]:
        """Create the button objects for each of the options in the dropdown menu."""
        buttons = []
        for i in range(1, num_options + 1):
            new_y = y + i * (height + y_offset)

            btn = button.BorderedRectButton(surface, x, new_y, background_colour, border_colour, width, height, border_width, on_click, on_hover, on_normal, corner_radius)
            buttons.append(btn)
            
        return buttons
    

class BorderedCircleDropdown(Dropdown):
    """
    A dropdown menu with circular options with borders.

    Inherits from Dropdown.

    Attributes
    ----------
    all attributes from Dropdown
    button_object : button.RectButton
        the button object for the main dropdown button
    option_buttons : list[button.RectButton]
        a list of the button objects for each of the options in the dropdown menu

    Methods
    -------
    all methods from Dropdown
    create_buttons(surface: pygame.Surface, num_options: int, x: int, y: int, colour: tuple[int], width: int, height: int, y_offset: int, on_click: callable, on_hover: callable, on_normal: callable, corner_radius: int)
        create the button objects for each of the options in the dropdown menu
    """

    def __init__(self, surface: pygame.Surface, option_names: list[str], x: int, y: int, background_colour: tuple[int], border_colour: tuple[int], radius: int, border_width: int, font_colour: tuple[int], font_size: int, font_name: str | None = None, y_offset: int = 10, on_option_changed: callable = None, initial_option: int = 0, on_click: callable = None, on_hover: callable = None, on_normal: callable = None, start_active: bool = False, antialias: bool = False) -> None:
        """Construct the necessary attributes for the BorderedCircleDropdown object."""
        button_object = button.BorderedCircleButton(surface, x, y, background_colour, border_colour, radius, border_width, on_click, on_hover, on_normal)
        option_buttons = self.create_buttons(surface, len(option_names), x, y, background_colour, border_colour, radius, border_width, y_offset, on_click, on_hover, on_normal)

        super().__init__(button_object, option_buttons, option_names, font_colour, font_size, font_name, on_option_changed, initial_option, start_active, antialias)

    def create_buttons(self, surface: pygame.Surface, num_options: int, x: int, y: int, background_colour: tuple[int], border_colour: tuple[int], radius: int, border_width: int, y_offset: int, on_click: callable, on_hover: callable, on_normal: callable) -> list[button.RectButton]:
        """Create the button objects for each of the options in the dropdown menu."""
        buttons = []
        for i in range(1, num_options + 1):
            new_y = y + i * (2 * radius + y_offset)

            btn = button.BorderedCircleButton(surface, x, new_y, background_colour, border_colour, radius, border_width, on_click, on_hover, on_normal)
            buttons.append(btn)
            
        return buttons