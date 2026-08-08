import pygame, sys, random, math
from settings import *
from main_menu import *
from control_menu import *
from quit_menu import *
from death_screen import *
from game_over import *
from win_screen import *
from paused import *
from playing import *

class Player():
    def __init__(self):
        self.lives = 3
        self.score = 0
        self.kills = 0
        self.deaths = 0
                
class Game():
    def __init__(self):

        self.player = Player()

        #clock for fps
        self.clock = pygame.time.Clock()

        self.main_menu = Main_Menu()
        self.control_menu = Control_Menu()
        self.quit_menu = Quit_Menu()
        self.death_screen = Death_Screen()
        self.game_over = Game_Over()
        self.win_screen = Win_Screen()
        self.paused = Paused()
        self.playing = Playing()

        self.game_state = "main_menu"
        self.prev_state = ""

        self.max_fps = 30
        self.current_fps = 0
        
        self.game_running = True
        
    def update(self):
        while self.game_running:
            self.clock.tick(self.max_fps)
            self.current_fps = self.clock.get_fps()
            
            if self.game_state == "main_menu":
                self.main_menu.update()
                self.main_menu.render()
                self.game_state = self.main_menu.game_state
                
            elif self.game_state == "control_menu":
                self.control_menu.update()
                self.control_menu.render()
                self.game_state = self.control_menu.game_state
                
            elif self.game_state == "quit_menu":
                self.quit_menu.update(self.prev_state)
                self.quit_menu.render()
                self.game_state = self.quit_menu.game_state
                
            elif self.game_state == "playing":
                self.playing.update()
                self.playing.render(self.player, self.current_fps, self.max_fps)#for now player
                self.game_state = self.playing.game_state
            
            elif self.game_state == "paused":
                self.paused.update()
                self.paused.render(self.player)
                self.game_state = self.paused.game_state
                
            elif self.game_state == "death_screen":
                self.death_screen.update()
                self.death_screen.render(self.player)
                self.game_state = self.death_screen.game_state
            
            elif self.game_state == "game_over":
                self.game_over.update()
                self.game_over.render(self.player)
                game_state = self.game_over.game_state
            
            elif self.game_state == "win_screen":
                self.win_screen.update()
                self.win_screen.render(self.player)
                game_state = self.win_screen.game_state
            
            
            
            else:
                print(self.game_state)
                self.game_running = False
            
        
            pygame.display.update()
            
        pygame.quit()
        sys.exit()
        
game = Game()
game.update()