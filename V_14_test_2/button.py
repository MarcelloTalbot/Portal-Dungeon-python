from settings import *
from game_states_file import *

class Main_Menu_Button():
    def __init__(self, x, y, up, down):#, next_state):#display):
        self.pos = pygame.math.Vector2((x, y))
        self.up = up
        self.down = down
        self.image = self.up
        self.rect = self.image.get_rect(center = (round(self.pos.x), round(self.pos.y)))
        self.group = [self.rect, self.image, self.up, self.down]
        # self.display = display
        self.clicked = False
        # self.next_state = next_state

    def update(self, m_pos, click, m_player):
        self.mouse_hover(m_pos, click , m_player)
        self.group = [self.rect, self.image, self.up, self.down]
        # self.render()
        if self.clicked:
            self.clicked = False
            return True
        else:
            return False

    def mouse_hover(self, m_pos, click, m_player):
        if self.rect.collidepoint(m_pos):
            if self.image != self.down:
                self.image = self.down
                if m_player.hitbox.colliderect(self.rect.topleft[0]+8, self.rect.topleft[1]+8, self.rect.topright[0]-self.rect.topleft[0]-16, self.rect.bottomleft[1]-self.rect.topleft[1]-32):
                    m_player.pos.y += 16
            if click:
                self.clicked = True
        else:
            if self.image != self.up:
                self.image = self.up
                if m_player.hitbox.colliderect(self.rect.topleft[0]+8, self.rect.topleft[1]+8+16, self.rect.topright[0]-self.rect.topleft[0]-16, self.rect.bottomleft[1]-self.rect.topleft[1]-32):
                    m_player.pos.y -= 16

    def render(self):
        display.blit(self.image, self.rect)

class Play_Button(Main_Menu_Button):
    def __init__(self, x, y, up = play_u, down = play_d, next_state = Playing()):
        super().__init__(x, y, up, down)
        self.next_state = next_state
        
    def update(self, m_pos, click, m_player):
        self.mouse_hover(m_pos, click , m_player)
        self.group = [self.rect, self.image, self.up, self.down]
        # if self.clicked:
        #     return Playing()
        # if self.clicked:
        #     self.clicked = False
        #     return True
        # else:
        #     return False
        return self.clicked
    
    def mouse_hover(self, m_pos, click, m_player):
        super().mouse_hover(m_pos, click, m_player)
    
    def render(self):
        super().render()

class Button():
    def __init__(self, x, y, up, down, next_state):
        self.pos = pygame.math.Vector2((x, y))
        self.up = up
        self.down = down
        self.image = self.up
        self.rect = self.image.get_rect(center = (round(self.pos.x), round(self.pos.y)))
        self.group = [self.rect, self.image, self.up, self.down]
        self.clicked = False
        self.next_state = next_state
        
    def update(self, m_pos, click):
        self.mouse_hover(m_pos, click)
        
        self.group = [self.rect, self.image, self.up, self.down]
        
        if self.clicked:
            self.clicked = False
            return True
        else:
            return False
        
    def mouse_hover(self, m_pos, click):
        if self.rect.collidepoint(m_pos):
            if self.image != self.down:
                self.image = self.down
            if click:
                self.clicked = True
        else:
            if self.image != self.up:
                self.image = self.up
        
    def render(self):
        display.blit(self.image, self.rect)