from button import *
from textbox import *
from settings import *

class Win_Screen():
    def __init__(self):
        #button creation
        self.rtry_btn = Button(d_width/2, d_height/2, rtry_u, rtry_d, "playing")
        self.main_btn = Button(d_width/2, d_height/1.45, main_u, main_d, "main_menu")
        self.quit_btn = Button(d_width/2, d_height/1.13, quit_u, quit_d, "quit_menu")
        self.buttons = [self.rtry_btn, self.main_btn, self.quit_btn]
        
        #textbox creation
        self.top_large_txt = textbox(d_width/2, 100, 150, white, display)
        self.score_txt = textbox(d_width/2 - 450, 200, 50, white, display)
        self.kills_txt = textbox(d_width/2 - 450, 250, 50, white, display)
        self.deaths_txt = textbox(d_width/2 - 450, 300, 50, white, display)
        
        self.game_state = "win_screen"
        
        #input variables
        self.m_pos = pygame.math.Vector2((0, 0))
        self.click = False
        
    def update(self):
        self.game_state = "win_screen"
        
        self.input_detection()
        
        for b in self.buttons:
            if b.update(self.m_pos, self.click):
                self.game_state = b.next_state
                break
        
        # #retry button
        # if self.rtry_btn.update(self.m_pos, self.click):
        #     self.game_state = "playing"
            
        # #main button
        # if self.main_btn.update(self.m_pos, self.click):
        #     self.game_state = "main_menu"
            
        # #quit button
        # if self.quit_btn.update(self.m_pos, self.click):
        #     self.game_state = "quit_menu"
    
    def input_detection(self):
        self.click = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                self.game_state = ":("
            
            #key presses
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = "quit_menu"
                    
            #mouse presses
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True
                    
        #mouse position
        self.m_pos = pygame.math.Vector2(pygame.mouse.get_pos())
    
    def render(self, player):
        display.fill(grey)
        
        #text
        self.top_large_txt.draw_c("You Win!")
        self.score_txt.draw_l("Score: " + str(player.score))
        self.kills_txt.draw_l("Kills: " + str(player.kills))
        self.deaths_txt.draw_l("Deaths: " + str(player.deaths))
        
        #buttons
        self.rtry_btn.render()
        self.main_btn.render()
        self.quit_btn.render()