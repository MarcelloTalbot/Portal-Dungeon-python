import pygame,random
from settings import *

class Tile(pygame.sprite.DirtySprite):
    def __init__(self,t_type,image,x,y):
        super().__init__()
        self.type = "tile"
        self.life = "alive"
        pygame.sprite.DirtySprite.__init__(self)
        self.t_type = t_type
        self.pos = pygame.math.Vector2((x,y))
        self.image = image
        self.scal_image = pygame.transform.scale(self.image,(tile_scale,tile_scale))
        self.rot_image = self.scal_image
        if t_type == "grass" or t_type == "flower_grass" or t_type == "snowy_grass" or t_type == "mud":
            self.rot_image = pygame.transform.rotate(self.scal_image,(90*random.randint(0,3)))
        self.rect = self.scal_image.get_rect(topleft = (round(self.pos.x), round(self.pos.y)))
        if t_type == "mud":
            self.speed_mult = 0.5
        elif t_type == "snowy_grass":
            self.speed_mult = 2/3
        else:
            self.speed_mult = 1
        self.dirty = 1
        self.z = 0

class Portal(pygame.sprite.DirtySprite):
    def __init__(self,t_type,image,pos):
        super().__init__()
        self.type = "portal"
        self.life = "alive"
        pygame.sprite.DirtySprite.__init__(self)
        self.t_type = t_type
        self.pos_1 = pygame.math.Vector2((pos[0],pos[1]))
        self.pos_2 = pygame.math.Vector2((pos[2],pos[3]))
        self.image = image
        self.scal_image = pygame.transform.scale(self.image,(tile_scale,tile_scale))
        self.rect_1 = self.scal_image.get_rect(topleft = (round(self.pos_1.x),round(self.pos_1.y)))
        self.rect_2 = self.scal_image.get_rect(topleft = (round(self.pos_2.x),round(self.pos_2.y)))
        self.speed_mult = 1
        self.dirty = 1
        self.z = 1
        #self.timer = 90

    #def update(self):
    #    if self.timer < 90:
    #        self.timer += 1
