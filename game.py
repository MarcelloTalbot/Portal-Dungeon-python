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
        
        # self.computer = pygame.display.Info()
        
        # #display resolution variables
        # self.d_width = computer.current_w#1200
        # self.d_height = computer.current_h#800
        
        # #sets the disply resolution
        # self.display = pygame.display.set_mode()#(d_width, d_height), FULLSCREEN)
        # # print(display.get_height())
        
        # set_global_vars()
        # my_list = [(4,3), (7,5), (1,8)]
        # sorted_list = sorted(my_list, key=lambda pos: pos[1])
        # print(sorted_list)
        
    def update_1(self):#if game actually crashes then I won't know exactly what happened only which state it was in
        while self.game_running:
            try:
                self.game_state = globals()[self.game_state.update()](self.game_state.__class__.__name__)
            except KeyError:
                print(self.game_state)
                self.game_running = False
    
    def update_1_1(self):#similar approach to update_1 but with a check instead of purposeful crash maybe? need to remove prev_state to initialisation I think
        while self.game_running:
            self.next_state = self.game_state.update()
            # print(type(globals()[self.next_state]))
            if type(globals()[self.next_state]) == type(type):#globals()[self.next_state]:#(self.game_state.__class__.__name__)) == __class__:
                self.game_state = globals()[self.next_state](self.game_state.__class__.__name__)
            else:
                print(self.next_state)
                self.game_running = False
                
    def update_1_2(self):#working version of update_1_1, I don't know why it never equalled __class__
        while self.game_running:
            self.next_state = self.game_state.update()
            # print(type(globals()[self.next_state]))
            try:
                self.game_state = globals()[self.next_state](self.game_state.__class__.__name__)
            except:
                print(self.next_state)
                self.game_running = False
    
    def update_2(self):#I can do differernt types of return from update not just bool
        while self.game_running:
            if self.game_state.update():
                self.game_state = globals()[self.game_state.next_state](self.game_state.__class__.__name__)
            else:
                print(self.game_state.next_state)
                self.game_running = False
                
    def update_2_2(self):#like update_2 with trying to be able to unfullscreen it, while loop should be in main.py to change display
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
                
    def update_3(self):#instead of initialising each game state every change I can just initialise all of them at the beginning and update in the update
        pass
                
def set_global_vars():#with this settings can be removed
    global screen, d_width, d_height, display, img_dir#, m_pos
    screen = pygame.display.Info()
    d_width = screen.current_w
    d_height = screen.current_h
    display = pygame.display.set_mode(flags=FULLSCREEN)
    img_dir = 'images/'
    # m_pos = pygame.math.Vector2(pygame.mouse.get_pos())