import pygame
from src.elements import text


TEXT = "Hello, World!"

BACKGROUND_COLOUR = (255, 255, 255)

BORDER_COLOUR = (0, 255, 0)
BORDER_WIDTH = 4

FONT_COLOUR = (0, 0, 0)
FONT_SIZE = 24


pygame.init()
window = pygame.display.set_mode((500, 500))


def create_text_boxes():
    polygon_b = text.PolygonTextBox(window, [(200, 200), (300, 200), (350, 250), (300, 300), (200, 300)], TEXT, BACKGROUND_COLOUR, FONT_COLOUR, FONT_SIZE)
    bord_polygon_b = text.BorderedPolygonTextBox(window, [(200, 350), (300, 350), (350, 400), (300, 450), (200, 450)], TEXT, BACKGROUND_COLOUR, BORDER_COLOUR, BORDER_WIDTH, FONT_COLOUR, FONT_SIZE)

    rect_b = text.RectTextBox(window, 250, 80, 200, 50, TEXT, BACKGROUND_COLOUR, FONT_COLOUR, FONT_SIZE)
    bord_rect_b = text.BorderedRectTextBox(window, 250, 150, 200, 50, TEXT, BACKGROUND_COLOUR, BORDER_COLOUR, BORDER_WIDTH, FONT_COLOUR, FONT_SIZE)

    circ_b = text.CircleTextBox(window, 100, 250, 50, TEXT, BACKGROUND_COLOUR, FONT_COLOUR, FONT_SIZE)
    bord_circ_b = text.BorderedCircleTextBox(window, 440, 250, 50, TEXT, BACKGROUND_COLOUR, BORDER_COLOUR, BORDER_WIDTH, FONT_COLOUR, FONT_SIZE)

    return [polygon_b, bord_polygon_b, rect_b, bord_rect_b, circ_b, bord_circ_b]


def draw_boxes(text_boxes):
    for i in text_boxes:
        i.draw()

    pygame.display.update()


def main():
    text_boxes = create_text_boxes()
    draw_boxes(text_boxes)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


if __name__ == "__main__":
    main()