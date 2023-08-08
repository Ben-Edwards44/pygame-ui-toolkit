import pygame
from src.elements import button, input


BUTTON_HEIGHT = 50
BUTTON_WIDTH = 200
BUTTON_RADIUS = 50

SELECTED_COLOUR = (100, 100, 100)
DESELECTED_COLOUR = (255, 255, 255)

BORDER_COLOUR = (255, 0, 0)
BORDER_WIDTH = 4

FONT_COLOUR = (0, 0, 0)
FONT_SIZE = 32


pygame.init()
window = pygame.display.set_mode((500, 500))


def button_normal(btn):
    if type(btn) == button.RectButton or type(btn) == button.BorderedRectButton:
        btn.height = BUTTON_HEIGHT
        btn.width = BUTTON_WIDTH
    elif type(btn) == button.CircleButton or type(btn) == button.BorderedCircleButton:
        btn.radius = BUTTON_RADIUS
    else:
        btn.points[0] = (btn.points[0][0], 200)
        btn.points[2] = (btn.points[2][0], 300)


def button_hover(btn):
    if type(btn) == button.RectButton or type(btn) == button.BorderedRectButton:
        btn.height = BUTTON_HEIGHT + 10
        btn.width = BUTTON_WIDTH + 10
    elif type(btn) == button.CircleButton or type(btn) == button.BorderedCircleButton:
        btn.radius = BUTTON_RADIUS + 10
    else:
        btn.points[0] = (btn.points[0][0], 190)
        btn.points[2] = (btn.points[2][0], 310)


def button_click(btn):
    if type(btn) == button.RectButton or type(btn) == button.BorderedRectButton:
        btn.height = BUTTON_HEIGHT - 20
        btn.width = BUTTON_WIDTH - 20
    elif type(btn) == button.CircleButton or type(btn) == button.BorderedCircleButton:
        btn.radius = BUTTON_RADIUS - 20


def on_selected(text_input):
    text_input.input_button.button_object.background_colour = SELECTED_COLOUR


def on_deselect(text_input):
    text_input.input_button.button_object.background_colour = DESELECTED_COLOUR


def create_text_inputs():
    rect = input.RectTextInput(window, 250, 100, DESELECTED_COLOUR, BUTTON_WIDTH, BUTTON_HEIGHT, FONT_COLOUR, FONT_SIZE, None, button_click, button_hover, button_normal, on_selected, on_deselect, click_once=False, prefix_text="Type here: ")
    bord_rect = input.BorderedRectTextInput(window, 250, 200, DESELECTED_COLOUR, BORDER_COLOUR, BUTTON_WIDTH, BUTTON_HEIGHT, BORDER_WIDTH, FONT_COLOUR, FONT_SIZE, None, button_click, button_hover, button_normal, on_selected, on_deselect, click_once=False)

    circ = input.CircleTextInput(window, 250, 300, DESELECTED_COLOUR, BUTTON_RADIUS, FONT_COLOUR, FONT_SIZE, None, button_click, button_hover, button_normal, on_selected, on_deselect, False, "Enter text")
    bord_circ = input.BorderedCircleTextInput(window, 250, 440, DESELECTED_COLOUR, BORDER_COLOUR, BUTTON_RADIUS, BORDER_WIDTH, FONT_COLOUR, FONT_SIZE, None, button_click, button_hover, button_normal, on_selected, on_deselect, False)

    return [rect, bord_rect, circ, bord_circ]


def update_text_inputs(text_inputs, event_loop):
    window.fill((0, 0, 0))

    for i in text_inputs:
        i.update(event_loop)

    pygame.display.update()


def main():
    text_inputs = create_text_inputs()

    while True:
        event_loop = pygame.event.get()

        update_text_inputs(text_inputs, event_loop)

        for event in event_loop:
            if event.type == pygame.QUIT:
                quit()


if __name__ == "__main__":
    main()