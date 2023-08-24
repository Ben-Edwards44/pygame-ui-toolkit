# pygame-ui-toolkit

pygame-ui-toolkit is a python library for easily creating UI elements with Pygame.

It makes it easy to add buttons, sliders, text inputs and more UI components to any pygame project.

# Installation

Run the following command to install pygame-ui-toolkit via pip:

    pip install pygame-ui-toolkit

# Usage

Once installed, import the package into your project by entering the following line at the top of your script.

    import pygame_ui_toolkit

There is no official documentation for this package.

The scripts in the `examples` directory should show you how to use the package. They detail the creation and use of all core UI elements and the presets.

Docstrings and type hints have been included within the scripts in the project, which should outline what each function and class does alongside the kinds of arguments that should be passed into them.

As a general tip, always remember to call an element's `update()` method **once per frame**. This is shown in the following example:

    import pygame
    import pygame_ui_toolkit

    # Create the button
    button = pygame_ui_toolkit.elements.button.RectButton(...)

    # Main loop
    while True:
        # Update the button
        button.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

# Features

pygame-ui-toolkit offers the following features:

## UI Elements:

These are the core user input elements that can be created using this library.

### Buttons

- Rectangle buttons
- Bordered rectangle buttons
- Circle buttons
- Bordered circle buttons
- Polygon buttons
- Bordered polygon buttons
- All of the above with text

### Sliders

- Horizontal sliders
- Vertical sliders

### Text Inputs

- All buttons (other than polygon buttons) can be used as text inputs

### Toggles

- Tick box
- Tick box with text to the left or right

### Dropdown Menus

- Rectangle dropdowns
- Bordered rectangle dropdowns
- Circle dropdowns
- Bordered circle dropdowns

### Text Boxes

- All button types can be used as a text box

## Presets:

These are additional functionalities added on top of the core UI elements.

### Button

- Changing colour when hovered over or clicked on
- Changing size when hovered over or clicked on

### Slider

- Automatically updating text that displays the current slider value

### Text Input

- Automatically change size when hovered or clicked and change colour when currently selected