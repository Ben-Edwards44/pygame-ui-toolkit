import pygame
from os import getcwd
from src.elements import button


CLICK_IMG_PATH = f"{getcwd()}\\examples\\images\\smile3.png"
HOVER_IMG_PATH = f"{getcwd()}\\examples\\images\\smile2.png"
NORMAL_IMG_PATH = f"{getcwd()}\\examples\\images\\smile1.png"

WIDTH = 150
HEIGHT = 150


pygame.init()
window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Image buttons")


def on_click(btn):
    btn.update_image(CLICK_IMG_PATH)


def on_hover(btn):
    btn.update_image(HOVER_IMG_PATH)



def on_normal(btn):
    btn.update_image(NORMAL_IMG_PATH)


def create_button():
    btn = button.ImageButton(window, 250, 250, WIDTH, HEIGHT, NORMAL_IMG_PATH, on_click, on_hover, on_normal, False)

    return btn


def update_button(btn):
    window.fill((0, 0, 0))
    btn.update()
    pygame.display.update()


def main():
    btn = create_button()

    while True:
        update_button(btn)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


if __name__ == "__main__":
    main()