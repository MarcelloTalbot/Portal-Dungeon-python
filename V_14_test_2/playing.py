from button import *
from textbox import *
from settings import *
from camera import *

class Playing():
    def __init__(self):
        #button creation
        self.buttons = []
        
        #textbox creation
        self.score_txt = textbox(5, 5, 20, white, display)
        self.cash_txt = textbox(d_width - 260, (d_height * 0.92)-2, 20, yellow, display)
        self.ammo_txt = textbox(d_width - 260, (d_height * 0.96)-2, 20, yellow, display)
        self.fps_txt = textbox(5,d_height - 20, 20, red, display)
        
        #image boxes
        self.cash_rect = cn.get_rect(topleft = (round(d_width - 290), round((d_height * 0.92)-2)))
        self.ammo_rect = amo.get_rect(topleft = (round(d_width - 297), round((d_height * 0.96)-5)))
        
        #camera for following player
        self.render_dist = (((d_width/2)**2 + (d_height/2)**2)**0.5) + 48
        self.sim_dist = 800
        self.camera = Camera(self.render_dist, self.sim_dist)
        
        self.game_state = "playing"
        
        #input variables
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        self.sprint = False
        self.attack = False
        self.swap_weapon = False
        self.interact = False
        self.moves = [self.move_up, self.move_down, self.move_left, self.move_right, self.sprint, self.attack, self.swap_weapon, self.interact]
        self.m_pos = pygame.math.Vector2((0, 0))
        self.click = False
        
        self.show_stats = False
    
    def update(self):
        self.game_state = "playing"
        
        self.input_detection()
        
        for b in self.buttons:
            if b.update(self.m_pos, self.click):
                self.moves = [False, False, False, False, False, False, False, False]
                self.game_state = b.next_state
                break
    
    def input_detection(self):
        self.click = False
        self.moves[6] = False
        self.moves[7] = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                self.game_state = "Why are you leaving when you're still playing? Are you sure it's saved?"
                
            #key presses
            elif event.type == pygame.KEYDOWN:
                #movement
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.moves[0] = True
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.moves[1] = True
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.moves[2]= True
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.moves[3] = True
                    
                #actions
                elif event.key == pygame.K_LSHIFT:
                    self.moves[4] = True
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.moves[5] = True
                
                #weapon selection
                # elif event.key == pygame.K_1:
                #     player.weapon = 0
                # elif event.key == pygame.K_2:
                #     player.weapon = 1
                    
                #game statistics (like Minecraft's F3 but worse)
                elif event.key == pygame.K_l:
                    self.show_stats = not self.show_stats
                    
                #pausing
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    self.game_state = "paused"
            
            elif event.type == pygame.KEYUP:
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
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.moves[5] = True
                elif event.key == pygame.K_q:
                    self.moves[6] = True
            
            #mouse presses
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.moves[5] = True
                elif event.button == 3:
                    self.moves[7] = True
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.moves[5] = False
                    
            elif event.type == pygame.MOUSEWHEEL:
                self.moves[6] = True 
                    
        #mouse position
        self.m_pos = pygame.math.Vector2(pygame.mouse.get_pos())
        
        #all key presses
        # self.moves = [self.move_up, self.move_down, self.move_left, self.move_right, self.sprint, self.attack, self.swap_weapon, self.interact]
    
    def render(self, player, current_fps, max_fps):#for now player
        display.fill(grey)
        
        if self.show_stats:
            self.fps_txt.draw_l("FPS:" + str(round(current_fps)) + " | Max:" + str(max_fps))
        # self.score_txt.draw_l("Score: " + str(player.score))