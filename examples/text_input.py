import pygame
from pygame_ui_toolkit.presets import input_size_colour_change


NORMAL_SIZE = (200, 60)
HOVER_SIZE = (220, 70)
CLICK_SIZE = (180, 50)

SELECTED_COLOUR = (100, 100, 100)
DESELECTED_COLOUR = (255, 255, 255)

BORDER_COLOUR = (255, 0, 0)
BORDER_WIDTH = 4

FONT_COLOUR = (0, 0, 0)
FONT_SIZE = 32


pygame.init()
window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Text inputs")


def on_text_input(txt):
    print(txt)


def create_text_inputs():
    input1 = input_size_colour_change.create_text_input(DESELECTED_COLOUR, SELECTED_COLOUR, NORMAL_SIZE, HOVER_SIZE, CLICK_SIZE, window, 250, 150, FONT_COLOUR, FONT_SIZE, on_text_input=on_text_input, prefix_text="Text: ")
    input2 = input_size_colour_change.create_text_input(DESELECTED_COLOUR, SELECTED_COLOUR, NORMAL_SIZE, HOVER_SIZE, CLICK_SIZE, window, 250, 350, FONT_COLOUR, FONT_SIZE, on_text_input=on_text_input)

    return input1, input2


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