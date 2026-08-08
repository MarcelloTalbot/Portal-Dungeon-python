import pygame
from pygame.locals import *#dont know if needed now
from settings import *
from game_states_file import *

class Game():#might be able to be just one function with __init__ as section just above update (may be better for globalling display)
    def __init__(self):

        # self.player = Player()
        
        # self.clock = pygame.time.Clock()#maybe only clock in Playing?

        self.game_state = Main_Menu(None)#globals()['Main_Menu']()
        
        self.game_running = True
    
    def update_1(self):#if game actually crashes then I won't know exactly what happened only which state it was in
        while self.game_running:
            # try:
            self.game_state = globals()[self.game_state.update()](self.game_state.__class__.__name__)
            # except:
            #     print(self.game_state)
            #     self.game_running = False
    
    def update_3(self):#similar approach to update_1 but with a check instead of purposeful crash maybe? need to remove prev_state to initialisation I think
        while self.game_running:
            self.next_state = self.game_state.update()
            if type(globals()[self.next_state]) == __class__:#(self.game_state.__class__.__name__)) == __class__:
                self.game_state = self.next_state
            else:
                print(self.next_state)
                self.game_running = False
    
    def update_2(self):#I can do differernt types of return from update not just bool
        while self.game_running:
            if self.game_state.update():
                self.game_state = globals()[self.game_state.next_state](self.game_state.__class__.__name__)
            else:
                print(self.game_state.next_state)
                self.game_running = False
                
    def update_4(self):#like update_2 with trying to be able to unfullscreen it, while loop should be in main.py to change display
        while self.game_running:
            output = self.game_state.update()
            if output == "change_state":
                self.game_state = globals()[self.game_state.next_state](self.game_state.__class__.__name__)
            elif output == "change_display":
                if display.get_height() == computer.current_h:
                    display = pygame.display.set_mode((computer.current_w, computer.current_h*0.93))
                else:
                    display = pygame.display.set_mode((computer.current_w, computer.current_h))
                return display
            else:
                print(self.game_state.next_state)
                self.game_running = False
                
def global_settings():#with this settings can be removed
    global screen, d_width, d_height, display, m_pos
    screen = pygame.display.Info()
    d_width = screen.current_w
    d_height = screen.current_h
    display = pygame.display.set_mode((d_width, d_height), 0)
    m_pos = pygame.math.Vector2(pygame.mouse.get_pos())