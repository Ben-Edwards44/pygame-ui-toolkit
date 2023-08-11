import pygame
from src.elements import dropdown


OPTIONS = ["Option 1", "Option 2", "Option 3"]

FONT_COLOUR = (0, 0, 0)
FONT_SIZE = 30

BACKGROUND_COLOUR = (255, 255, 255)
BORDER_COLOUR = (255, 0, 0)

BORDER_WIDTH = 2


pygame.init()
window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Dropdown menus")


def on_click():
    print("click")


def create_dropdowns():
    rect = dropdown.RectDropdown(window, OPTIONS, 100, 100, BACKGROUND_COLOUR, 95, 50, FONT_COLOUR, FONT_SIZE, on_click=on_click)
    bord_rect = dropdown.BorderedRectDropdown(window, OPTIONS, 200, 100, BACKGROUND_COLOUR, BORDER_COLOUR, 95, 50, BORDER_WIDTH, FONT_COLOUR, FONT_SIZE, on_click=on_click)

    circ = dropdown.CircleDropdown(window, OPTIONS, 300, 100, BACKGROUND_COLOUR, 45, FONT_COLOUR, FONT_SIZE, on_click=on_click)
    bord_circ = dropdown.BorderedCircleDropdown(window, OPTIONS, 400, 100, BACKGROUND_COLOUR, BORDER_COLOUR, 45, BORDER_WIDTH, FONT_COLOUR, FONT_SIZE, on_click=on_click)

    return [rect, bord_rect, circ, bord_circ]


def update_dropdowns(dropdowns):
    window.fill((0, 0, 0))

    for i in dropdowns:
        i.update()

    pygame.display.update()


def main():
    dropdowns = create_dropdowns()

    while True:
        update_dropdowns(dropdowns)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


if __name__ == "__main__":
    main()