from button import *
from settings import *

class Control_Menu():
    def __init__(self):
        #button creation
        self.back_btn = Button(d_width/2, d_height*0.92, back_u, back_d, "main_menu")
        self.buttons = [self.back_btn]
        
        #image boxes
        self.ctrls_rect = ctrls_img.get_rect(topleft = (0, 0))
        
        self.game_state = "control_menu"
        
        #input variables
        self.m_pos = pygame.math.Vector2((0, 0))
        self.click = False
        
    def update(self):
        self.game_state = "control_menu"
        
        self.input_detection()
        
        for b in self.buttons:
            if b.update(self.m_pos, self.click):
                self.game_state = b.next_state
                break
        
        # #back button
        # if self.back_btn.update(self.m_pos, self.click):
        #     self.game_state = "main_menu"
        
    def input_detection(self):
        self.click = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                self.game_state = "Fair well"
            
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
        
        #images
        display.blit(ctrls_img, self.ctrls_rect)
        
        #buttons
        self.back_btn.render()