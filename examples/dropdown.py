import pygame
from src.elements import dropdown


OPTIONS = ["Option 1", "Option 2", "Option 3"]


pygame.init()
window = pygame.display.set_mode((500, 500))


def create_dropdowns():
    d = dropdown.RectDropdown(window, OPTIONS, 250, 250, (255, 255, 255), 200, 50, (0, 0, 0), 32)

    return [d]


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