import pygame

def text_objects(text, font, c):
    textSurface = font.render(text, True, c)
    return textSurface, textSurface.get_rect()#might not need rect just use the pos

class textbox():#?more like text and not textbox? or updating text
    def __init__(self, x, y, size, colour, gd):#, has_bg = False):
        self.x = x
        self.y = y
        self.s = size
        self.c = colour
        self.gd = gd
        self.name = 'txt'
        # self.has_background = has_bg
        # self.background_colour = (88, 88, 88)
        # self.background = pygame.rect.Rect()

    def draw_l(self, text):
        fontstyle = pygame.font.Font('freesansbold.ttf', self.s)
        TextSurf, TextRect = text_objects(text, fontstyle, self.c)
        TextRect.topleft = self.x, self.y
        self.gd.blit(TextSurf, TextRect)

    def draw_c(self, text):
        fontstyle = pygame.font.Font('freesansbold.ttf', self.s)
        TextSurf, TextRect = text_objects(text, fontstyle, self.c)
        TextRect.midtop = self.x, self.y
        self.gd.blit(TextSurf, TextRect)

    def draw_r(self, text):
        fontstyle = pygame.font.Font('freesansbold.ttf', self.s)
        TextSurf, TextRect = text_objects(text, fontstyle, self.c)
        TextRect.topright = self.x, self.y
        self.gd.blit(TextSurf, TextRect)

class Text():
    def __init__(self, x:float|int, y:float|int, size:float|int, colour:tuple|list, gd:pygame.surface, text:str=..., fontstyle:str='freesansbold.ttf', has_bg:bool=False):
        # super().__init__(text)
        self.x = x
        self.y = y
        self.s = size
        if len(colour) != 3:
            raise ValueError('"colour" must have 3 elements each being an integer from 0 to 255')
        for value in colour:
            if not isinstance(value, int):
                raise TypeError('Each element must be an integer')
            if value < 0 or value > 255:
                raise ValueError('Int must be between 0 and 255')
        self.c = colour
        self.gd = gd
        self.fontstyle = fontstyle
        self.font = pygame.font.Font(fontstyle, size)
        self.text = text
        # self.has_background = has_bg
        # self.background_colour = (88, 88, 88)
        # self.background = pygame.rect.Rect(x-3, y-3, size*len(text)/2, size)

    def draw_l(self):
        TextSurf, TextRect = text_objects(self.text, self.font, self.c)
        TextRect.topleft = self.x, self.y
        # pygame.draw.rect(self.gd, self.background_colour, self.background)
        self.gd.blit(TextSurf, TextRect)
        
    def draw_c(self):
        TextSurf, TextRect = text_objects(self.text, self.font, self.c)
        TextRect.center = self.x, self.y
        # pygame.draw.rect(self.gd, self.background_colour, self.background)
        self.gd.blit(TextSurf, TextRect)
        
    # for x in str.:
    #     def 
    
    def __add__(self, other):
        if isinstance(other, str):
            return Text(self.x, self.y, self.s, self.c, self.gd, self.text + other, self.font)
        elif isinstance(other, Text):
            return Text(self.x, self.y, self.s, self.c, self.gd, self.text + other.text, self.font)
        else:
            raise TypeError()
    
    def __iadd__(self, other):
        if isinstance(other, str):
            self.text += other
        elif isinstance(other, Text):
            self.text += other.text
        # elif isinstance(other, list):
        else:
            raise TypeError()
    
    def __str__(self):
        return '"' + self.text + f'" in size {self.s} and colour {self.c} {self.font} at ({self.x}, {self.y}) on {self.gd}'
    
# class str():
#     def __init__(self) -> None:
#         pass
# text = Text(0,0,1,(0,0,0),None,"no")
# print(text)
# string = "no"
# str.

class Lined_Text(list):
    def __init__(self, x, y, size, colour, gd, string:str=...):#, text:Text=...):#, lined_text:Lined_Text=...):#maybe just list and ignore anything thats not a 
        self.x = x
        self.y = y
        self.s = size
        self.c = colour
        self.gd = gd
        split_text = string.split('\n')
        self.lines = []
        # self = []
        for line in range(len(split_text)):
            self.lines.append(Text(x, y, size, colour, gd, split_text[line]))
        # self.text = []
        # self.lines.append(text)
        self.draw_func = self.draw_l
        
    def draw_l(self):
        for line in self.lines:
            line.draw_l()
    
    def replace_text(self, text):
        # self.text = text.split('\n')
        # for line in self.text:
        #     newText = textbox(self.x, self.y, )
        
        # for line in text.split('\n'):
        #     newText = Text(self.x, self.y, self.s, self.c, self.gd, )
        #     try:
        #         self.text[line]
        #     self.text.append(newText)
        
        split_text = text.split('\n')
        for line in range(len(split_text)):
            try:
                self[line] = split_text[line]
            except:
                newText = Text(self.x, self.y, self.s, self.c, self.gd, split_text[line])
                
    def __add__(self, other):
        if isinstance(other, str):
            self.lines.append(Text(self.x, self.y, self.s, self.c, self.gd, other, self.font))
                
    def __str__(self):
        return 

class Text_Box():#list):
    def __init__(self, x, y, gd):
        self.x = x
        self.y = y
        self.gd = gd
        self.text = [[]]
        
    def render(self):
        pass
    
    def update_text(self, text):
        for letter in text:
            pass
    
    def clear(self):
        self.text = []