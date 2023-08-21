import pygame
from src.elements import slider, button


NORMAL_COLOUR = (255, 255, 255)
HOVER_COLOUR = (200, 200, 200)
CLICK_COLOUR = (100, 100, 100)

BORDER_COLOUR = (255, 0, 0)
BORDER_WIDTH = 2

SLIDER_LENGTH = 100
SLIDER_THICKNESS = 10
SLIDER_COLOUR = (200, 200, 200)

MIN_VALUE = 0
MAX_VALUE = 100


pygame.init()
window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Sliders")


def button_normal(btn):
    btn.background_colour = NORMAL_COLOUR


def button_hover(btn):
    btn.background_colour = HOVER_COLOUR


def button_click(btn):
    btn.background_colour = CLICK_COLOUR


def create_slider_buttons():
    rect_btn = button.RectButton(window, 0, 0, NORMAL_COLOUR, 20, 20, button_click, button_hover, button_normal, 2, False)
    bord_rect_btn = button.BorderedRectButton(window, 0, 0, NORMAL_COLOUR, BORDER_COLOUR, 20, 20, BORDER_WIDTH, button_click, button_hover, button_normal, 2, False)

    circ_btn = button.CircleButton(window, 0, 0, NORMAL_COLOUR, 10, button_click, button_hover, button_normal, False)
    bord_circ_btn = button.BorderedCircleButton(window, 0, 0, NORMAL_COLOUR, BORDER_COLOUR, 10, BORDER_WIDTH, button_click, button_hover, button_normal, False)

    return rect_btn, bord_rect_btn, circ_btn, bord_circ_btn


def create_horizontal_sliders():
    buttons = create_slider_buttons()

    sliders = []
    for i, x in enumerate(buttons):
        y = 175 + i * 50

        s = slider.HorizontalSlider(window, SLIDER_LENGTH, SLIDER_THICKNESS, 100, y, MIN_VALUE, MAX_VALUE, (MAX_VALUE - MIN_VALUE) // 2, SLIDER_COLOUR, slider_button=x)
        sliders.append(s)

    return sliders


def create_vertical_sliders():
    buttons = create_slider_buttons()

    sliders = []
    for i, j in enumerate(buttons):
        x = 250 + i * 50

        s = slider.VerticalSlider(window, SLIDER_LENGTH, SLIDER_THICKNESS, x, 250, MIN_VALUE, MAX_VALUE, (MAX_VALUE - MIN_VALUE) // 2, SLIDER_COLOUR, slider_button=j)
        sliders.append(s)

    return sliders


def update_sliders(sliders):
    window.fill((0, 0, 0))

    for i in sliders:
        i.update()

    pygame.display.update()


def main():
    hor_sliders = create_horizontal_sliders()
    vert_sliders = create_vertical_sliders()

    sliders = hor_sliders + vert_sliders

    while True:
        update_sliders(sliders)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


if __name__ == "__main__":
    main()