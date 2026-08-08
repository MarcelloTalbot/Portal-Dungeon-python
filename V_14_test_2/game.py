import pygame
from pygame.locals import *#dont know if needed now
from settings import *
from game_states_file import *

# class Player():
#     def __init__(self):
#         self.lives = 3
#         self.score = 0
#         self.kills = 0
#         self.deaths = 0
                
class Game():#might be able to be just one function with __init__ as section just above update (may be better for globalling display)
    def __init__(self):

        # self.player = Player()

        #clock for fps
        # global clock
        # clock = pygame.time.Clock()
        
        self.clock = pygame.time.Clock()#maybe only clock in Playing?

        self.game_state = Main_Menu(None)#globals()['Main_Menu']()
        # self.prev_state = ""

        # self.max_fps = 30
        # self.current_fps = 0
        
        self.game_running = True
        
    def update(self):
        while self.game_running:
            # try:
            # if hasattr(game_state, "update"):
            self.game_state = self.game_state.update()
            # except:
            # else:
                # print(self.game_state)
                # self.game_running = False
                
    def update_2(self):
        while self.game_running:
            self.game_state.update()
            if self.game_state.next_state == "main_menu":
                self.game_state = Main_Menu()
            elif self.game_state.next_state == "control_menu":
                self.game_state = Control_Menu()
            elif self.game_state.next_state == "quit_menu":
                self.game_state = Quit_Menu()
            elif self.game_state.next_state == "death_screen":
                self.game_state = Death_Screen()
            elif self.game_state.next_state == "win_screen":
                self.game_state = Win_Screen()
            elif self.game_state.next_state == "game_over":
                self.game_state = Game_Over()
            elif self.game_state.next_state == "playing":
                self.game_state = Playing()
            elif self.game_state.next_state == "paused":
                self.game_state = Paused()
            else:
                print(self.game_state)
                self.game_running = False
                
    def update_3(self):#if game crashes then I won't know what happened
        while self.game_running:
            # try:
            self.game_state = globals()[self.game_state.update()](self.game_state.__class__.__name__)#self.game_state.own_state)
            # except:
            #     print(self.game_state)
            #     self.game_running = False
                
    def update_4(self):#I can do differernt types of return from update not just bool
        while self.game_running:
            if self.game_state.update():
                    self.game_state = globals()[self.game_state.next_state](self.game_state.__class__.__name__)
            else:
                print(self.game_state.next_state)
                self.game_running = False