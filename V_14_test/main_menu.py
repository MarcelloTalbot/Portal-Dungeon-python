from settings import *
import pygame, random, math
from pygame.locals import *
from entity import *
from button import *

class Main_Menu():
    def __init__(self):
        #button creation
        self.play_btn = Main_Menu_Button(d_width/2, d_height/2, play_u, play_d, "playing")
        self.ctrl_btn = Main_Menu_Button(d_width/2, d_height/1.45, ctrl_u, ctrl_d, "control_menu")
        self.quit_btn = Main_Menu_Button(d_width/2, d_height/1.13, quit_u, quit_d, "quit_menu")
        self.buttons = [self.play_btn, self.ctrl_btn, self.quit_btn]
        
        #image boxes
        self.title_rect = title_img.get_rect(center = (round(d_width/2), round(d_height/4)))
        self.menu_portal_rect = pygame.Rect((round(d_width/2) + 212), (round(d_height/4) + 30), 32, 56)
        
        #menu sprite
        self.m_player = Menu_player(d_width/10 ,d_height/10, display, plrhd, plrrm)
        m_group = pygame.sprite.Group()#why does it not die??
        m_group.add(self.m_player)
        
        self.game_state = "main_menu"
        
        #input variables
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        self.sprint = False
        self.moves = [self.move_up, self.move_down, self.move_left, self.move_right, self.sprint]
        self.m_pos = pygame.math.Vector2((0, 0))
        self.click = False
                
    def update(self):
        self.game_state = "main_menu"
        
        self.input_detection()
        
        for b in self.buttons:
            if b.update(self.m_pos, self.click, self.m_player):
                self.moves = [False, False, False, False, False]# won't need if re-initialise on change state
                self.m_player.energyval = self.m_player.energymax# won't need if re-initialise on change state
                self.game_state = b.next_state
                break
        
        # if True in self.buttons.update(self.m_pos, self.click, self.m_player):
        #     self.moves = [False, False, False, False, False]
        #     self.game_state = 
        
        # #play button
        # if self.play_btn.update(self.m_pos,self.click,self.m_player):
        #     self.game_state = "playing"
        #     self.up_pressed = False
        #     self.down_pressed = False
        #     self.left_pressed = False
        #     self.right_pressed = False
        #     self.sprint_pressed = False

        # #controls button
        # if self.ctrl_btn.update(self.m_pos,self.click,self.m_player):
        #     self.game_state = "control_menu"
        #     self.up_pressed = False
        #     self.down_pressed = False
        #     self.left_pressed = False
        #     self.right_pressed = False
        #     self.sprint_pressed = False

        # #quit button
        # if self.quit_btn.update(self.m_pos,self.click,self.m_player):
        #     self.game_state = "quit_menu"
        #     self.up_pressed = False
        #     self.down_pressed = False
        #     self.left_pressed = False
        #     self.right_pressed = False
        #     self.sprint_pressed = False

        self.m_player.update(self.moves, self.m_pos, self.menu_portal_rect, self.play_btn.group, self.quit_btn.group, self.ctrl_btn.group)

        if self.m_player.hitbox.colliderect(self.menu_portal_rect):
            #m_player.kill()
            self.game_state = "playing"
            
            self.moves = [False, False, False, False, False]# won't need if re-initialise on change state
            self.m_player.pos = pygame.math.Vector2((d_width/10, d_height/10))#this can be changed with .kill when init for game states is done in loop or just removed?
            self.m_player.energyval = self.m_player.energymax# won't need if re-initialise on change state
    
    def input_detection(self):
        self.click = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                self.game_state = "Goodbye"
            
            #key presses
            elif event.type == pygame.KEYDOWN:
                #movement
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.moves[0] = True
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.moves[1] = True
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.moves[2] = True
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.moves[3] = True
                    
                #actions
                elif event.key == pygame.K_LSHIFT:
                    self.moves[4] = True
                    
                #leaving
                elif event.key == pygame.K_ESCAPE:
                    self.game_state = "quit_menu"
                # elif event.key == pygame.K_b:
                #     self.game_state = "paused"
                    
            elif event.type == pygame.KEYUP:
                #movement
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.moves[0] = False
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.moves[1] = False
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.moves[2] = False
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.moves[3] = False
                    
                #actions
                elif event.key == pygame.K_LSHIFT:
                    self.moves[4] = False
                    
            #mouse presses
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True
                    
        #mouse position
        self.m_pos = pygame.math.Vector2(pygame.mouse.get_pos())
        
        #all key presses
        # self.moves = [self.move_up, self.move_down, self.move_left, self.move_right, self.sprint]
    
    def render(self):
        display.fill(grey)
        
        #images
        display.blit(title_img, self.title_rect)
        
        #sprint bar
        self.m_player.render_bar(self.play_btn.rect, self.play_btn.image)
        
        #button rendering
        self.play_btn.render()
        self.ctrl_btn.render()
        self.quit_btn.render()
        
        #sprites
        self.m_player.render()
        
        