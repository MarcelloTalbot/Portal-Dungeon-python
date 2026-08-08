from settings import *
import pygame, random, math
from pygame.locals import *
from entity import *
from button import *

class Main_Menu():
    def __init__(self):
        #button creation
        self.play_btn = Button(d_width/2,d_height/2,play_u,play_d)
        self.ctrl_btn = Button(d_width/2,d_height/1.45,ctrl_u,ctrl_d)
        self.quit_btn = Button(d_width/2,d_height/1.13,quit_u,quit_d)
        
        #main menu images
        self.title_rect = title_img.get_rect(center = (round(d_width/2),round(d_height/4)))
        self.menu_portal_rect = pygame.Rect((round(d_width/2) + 212),(round(d_height/4) + 30),32,56)
        
        #menu sprite
        self.m_player = Menu_player(d_width/10,d_height/10,display,plrhd,plrrm)
        m_group = pygame.sprite.Group()#why does it not die??
        m_group.add(self.m_player)
        
        self.game_state = "main_menu"
        
        #input variables
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.sprint_pressed = False
        
        self.moves = [self.up_pressed, self.down_pressed, self.left_pressed, self.right_pressed, self.sprint_pressed]
        
        self.mx = 0
        self.my = 0
        
        self.click = False
                
    def update(self):
        self.input_detection()
        
        #play button
        if self.play_btn.update(self.mx,self.my,self.click,self.m_player):
            self.game_state = "playing"

        #controls button
        if self.ctrl_btn.update(self.mx,self.my,self.click,self.m_player):
            self.game_state = "ctrl_menu"

        #quit button
        if self.quit_btn.update(self.mx,self.my,self.click,self.m_player):
            self.game_state = "quit"

        self.m_player.update(self.moves,self.mx,self.my,self.menu_portal_rect,self.play_btn.group,self.quit_btn.group,self.ctrl_btn.group)

        if self.m_player.hitbox.colliderect(self.menu_portal_rect):
            #m_player.kill()
            self.game_state = "playing"
        
        self.render()
        
    
    def input_detection(self):
        self.click = False
        
        for event in pygame.event.get():
            #key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.up_pressed = True
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.down_pressed = True
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.left_pressed = True
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.right_pressed = True
                elif event.key == pygame.K_LSHIFT:
                    self.sprint_pressed = True
                elif event.key == pygame.K_ESCAPE:
                    self.game_state = "quit"
                    
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.up_pressed = False
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.down_pressed = False
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.left_pressed = False
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.right_pressed = False
                elif event.key == pygame.K_LSHIFT:
                    self.sprint_pressed = False
                    
            #mouse presses
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True
                    
        #mouse position
        # m_pos = pygame.mouse.get_pos()
        self.mx,self.my = pygame.mouse.get_pos()
        
        #all inputs
        self.moves = [self.up_pressed, self.down_pressed, self.left_pressed, self.right_pressed, self.sprint_pressed]
    
    def render(self):
        display.blit(title_img,self.title_rect)
        
        self.m_player.render_bar(self.play_btn.rect,self.play_btn.image)
        
        self.play_btn.render()
        self.ctrl_btn.render()
        self.quit_btn.render()
        
        self.m_player.render()
        
        