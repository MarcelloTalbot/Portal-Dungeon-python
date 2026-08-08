from button import *
from textbox import *
from settings import *

class Quit_Menu():
    def __init__(self):
        #button creation
        self.yes_btn = Button(d_width*0.4, d_height/1.45, yes_u, yes_d, "Quitting in 3...2...1...")
        self.no_btn = Button(d_width*0.6, d_height/1.45, no_u, no_d, "main_menu")#change state
        self.buttons = [self.yes_btn, self.no_btn]
        
        #textbox creation
        self.top_large_txt = textbox(d_width/2, 100, 150, white, display)
        
        self.game_state = "quit_menu"
        
        #input variables
        self.m_pos = pygame.math.Vector2((0, 0))
        self.click = False
        
    def update(self,prev_state):
        self.game_state = "quit_menu"
        
        self.input_detection()
        
        for b in self.buttons:
            if b.update(self.m_pos, self.click):
                self.game_state = b.next_state
                break
        
        # #yes button
        # if self.yes_btn.update(self.m_pos, self.click):
        #     self.game_state = "Quitting in 3...2...1..."
        
        # #no button
        # if self.no_btn.update(self.m_pos, self.click):
        #     self.game_state = prev_state
        
    def input_detection(self):
        self.click = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                self.game_state = "See you later?"
            
            #key presses
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = "main_menu"
                    
            #mouse presses
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True
                    
        #mouse position
        self.m_pos = pygame.math.Vector2(pygame.mouse.get_pos())
                    
    def render(self):
        display.fill(grey)
        
        #text
        self.top_large_txt.draw_c("Are you sure?")
        
        #buttons
        self.yes_btn.render()
        self.no_btn.render()