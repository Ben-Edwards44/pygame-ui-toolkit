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
    btn.image_path = CLICK_IMG_PATH
    btn.setup_image()


def on_hover(btn):
    btn.image_path = HOVER_IMG_PATH
    btn.setup_image()


def on_normal(btn):
    btn.image_path = NORMAL_IMG_PATH
    btn.setup_image()


def create_button():
    btn = button.ImageButton(window, 250, 250, WIDTH, HEIGHT, NORMAL_IMG_PATH, on_click, on_hover, on_normal, False)

    return btn


def update_buttons(btn):
    btn.update()
    pygame.display.update()


def main():
    btn = create_button()

    while True:
        update_buttons(btn)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


if __name__ == "__main__":
    main()