from button import *
from textbox import *
from settings import *
from camera import *
from entity import *

#common functions that can occur in __init__ funcs can go here? and others I think?
# def

class Game_State():
    def __init__(self):
        #mouse inputs
        self.m_pos = pygame.math.Vector2((0, 0))
        self.click = False
        self.sprites = pygame.sprite.Group()
        self.bob = Menu_player(d_width/10 ,d_height/10, display, plrhd, plrrm)
        self.sprites.add(self.bob)
        self.txt = textbox(d_width/2, d_height/2, 150, white, display)
        self.classes = [self.txt]
        
        self.classes_2 = [self.bob, self.txt]
        
    def update(self):
        self.game_state = self.own_state
        
        self.input_detection()
        
    def input_detection(self):
        pass

    def render(self):
        pass
    
    #I think this will remove all data (from RAM?) of every class instance in the game state?
    #I don't know which is better or if they're needed
    def die_delete(self):
        for c in range(0, len(self.classes_2)):
            delattr(self, self.classes_2[c].name)
            
        self.classes.clear()
        self.sprites.empty()
        
    def die_replace(self):
        for c in range (0, len(self.classes)):
            setattr(self, self.classes[c].name, None)
            
        for sprite in self.sprites:
            sprite.kill()
            setattr(self, sprite.name, None)
            
        self.classes.clear()
            
# s = Game_State()

# print("Before:")
# print(s.bob)
# print(len(s.sprites))
# print(s.txt)
# print(len(s.classes))
# print(len(s.classes_2))

# s.die_del()

# print("After:")
# # print(s.bob)#hash this if s.die_delete()
# print(len(s.sprites))
# # print(s.txt)#hash this if s.die_delete()
# print(len(s.classes))
# print(len(s.classes_2))