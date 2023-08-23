import pygame
from pygame_ui_toolkit.elements import toggle, text


TICK_COLOUR = (0, 0, 0)
TICK_THICKNESS = 6

TICK_BOX_COLOUR = (255, 255, 255)
OUTER_COLOUR = (150, 150, 150)

WIDTH = 200
HEIGHT = 50

FONT_COLOUR = (255, 255, 255)
FONT_SIZE = 32
FONT_NAME = None

CORNER_RADIUS = 5


pygame.init()
window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Toggles")


def create_toggles():
    left_tick = toggle.TickBoxToggle(window, TICK_THICKNESS, TICK_COLOUR, TICK_BOX_COLOUR, OUTER_COLOUR, 300, 100, WIDTH, HEIGHT, "Tick box", FONT_COLOUR, FONT_SIZE, FONT_NAME, inner_corner_radius=CORNER_RADIUS, outer_corner_radius=CORNER_RADIUS)
    right_tick = toggle.TickBoxToggle(window, TICK_THICKNESS, TICK_COLOUR, TICK_BOX_COLOUR, OUTER_COLOUR, 300, 400, WIDTH, HEIGHT, "Tick box", FONT_COLOUR, FONT_SIZE, FONT_NAME, inner_corner_radius=CORNER_RADIUS, outer_corner_radius=CORNER_RADIUS, text_to_right=False)

    return [left_tick, right_tick]


def create_text_boxes():
    text_box1 = text.RectTextBox(window, 100, 100, HEIGHT, HEIGHT, "unselected", TICK_BOX_COLOUR, FONT_COLOUR, FONT_SIZE, FONT_NAME, CORNER_RADIUS)
    text_box2 = text.RectTextBox(window, 100, 400, HEIGHT, HEIGHT, "unselected", TICK_BOX_COLOUR, FONT_COLOUR, FONT_SIZE, FONT_NAME, CORNER_RADIUS)

    return [text_box1, text_box2]


def update_toggles(toggles):
    for i in toggles:
        i.update()


def update_text(text_boxes, toggles):
    for i, x in enumerate(text_boxes):
        selected = toggles[i].selected
        txt = "selected" if selected else "unselected"

        x.update_text(txt, FONT_COLOUR, FONT_SIZE, FONT_NAME)
        x.blit_text()


def update(toggles, text_boxes):
    window.fill((0, 0, 0))

    update_toggles(toggles)
    update_text(text_boxes, toggles)

    pygame.display.update()


def main():
    toggles = create_toggles()
    text_boxes = create_text_boxes()

    while True:
        update(toggles, text_boxes)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


if __name__ == "__main__":
    main()