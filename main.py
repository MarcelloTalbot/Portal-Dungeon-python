import sys, pygame
# from sys import exit
# from pygame import init, quit
# pygame.init()
pygame.init()
from game import *

game = Game()

game.update_1_2()
# print(repr((1,2,3)))
# my_list = pygame.sprite.Group()
# my_list.add(Player(200,200))
# my_list.clear()
# if my_list:
#     print(True)
pygame.quit()
sys.exit()