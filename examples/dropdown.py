import pygame
from src.elements import dropdown


OPTIONS = ["Option 1", "Option 2", "Option 3"]


pygame.init()
window = pygame.display.set_mode((500, 500))


def create_dropdowns():
    rect = dropdown.RectDropdown(window, OPTIONS, 250, 100, (255, 255, 255), 100, 50, (0, 0, 0), 32)
    bord_rect = dropdown.BorderedRectDropdown(window, OPTIONS, 100, 100, (255, 255, 255), (255, 0, 0), 100, 50, 5, (0, 0, 0), 32)

    circ = dropdown.CircleDropdown(window, OPTIONS, 400, 100, (255, 255, 255), 50, (0, 0, 0), 32)

    return [rect, bord_rect, circ]


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