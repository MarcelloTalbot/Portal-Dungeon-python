from settings import *

class Main_Menu_Button():
    def __init__(self, next_state, x, y, up, down):#, display):
        self.pos = pygame.math.Vector2((x, y))
        self.up = up
        self.down = down
        self.image = self.up
        self.rect = self.image.get_rect(center = (round(self.pos.x), round(self.pos.y)))
        self.group = [self.rect, self.image, self.up, self.down]
        # self.display = display
        self.clicked = False
        self.next_state = next_state

    def update(self, m_pos, click, m_player):
        self.mouse_hover(m_pos, click, m_player)
        
        self.group = [self.rect, self.image, self.up, self.down]
        
        return self.clicked

    def mouse_hover(self, m_pos, click, m_player):
        if self.rect.collidepoint(m_pos):
            if self.image != self.down:#don't really need
                self.image = self.down
                if m_player.hitbox.colliderect(self.rect.topleft[0]+8, self.rect.topleft[1]+8, self.rect.topright[0]-self.rect.topleft[0]-16, self.rect.bottomleft[1]-self.rect.topleft[1]-32):
                    m_player.pos.y += 16
            if click:
                self.clicked = True
        else:
            if self.image != self.up:#dont really need
                self.image = self.up
                if m_player.hitbox.colliderect(self.rect.topleft[0]+8, self.rect.topleft[1]+8+16, self.rect.topright[0]-self.rect.topleft[0]-16, self.rect.bottomleft[1]-self.rect.topleft[1]-32):
                    m_player.pos.y -= 16

    def render(self):
        display.blit(self.image, self.rect)

class Play_Button(Main_Menu_Button):
    def __init__(self, next_state = 'Playing', x = d_width/2, y = d_height/2, up = play_u, down = play_d):
        super().__init__(next_state, x, y, up, down)
        
    def update(self, m_pos, click, m_player):
        return super().update(m_pos, click, m_player)
    
    def render(self):
        super().render()
        
class Quit_Button(Main_Menu_Button):
    def __init__(self, next_state = 'Quit_Menu', x = d_width/2, y = d_height/1.13, up = quit_u, down = quit_d):
        super().__init__(next_state, x, y, up, down)
        
    def update(self, m_pos, click, m_player):
        return super().update(m_pos, click, m_player)
    
    def render(self):
        super().render()

class Control_Button(Main_Menu_Button):
    def __init__(self, next_state = 'Control_Menu', x = d_width/2, y = d_height/1.45, up = ctrl_u, down = ctrl_d):
        super().__init__(next_state, x, y, up, down)
        
    def update(self, m_pos, click, m_player):
        return super().update(m_pos, click, m_player)
    
    def render(self):
        super().render()

class Button():
    def __init__(self, next_state, x, y, up, down):
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
        
        return self.clicked
        
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
        
class Yes_Button(Button):
    def __init__(self, next_state, x = d_width*0.4, y = d_height/1.45, up = yes_u, down = yes_d):
        super().__init__(next_state, x, y, up, down)
        
    def update(self, m_pos, click):
        return super().update(m_pos, click)
    
    def render(self):
        super().render()

class No_Button(Button):
    def __init__(self, next_state, x = d_width*0.6, y = d_height/1.45, up = no_u, down = no_d):
        super().__init__(next_state, x, y, up, down)
        
    def update(self, m_pos, click):
        return super().update(m_pos, click)
    
    def render(self):
        super().render()
        
class Back_Button(Button):
    def __init__(self, next_state, x = d_width/2, y = d_height*0.92, up = back_u, down = back_d):
        super().__init__(next_state, x, y, up, down)
    
    def update(self, m_pos, click):
        return super().update(m_pos, click)
    
    def render(self):
        super().render()

class Continue_Button(Button):
    def __init__(self, next_state = 'Playing', x = d_width/2, y = d_height/2, up = cont_u, down = cont_d):
        super().__init__(next_state, x, y, up, down)
    
    def update(self, m_pos, click):
        return super().update(m_pos, click)
    
    def render(self):
        super().render()

class Main_Button(Button):
    def __init__(self, next_state = 'Main_Menu', x = d_width/2, y = d_height/1.45, up = main_u, down = main_d):
        super().__init__(next_state, x, y, up, down)
    
    def update(self, m_pos, click):
        return super().update(m_pos, click)
    
    def render(self):
        super().render()
        
class Quit_Button_2(Button):
    def __init__(self, next_state = 'Quit_Menu', x = d_width/2, y = d_height/1.13, up = quit_u, down = quit_d):
        super().__init__(next_state, x, y, up, down)
    
    def update(self, m_pos, click):
        return super().update(m_pos, click)
    
    def render(self):
        super().render()
        
class Respawn_Button(Button):
    def __init__(self, next_state = 'Playing', x = d_width/2, y = d_height/2, up = rspn_u, down = rspn_d):
        super().__init__(next_state, x, y, up, down)
    
    def update(self, m_pos, click):
        return super().update(m_pos, click)
    
    def render(self):
        super().render()
        
class Retry_Button(Button):
    def __init__(self, next_state = 'Playing', x = d_width/2, y = d_height/2, up = rtry_u, down = rtry_d):
        super().__init__(next_state, x, y, up, down)
    
    def update(self, m_pos, click):
        return super().update(m_pos, click)
    
    def render(self):
        super().render()