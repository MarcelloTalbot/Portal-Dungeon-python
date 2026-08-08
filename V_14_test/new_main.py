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

player = Player()

#clock for fps
clock = pygame.time.Clock()

main_menu = Main_Menu()
control_menu = Control_Menu()
quit_menu = Quit_Menu()
death_screen = Death_Screen()
game_over = Game_Over()
win_screen = Win_Screen()
paused = Paused()
playing = Playing()

game_state = "main_menu"
prev_state = ""

max_fps = 30
current_fps = 0

game_running = True
while game_running:
    clock.tick(max_fps)
    current_fps = clock.get_fps()
    
    # if game_state == "main_menu":
    #     if prev_state == game_state:
    #         main_menu.update()
    #         game_state = main_menu.game_state
    #     else:
    #         main_menu = Main_Menu()
    #         prev_state = game_state
    
    #above is better but can be improved by having game_state and prev_state in the settings or imported into each file somehow
    
    if game_state == "main_menu":
        main_menu.update()
        main_menu.render()
        game_state = main_menu.game_state
        
    elif game_state == "control_menu":
        control_menu.update()
        control_menu.render()
        game_state = control_menu.game_state
        
    elif game_state == "quit_menu":
        quit_menu.update(prev_state)
        quit_menu.render()
        game_state = quit_menu.game_state
        
    elif game_state == "playing":
        playing.update()
        playing.render(player, current_fps, max_fps)#for now player
        game_state = playing.game_state
    
    elif game_state == "paused":
        paused.update()
        paused.render(player)
        game_state = paused.game_state
        
    elif game_state == "death_screen":
        death_screen.update()
        death_screen.render(player)
        game_state = death_screen.game_state
    
    elif game_state == "game_over":
        game_over.update()
        game_over.render(player)
        game_state = game_over.game_state
    
    elif game_state == "win_screen":
        win_screen.update()
        win_screen.render(player)
        game_state = win_screen.game_state
    
    
    
    else:
        print(game_state)
        game_running = False
            
        
    pygame.display.update()
        
pygame.quit()
sys.exit()



#basic idea for the wanted ones:

#idk = "Player"
#player = f(idk)()

#Player is a class, so it's the same as:

#player = Player()

#wanted: with no while in game states - need to work out

# game_state = Main_Menu()

# game_playing = True
# while game_playing:
#     clock.tick(max_fps)
#     current_fps = clock.get_fps()
    
#     game_state.update()
#     game_state.render()
#     if game_state.change_state:
#         next_state = game_state.next_state
#         game_state.die()
#         try:
#             game_state = f(next_state)()#this thing
#         except:
#             print(next_state)
#             game_playing = False
        
#     pygame.display.update()
        
# pygame.quit()
# sys.exit()



#wanted: with while in game states - need to work out - this would be preferred out of all of them

# game_state = Main_Menu()

# game_playing = True
# while game_playing:
#     game_state.update()
#     next_state = game_state.next_state
#     game_state.die()
#     try:
#         game_state = f(next_state)()#this thing
#     except:
#         print(next_state)
#         game_playing = False
        
# pygame.quit()
# sys.exit()



#wanted: different approach to preferred (above)

# game_state = Main_Menu()

# game_playing = True
# while game_playing:
#     try:
#         game_state = game_state.update()
#     except:
#         print(game_state)
#         game_playing = False
        
# pygame.quit()
# sys.exit()



#better: with no while in game states

# game_state = Main_Menu()

# game_playing = True
# while game_playing:
#     clock.tick(max_fps)
#     current_fps = clock.get_fps()
    
#     game_state.update()
#     game_state.render()
#     if game_state.change_state:
#         next_state = game_state.next_state
#         game_state.die()
#         if next_state == "main_menu":
#             game_state = Main_Menu()
#         elif next_state == "control_menu":
#             game_state = Control_Menu()
#         elif next_state == "quit_menu":
#             game_state = Quit_Menu()
#         elif next_state == "playing":
#             game_state = Playing()
#         elif next_state == "paused":
#             game_state = Paused()
#         elif next_state == "death_screen":
#             game_state = Death_Screen()
#         elif next_state == "game_over":
#             game_state = Game_Over()
#         elif next_state == "win_screen":
#             game_state = Win_Screen()
#         else:
#             print(next_state)
#             game_playing = False
            
#     pygame.display.update()
            
# pygame.quit()
# sys.exit()



#better: with while in game states - preferred out of the better ones

# game_state = Main_Menu()

# game_playing = True
# while game_playing:
#     game_state.update()
#     next_state = game_state.next_state
#     game_state.die()
#     if next_state == "main_menu":
#         game_state = Main_Menu()
#     elif next_state == "control_menu":
#         game_state = Control_Menu()
#     elif next_state == "quit_menu":
#         game_state = Quit_Menu()
#     elif next_state == "playing":
#         game_state = Playing()
#     elif next_state == "paused":
#         game_state = Paused()
#     elif next_state == "death_screen":
#         game_state = Death_Screen()
#     elif next_state == "game_over":
#         game_state = Game_Over()
#     elif next_state == "win_screen":
#         game_state = Win_Screen()
#     else:
#         print(next_state)
#         game_playing = False
            
# pygame.quit()
# sys.exit()