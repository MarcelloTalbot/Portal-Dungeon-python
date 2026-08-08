import sys, pygame

pygame.init()

from game import *

game = Game()

game.update()

pygame.quit()
sys.exit()