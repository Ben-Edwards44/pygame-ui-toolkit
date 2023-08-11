from src.elements import button
import pygame


TEXT_COLOUR = (0, 0, 0)
BUTTON_COLOUR = (255, 255, 255)
FONT_COLOUR = (0, 0, 0)
BORDER_COLOUR = (0, 255, 0)
BORDER_WIDTH = 5
START_TEXT = "Clicked: 0"
FONT_SIZE = 32


pygame.init()
window = pygame.display.set_mode((500, 500))


def get_num(string):
    string = string.split(": ")
    num_click = int(string[-1])

    return num_click


def on_click(btn: button.TextWrapper):
    num_click = get_num(btn.text)
    num_click += 1

    btn.update_text(f"Clicked: {num_click}", FONT_COLOUR, FONT_SIZE)


def button1():
    on_click(buttons[0])


def button2():
    on_click(buttons[1])


def button3():
    on_click(buttons[2])


def button4():
    on_click(buttons[3])


def create_buttons():
    btn1 = button.RectButton(window, 150, 150, BUTTON_COLOUR, 125, 50, button1)
    btn2 = button.CircleButton(window, 350, 150, BUTTON_COLOUR, 62, button2)
    btn3 = button.BorderedRectButton(window, 150, 350, BUTTON_COLOUR, BORDER_COLOUR, 125, 50, BORDER_WIDTH, button3)
    btn4 = button.BorderedCircleButton(window, 350, 350, BUTTON_COLOUR, BORDER_COLOUR, 62, BORDER_WIDTH, button4)

    buttons = [btn1, btn2, btn3, btn4]

    text_wrappers = [button.TextWrapper(i, START_TEXT, FONT_COLOUR, FONT_SIZE) for i in buttons]

    return text_wrappers


def update_buttons():
    for btn in buttons:
        btn.update()

    pygame.display.update()


def main():
    global buttons

    buttons = create_buttons()

    while True:
        update_buttons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()