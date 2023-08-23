import pygame
from pygame_ui_toolkit.presets.slider import value_text


NORMAL_COLOUR = (255, 255, 255)
HOVER_COLOUR = (200, 200, 200)
CLICK_COLOUR = (100, 100, 100)

BORDER_COLOUR = (255, 0, 0)
BORDER_WIDTH = 2

SLIDER_LENGTH = 150
SLIDER_THICKNESS = 10
SLIDER_COLOUR = (200, 200, 200)

MIN_VALUE = 0
MAX_VALUE = 100

FONT_NAME = None
FONT_SIZE = 32
FONT_COLOUR = (255, 255, 255)


pygame.init()
window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Sliders with text")


def create_sliders():
    start = (MAX_VALUE + MIN_VALUE) // 2
    hor_slider = value_text.create_slider_text(window, 250, 100, 250, 125, SLIDER_LENGTH, SLIDER_THICKNESS, MIN_VALUE, MAX_VALUE, start, SLIDER_COLOUR, FONT_NAME, FONT_SIZE, FONT_COLOUR)
    vert_slider = value_text.create_slider_text(window, 250, 300, 285, 300, SLIDER_LENGTH, SLIDER_THICKNESS, MIN_VALUE, MAX_VALUE, start, SLIDER_COLOUR, FONT_NAME, FONT_SIZE, FONT_COLOUR, horizontal_slider=False)

    return hor_slider, vert_slider


def update_sliders(sliders):
    window.fill((0, 0, 0))

    for i in sliders:
        i.update()
        value_text.blit_slider_text(i)

    pygame.display.update()


def main():
    sliders = create_sliders()

    while True:
        update_sliders(sliders)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


if __name__ == "__main__":
    main()