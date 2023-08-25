import pygame
from pygame_ui_toolkit.elements import button
from pygame_ui_toolkit.presets.buttons import colour_change, size_change


CLICK_COLOUR = (255, 0, 0)
HOVER_COLOUR = (0, 0, 255)
NORMAL_COLOUR = (0, 255, 0)

NORMAL_SIZE = (50, 50)
HOVER_SIZE = (60, 60)
CLICK_SIZE = (40, 40)

BORDER_COLOUR = (255, 255, 255)
BORDER_WIDTH = 5


pygame.init()
window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Buttons")


def create_buttons():
    rect_btn = button.RectButton(window, 100, 100, NORMAL_COLOUR, 50, 50)
    circ_btn = button.CircleButton(window, 100, 200, NORMAL_COLOUR, 25)
    bord_rect_btn = button.BorderedRectButton(window, 100, 300, NORMAL_COLOUR, BORDER_COLOUR, 50, 50, BORDER_WIDTH)
    bord_circ_btn = button.BorderedCircleButton(window, 100, 400, NORMAL_COLOUR, BORDER_COLOUR, 25, BORDER_WIDTH)
    polygon_btn = button.PolygonButton(window, [(200, 150), (250, 150), (275, 100), (225, 65), (175, 100)], NORMAL_COLOUR)
    bord_polygon_btn = button.BorderedPolygonButton(window, [(200, 300), (250, 300), (275, 250), (225, 215), (175, 250)], NORMAL_COLOUR, BORDER_COLOUR, BORDER_WIDTH)

    rect_btn2 = button.RectButton(window, 400, 100, NORMAL_COLOUR, 50, 50)
    circ_btn2 = button.CircleButton(window, 400, 200, NORMAL_COLOUR, 25)
    bord_rect_btn2 = button.BorderedRectButton(window, 400, 300, NORMAL_COLOUR, BORDER_COLOUR, 50, 50, BORDER_WIDTH)
    bord_circ_btn2 = button.BorderedCircleButton(window, 400, 400, NORMAL_COLOUR, BORDER_COLOUR, 25, BORDER_WIDTH)

    return [rect_btn, circ_btn, bord_rect_btn, bord_circ_btn, polygon_btn, bord_polygon_btn, rect_btn2, circ_btn2, bord_rect_btn2, bord_circ_btn2]


def prepare_buttons(buttons):
    for i, x in enumerate(buttons):
        if i < 6:
            colour_change.change_existing_button(x, NORMAL_COLOUR, HOVER_COLOUR, CLICK_COLOUR)
        else:
            if type(x) == button.RectButton or type(x) == button.BorderedRectButton:
                size_change.change_existing_button(x, NORMAL_SIZE, HOVER_SIZE, CLICK_SIZE)
            else:
                size_change.change_existing_button(x, NORMAL_SIZE[0] // 2, HOVER_SIZE[0] // 2, CLICK_SIZE[0] // 2)


def update_buttons(buttons):
    window.fill((0, 0, 0))

    for btn in buttons:
        btn.update()

    pygame.display.update()


def main():
    buttons = create_buttons()
    prepare_buttons(buttons)

    while True:
        update_buttons(buttons)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


if __name__ == "__main__":
    main()