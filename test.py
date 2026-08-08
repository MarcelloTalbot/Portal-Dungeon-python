import pygame, sys, random, math
from settings import *
from main_menu import *

#clock for fps
clock = pygame.time.Clock()

main_menu = Main_Menu()

game_state = "main_menu"

max_fps = 30

game_running = True
while game_running:
    display.fill(grey)
    
    clock.tick(max_fps)
    
    if game_state == "main_menu":
        main_menu.update()
        game_state = main_menu.game_state
        
    else:
        game_running = False
        
    pygame.display.update()
        
pygame.quit()
sys.exit()