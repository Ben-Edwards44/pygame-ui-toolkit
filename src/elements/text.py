from src.elements import pygame
from . import pygame


class TextBox:
    def __init__(self, surface: pygame.Surface, text: str, background_colour: tuple[int], font_colour: tuple[int], font_size: int, font_name: str | None = None, antialias: bool = False) -> None:
        self.surface = surface
        
        self.text = text
        
        self.background_colour = background_colour
        self.font_colour = font_colour

        self.font_size = font_size
        self.font_name = font_name

        self.antialias = antialias

        self.text_surface, self.text_rect = self.get_text()

    def get_text(self) -> tuple[pygame.Surface, pygame.Rect]:
        font = pygame.font.Font(self.font_name, self.font_size)
        text_surface = font.render(self.text, self.antialias, self.font_colour)
        
        text_rect = text_surface.get_rect()

        if hasattr(self, "center"):
            text_rect.center = self.center
        else:
            raise Exception("TextBox class is not supposed to be used directly. Use another class like RectTextBox instead")

        return text_surface, text_rect

    def update_text(self, new_text: str, new_font_colour: tuple[int], new_font_size: int) -> None:
        self.text = new_text
        self.font_colour = new_font_colour
        self.font_size = new_font_size

        self.text_surface, self.text_rect = self.get_text()

    def blit_text(self) -> None:
        self.surface.blit(self.text_surface, self.text_rect)


class PolygonTextBox(TextBox):
    def __init__(self, surface: pygame.Surface, points: list[tuple[int, int]], text: str, background_colour: tuple[int], font_colour: tuple[int], font_size: int, font_name: str | None = None, antialias: bool = False) -> None:
        self.points = points
        self.center = self.get_center()

        super().__init__(surface, text, background_colour, font_colour, font_size, font_name, antialias)

    def get_center(self) -> tuple[int, int]:
        x_values = [i[0] for i in self.points]
        y_values = [i[1] for i in self.points]

        x = sum(x_values) // len(x_values)
        y = sum(y_values) // len(y_values)

        return x, y
    
    def draw(self) -> None:
        pygame.draw.polygon(self.surface, self.background_colour, self.points)
        self.blit_text()


class RectTextBox(PolygonTextBox):
    def __init__(self, surface: pygame.Surface, x: int, y: int, width: int, height: int, text: str, background_colour: tuple[int], font_colour: tuple[int], font_size: int, font_name: str | None = None, antialias: bool = False) -> None:
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        points = self.create_points()
        
        super().__init__(surface, points, text, background_colour, font_colour, font_size, font_name, antialias)

    def create_points(self) -> list[tuple[int, int]]:
        offset_x = self.width // 2
        offset_y = self.height // 2

        multipliers = ((-1, -1), (-1, 1), (1, 1), (1, -1))
        points = [(self.x + i * offset_x, self.y + j * offset_y) for i, j in multipliers]

        return points
    

class BorderedPolygonTextBox(PolygonTextBox):
    def __init__(self, surface: pygame.Surface, points: list[tuple[int, int]], text: str, background_colour: tuple[int], border_colour: tuple[int], border_width: int, font_colour: tuple[int], font_size: int, font_name: str | None = None, antialias: bool = False) -> None:
        print(text, background_colour, border_colour, border_width)
        self.border_colour = border_colour
        self.border_width = border_width
        
        super().__init__(surface, points, text, background_colour, font_colour, font_size, font_name, antialias)

    def draw(self) -> None:
        pygame.draw.polygon(self.surface, self.background_colour, self.points)
        pygame.draw.polygon(self.surface, self.border_colour, self.points, self.border_width)

        self.blit_text()


class BorderedRectTextBox(RectTextBox):
    def __init__(self, surface: pygame.Surface, x: int, y: int, width: int, height: int, text: str, background_colour: tuple[int], border_colour: tuple[int], border_width: int, font_colour: tuple[int], font_size: int, font_name: str | None = None, antialias: bool = False) -> None:
        super().__init__(surface, x, y, width, height, text, background_colour, font_colour, font_size, font_name, antialias)

        self.border_colour = border_colour
        self.border_width = border_width

    def draw(self) -> None:
        pygame.draw.polygon(self.surface, self.background_colour, self.points)
        pygame.draw.polygon(self.surface, self.border_colour, self.points, self.border_width)

        self.blit_text()