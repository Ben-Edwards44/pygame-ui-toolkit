import pygame
from src.elements import toggle


TICK_COLOUR = (0, 0, 0)
TICK_THICKNESS = 6

TICK_BOX_COLOUR = (255, 255, 255)
OUTER_COLOUR = (150, 150, 150)

WIDTH = 200
HEIGHT = 50

FONT_COLOUR = (255, 255, 255)
FONT_SIZE = 32


pygame.init()
window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Toggles")


def on_value_changed(value):
    print(f"Toggle value: {value}")


def create_toggles():
    left_tick = toggle.TickBoxToggle(window, TICK_THICKNESS, TICK_COLOUR, TICK_BOX_COLOUR, OUTER_COLOUR, 250, 100, WIDTH, HEIGHT, "Tick box", FONT_COLOUR, FONT_SIZE, on_value_changed=on_value_changed, inner_corner_radius=5, outer_corner_radius=8)
    right_tick = toggle.TickBoxToggle(window, TICK_THICKNESS, TICK_COLOUR, TICK_BOX_COLOUR, OUTER_COLOUR, 250, 400, WIDTH, HEIGHT, "Tick box", FONT_COLOUR, FONT_SIZE, on_value_changed=on_value_changed, inner_corner_radius=5, outer_corner_radius=8, text_to_right=False)

    return [left_tick, right_tick]


def update_toggles(toggles):
    window.fill((0, 0, 0))

    for i in toggles:
        i.update()

    pygame.display.update()


def main():
    toggles = create_toggles()

    while True:
        update_toggles(toggles)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


if __name__ == "__main__":
    main()