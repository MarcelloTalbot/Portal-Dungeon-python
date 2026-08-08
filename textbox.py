import pygame

def text_objects(text, font, c):
    textSurface = font.render(text, True, c)
    return textSurface, textSurface.get_rect()

class textbox():
    def __init__(self, x, y, size, colour, gd):
        self.x = x
        self.y = y
        self.s = size
        self.c = colour
        self.gd = gd
        self.name = 'txt'

    def draw_l(self, text):
        fontstyle = pygame.font.Font('freesansbold.ttf', self.s)
        TextSurf, TextRect = text_objects(text, fontstyle, self.c)
        TextRect.topleft = self.x, self.y
        self.gd.blit(TextSurf, TextRect)

    def draw_c(self, text):
        fontstyle = pygame.font.Font('freesansbold.ttf', self.s)
        TextSurf, TextRect = text_objects(text, fontstyle, self.c)
        TextRect.center = self.x, self.y
        self.gd.blit(TextSurf, TextRect)

    def draw_r(self, text):
        fontstyle = pygame.font.Font('freesansbold.ttf', self.s)
        TextSurf, TextRect = text_objects(text, fontstyle, self.c)
        TextRect.topright = self.x, self.y
        self.gd.blit(TextSurf, TextRect)

