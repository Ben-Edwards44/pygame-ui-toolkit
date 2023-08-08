import pygame
from src.elements import button


CLICK_COLOUR = (255, 0, 0)
HOVER_COLOUR = (0, 0, 255)
NORMAL_COLOUR = (0, 255, 0)

BORDER_COLOUR = (255, 255, 255)
BORDER_WIDTH = 5


pygame.init()
window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Colour changing buttons")


def on_click(btn):
    btn.background_colour = CLICK_COLOUR


def on_hover(btn):
    btn.background_colour = HOVER_COLOUR


def on_normal(btn):
    btn.background_colour = NORMAL_COLOUR


def create_buttons():
    rect_btn = button.RectButton(window, 100, 100, NORMAL_COLOUR, 50, 50, on_click, on_hover, on_normal, 10, False)
    circ_btn = button.CircleButton(window, 400, 100, NORMAL_COLOUR, 25, on_click, on_hover, on_normal, False)
    bord_rect_btn = button.BorderedRectButton(window, 100, 400, NORMAL_COLOUR, BORDER_COLOUR, 50, 50, BORDER_WIDTH, on_click, on_hover, on_normal, 10, False)
    bord_circ_btn = button.BorderedCircleButton(window, 400, 400, NORMAL_COLOUR, BORDER_COLOUR, 25, BORDER_WIDTH, on_click, on_hover, on_normal, False)
    polygon_btn = button.PolygonButton(window, [(325, 300), (375, 300), (400, 250), (350, 215), (300, 250)], NORMAL_COLOUR, on_click, on_hover, on_normal, False)
    bord_polygon_btn = button.BorderedPolygonButton(window, [(125, 300), (175, 300), (200, 250), (150, 215), (100, 250)], NORMAL_COLOUR, BORDER_COLOUR, BORDER_WIDTH, on_click, on_hover, on_normal, False)

    return [rect_btn, circ_btn, bord_rect_btn, bord_circ_btn, polygon_btn, bord_polygon_btn]


def update_buttons(buttons):
    for btn in buttons:
        btn.update()

    pygame.display.update()


def main():
    buttons = create_buttons()

    while True:
        update_buttons(buttons)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


if __name__ == "__main__":
    main()