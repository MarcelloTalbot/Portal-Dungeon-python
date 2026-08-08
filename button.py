from settings import *

class Button():
    def __init__(self,x,y,up,down,display):
        self.pos = pygame.math.Vector2((x,y))
        self.up = up
        self.down = down
        self.image = self.up
        self.rect = self.image.get_rect(center = (round(self.pos.x),round(self.pos.y)))
        self.group = [self.rect,self.image,self.up,self.down]
        self.display = display
        self.clicked = False

    def update(self,mx,my,click,m_player):
        self.mouse_hover(mx,my,click,m_player)
        self.group = [self.rect,self.image,self.up,self.down]
        self.render()
        if self.clicked:
            self.clicked = False
            return True
        else:
            return False

    def mouse_hover(self,mx,my,click,m_player):
        if self.rect.collidepoint((mx,my)):
            if self.image != self.down:
                self.image = self.down
                if m_player.hitbox.colliderect(self.rect.topleft[0]+8,self.rect.topleft[1]+8,self.rect.topright[0]-self.rect.topleft[0]-16,self.rect.bottomleft[1]-self.rect.topleft[1]-32):
                    m_player.pos.y += 16
            if click:
                self.clicked = True
        else:
            if self.image != self.up:
                self.image = self.up
                if m_player.hitbox.colliderect(self.rect.topleft[0]+8,self.rect.topleft[1]+8+16,self.rect.topright[0]-self.rect.topleft[0]-16,self.rect.bottomleft[1]-self.rect.topleft[1]-32):
                    m_player.pos.y -= 16

    def render(self):
        self.display.blit(self.image,self.rect)
                    
