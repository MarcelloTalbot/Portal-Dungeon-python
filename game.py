import pygame
from pygame.locals import *#dont know if needed now
from settings import *
from game_states_file import *

class Game():#might be able to be just one function with __init__ as section just above update (may be better for globalling display)
    def __init__(self):
        self.game_state = Main_Menu(None)
        
        self.game_running = True
                
    def update(self):#working version of update_1_1, I don't know why it never equalled __class__
        while self.game_running:
            self.next_state = self.game_state.update()
            try:
                self.game_state = globals()[self.next_state](self.game_state.__class__.__name__)
            except:
                print(self.next_state)
                self.game_running = False
                
def set_global_vars():#with this settings can be removed
    global screen, d_width, d_height, display, img_dir#, m_pos
    screen = pygame.display.Info()
    d_width = screen.current_w
    d_height = screen.current_h
    display = pygame.display.set_mode(flags=FULLSCREEN)
    img_dir = 'images/'
    # m_pos = pygame.math.Vector2(pygame.mouse.get_pos())