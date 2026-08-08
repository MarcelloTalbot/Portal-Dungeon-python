from button import *
from textbox import *
from settings import *
from camera import *
from entity import *

#common functions that can occur in the __init__ funcs can go here? and others I think?
# def

class Game_State():
    def __init__(self, prev_state):
        self.show = True
        
        #mouse inputs
        self.m_pos = pygame.math.Vector2((0, 0))
        self.click = False
        # self.sprites = pygame.sprite.Group()
        # self.bob = Menu_player(d_width/10 ,d_height/10, display, plrhd, plrrm)
        # self.sprites.add(self.bob)
        # self.txt = textbox(d_width/2, d_height/2, 150, white, display)
        # self.classes = [self.txt]
        
        # self.classes_2 = [self.bob, self.txt]
        
        self.prev_state = prev_state
        
    def update(self):
        # self.game_state = self.own_state
        
        # self.input_detection()
        pass
        
    def input_detection(self):
        pass

    def render(self):
        pass
    
    #I think this will remove all data (from RAM?) of every class instance in the game state?
    
    def die_delete(self):
        for c in range(0, len(self.classes_2)):
            delattr(self, self.classes_2[c].name)
            
        self.classes.clear()
        self.sprites.empty()
    
    #I don't know which is better or if they're needed
    def die_replace(self):
        for c in range (0, len(self.classes)):
            setattr(self, self.classes[c].name, None)
            
        for sprite in self.sprites:
            setattr(self, sprite.name, None)
            
        self.classes.clear()
        self.sprites.empty()

#Main menu screen
class Main_Menu(Game_State):
    def __init__(self, prev_state):
        super().__init__(prev_state)
        #button creation
        self.play_btn = Play_Button()
        self.ctrl_btn = Control_Button()
        self.quit_btn = Quit_Button()
        self.buttons = [self.play_btn, self.ctrl_btn, self.quit_btn]
        
        #image boxes
        self.title_rect = title_img.get_rect(center = (round(d_width/2), round(d_height/4)))
        self.menu_portal_rect = pygame.Rect((round(d_width/2) + 212), (round(d_height/4) + 30), 32, 56)
        
        #menu sprite
        self.m_player = Menu_player(d_width/10 ,d_height/10, display, plrhd, plrrm)
        
        #fps
        self.clock = pygame.time.Clock()
        self.max_fps = 30
        self.current_fps = 0
        
        # self.prev_state = prev_state
        
        # m_group = pygame.sprite.Group()#why does it not die??
        # m_group.add(self.m_player)
        
        # self.game_state = "main_menu"
        
        #input variables
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        self.sprint = False
        self.moves = [self.move_up, self.move_down, self.move_left, self.move_right, self.sprint]
        
        # self.own_state = 'Main_Menu'
                
    # def update(self):
    #     # self.game_state = "main_menu"
        
    #     self.input_detection()
        
    #     for b in self.buttons:
    #         if b.update(self.m_pos, self.click, self.m_player):
    #             self.game_state = b.next_state
    #             break

    #     self.m_player.update(self.moves, self.m_pos, self.menu_portal_rect, self.play_btn.group, self.quit_btn.group, self.ctrl_btn.group)

    #     if self.m_player.hitbox.colliderect(self.menu_portal_rect):
    #         #m_player.kill()
    #         self.game_state = "playing"
            
    #         self.moves = [False, False, False, False, False]# won't need if re-initialise on change state
    #         self.m_player.pos = pygame.math.Vector2((d_width/10, d_height/10))#this can be changed with .kill when init for game states is done in loop or just removed?
    #         self.m_player.energyval = self.m_player.energymax# won't need if re-initialise on change state
            
    def update(self):#does this need clock
        while self.show:
            self.clock.tick(self.max_fps)
            
            self.input_detection()
            # if self.input_detection():
            #     return self.next_state
            
            for b in self.buttons:
                # try:
                #     return b.update(self.m_pos, self.click, self.m_player)
                # except:
                #     pass
                
                if b.update(self.m_pos, self.click, self.m_player):
                    self.next_state = b.next_state
            
            self.m_player.update(self.moves, self.m_pos, self.menu_portal_rect, self.play_btn.group, self.quit_btn.group, self.ctrl_btn.group)
            
            if self.m_player.hitbox.colliderect(self.menu_portal_rect):
                self.next_state = 'Playing'
            
            if hasattr(self, 'next_state'):
                return self.next_state
            
            self.render()
            
            pygame.display.update()

    def input_detection(self):
        self.click = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                self.next_state = "Goodbye"
            
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
                    # self.game_state = "quit_menu"
                    # return Quit_Menu()#this one hopefully
                    # return True
                    self.next_state = 'Quit_Menu'#Quit_Menu(Main_Menu())
                elif event.key == pygame.K_b:
                    self.next_state = 'Win_Screen'
                
                elif event.key == pygame.K_F11:
                    self.change_display = True
                    # height = display.get_height()
                    # if height == computer.current_h:
                    #     display = pygame.display.set_mode((computer.current_w, computer.current_h*0.93))
                    # else:
                    #     display = pygame.display.set_mode((computer.current_w, computer.current_h))
                    # return display

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
        # self.m_pos = pygame.math.Vector2(pygame.mouse.get_pos())
        self.m_pos.x, self.m_pos.y = pygame.mouse.get_pos()
    
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

#Screen to shows the controls of the game
class Control_Menu(Game_State):
    def __init__(self, prev_state):
        super().__init__(prev_state)
        #button creation
        self.back_btn = Back_Button(prev_state, d_width/2, d_height*0.92, back_u, back_d)
        self.buttons = [self.back_btn]
        
        #image boxes
        self.ctrls_rect = ctrls_img.get_rect(topleft = (0, 0))
        
        # self.own_state = 'Control_Menu'
        
        # self.game_state = "control_menu"
        
    def update(self):
        while self.show:
            # self.game_state = "control_menu"
            
            self.input_detection()
            
            # for b in self.buttons:
            #     if b.update(self.m_pos, self.click):
            #         self.game_state = b.next_state
            #         break
            
            for b in self.buttons:
                if b.update(self.m_pos, self.click):
                        return b.next_state
            
            self.render()
            
            if hasattr(self, 'next_state'):
                return self.next_state
            
            pygame.display.update()
        
    def input_detection(self):
        self.click = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                self.next_state = "Fair well"
            
            #key presses
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_state = Main_Menu()
                    
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

#Screen to check if player actually wants to quit the game
class Quit_Menu(Game_State):
    def __init__(self, prev_state):
        super().__init__(prev_state)
        #button creation
        self.yes_btn = Yes_Button("Quitting in 3...2...1...")
        self.no_btn = No_Button(prev_state)#Main_Menu())
        self.buttons = [self.yes_btn, self.no_btn]
        
        #textbox creation
        self.top_large_txt = textbox(d_width/2, 100, 150, white, display)
        
        # self.game_state = "quit_menu"
        # self.prev_state = prev_state
    
    def update(self):
        while self.show:
            # self.game_state = "quit_menu"
            
            self.input_detection()
            
            # for b in self.buttons:
            #     if b.update(self.m_pos, self.click):
            #         self.game_state = b.next_state
            #         break
            for b in self.buttons:
                if b.update(self.m_pos, self.click):
                        return b.next_state
            
            self.render()
            
            if hasattr(self, 'next_state'):
                return self.next_state
            
            pygame.display.update()
    
    def input_detection(self):
        self.click = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                self.next_state = "See you later?"
            
            #key presses
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_state = self.prev_state
                    
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

#When player looses all health but has more lives and shows the players statistics the moment they died
class Death_Screen(Game_State):
    def __init__(self, prev_state):
        super().__init__(prev_state)
        #button creation
        self.rspn_btn = Respawn_Button(prev_state)
        self.main_btn = Main_Button()
        self.quit_btn = Quit_Button_2()
        self.buttons = [self.rspn_btn, self.main_btn, self.quit_btn]
        
        #textbox creation
        self.top_large_txt = textbox(d_width/2, 100, 150, white, display)
        self.lives_txt = textbox(d_width/2 - 450, 300, 50, white, display)
        
        #self.game_state = "death_screen"
        
    def update(self):
        while self.show:
            # self.game_state = "death_screen"
            
            self.input_detection()
            
            # for b in self.buttons:
            #     if b.update(self.m_pos, self.click):
            #         self.game_state = b.next_state
            #         break
            
            for b in self.buttons:
                if b.update(self.m_pos, self.click):
                        return b.next_state
            
            self.render()
            
            if hasattr(self, 'next_state'):
                return self.next_state
            
            pygame.display.update()
    
    def input_detection(self):
        self.click = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                self.game_state = "D:"
            
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
        
    def render(self):#, player):
        display.fill(grey)
        
        #text
        self.top_large_txt.draw_c("You Died")
        
        # if player.lives == 1:
        #     self.lives_txt.draw_l(str(player.lives)+" life remaining")
        # else:
        #     self.lives_txt.draw_l(str(player.lives)+" lives remaining")
            
        #buttons
        self.rspn_btn.render()
        self.main_btn.render()
        self.quit_btn.render()

#When player looses all their lives and shows the players statistics the moment they died
class Game_Over(Game_State):
    def __init__(self, prev_state):
        super().__init__(prev_state)
        #button creation
        self.rtry_btn = Retry_Button(prev_state)
        self.main_btn = Main_Button()
        self.quit_btn = Quit_Button_2()
        self.buttons = [self.rtry_btn, self.main_btn, self.quit_btn]
        
        #textbox creation
        self.top_large_txt = textbox(d_width/2, 100, 150, white, display)
        self.score_txt = textbox(d_width/2 - 450, 200, 50, white, display)
        self.kills_txt = textbox(d_width/2 - 450, 250, 50, white, display)
        
        # self.game_state = "game_over"
        
    def update(self):
        while self.show:
            # self.game_state = "game_over"
            
            self.input_detection()
            
            # for b in self.buttons:
            #     if b.update(self.m_pos, self.click):
            #         self.game_state = b.next_state
            #         break
            
            for b in self.buttons:
                    if b.update(self.m_pos, self.click):
                            return b.next_state
            
            self.render()
            
            if hasattr(self, 'next_state'):
                return self.next_state
            
            pygame.display.update()
        
    def input_detection(self):
        self.click = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                self.game_state = "):"
            
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
        
    def render(self):#, player):
        display.fill(grey)
        
        #text
        self.top_large_txt.draw_c("Game Over")
        # self.score_txt.draw_l("Score: " + str(player.score))
        # self.kills_txt.draw_l("Kills: " + str(player.kills))
        
        #buttons
        self.rtry_btn.render()
        self.main_btn.render()
        self.quit_btn.render()

#Shows when player reaches the end of the game
class Win_Screen(Game_State):
    def __init__(self, prev_state):
        super().__init__(prev_state)
        #button creation
        self.rtry_btn = Retry_Button(prev_state)
        self.main_btn = Main_Button()
        self.quit_btn = Quit_Button_2()
        self.buttons = [self.rtry_btn, self.main_btn, self.quit_btn]
        
        #textbox creation
        self.top_large_txt = textbox(d_width/2, 100, 150, white, display)
        self.score_txt = textbox(d_width/2 - 450, 200, 50, white, display)
        self.kills_txt = textbox(d_width/2 - 450, 250, 50, white, display)
        self.deaths_txt = textbox(d_width/2 - 450, 300, 50, white, display)
        
        # self.game_state = "win_screen"
        
    def update(self):
        while self.show:
            # self.game_state = "win_screen"
            
            self.input_detection()
            
            # for b in self.buttons:
            #     if b.update(self.m_pos, self.click):
            #         self.game_state = b.next_state
            #         break
            
            for b in self.buttons:
                    if b.update(self.m_pos, self.click):
                            return b.next_state
            
            self.render()
            
            if hasattr(self, 'next_state'):
                return self.next_state
            
            pygame.display.update()
    
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
    
    def render(self):#, player):
        display.fill(grey)
        
        #text
        self.top_large_txt.draw_c("You Win!\nok")
        # self.score_txt.draw_l("Score: " + str(player.score))
        # self.kills_txt.draw_l("Kills: " + str(player.kills))
        # self.deaths_txt.draw_l("Deaths: " + str(player.deaths))
        
        #buttons
        self.rtry_btn.render()
        self.main_btn.render()
        self.quit_btn.render()

#Shows when the game is paused
class Paused(Game_State):
    def __init__(self, prev_state):
        super().__init__(prev_state)
        #button creation
        self.cont_btn = Continue_Button(prev_state)
        self.main_btn = Main_Button()
        self.quit_btn = Quit_Button_2()
        self.buttons = [self.cont_btn, self.main_btn, self.quit_btn]
        
        #textbox creation
        self.top_large_txt = textbox(d_width/2, 100, 150, white, display)
        self.score_txt = textbox(d_width/2 - 450, 200, 50, white, display)
        self.kills_txt = textbox(d_width/2 - 450, 250, 50, white, display)
        self.lives_txt = textbox(d_width/2 - 450, 300, 50, white, display)
        
        #image boxes
        #self.overlay = white_ovly.get_rect(topleft = (0,0))
        
        # self.game_state = "paused"
    
    def update(self):
        while self.show:
            # self.game_state = "paused"
        
            self.input_detection()
            
            for b in self.buttons:
                if b.update(self.m_pos, self.click):
                    return b.next_state
                
            self.render()
                
            if hasattr(self, 'next_state'):
                return self.next_state
                
            pygame.display.update()
    
    def input_detection(self):
        self.click = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                self.next_state = "Until you come back...I'll be waiting here...for as long as it takes...I'll be waiting...even forever"
            
            #key presses
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    self.next_state = 'Playing'#Playing()
                    
            #mouse presses
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True
                    
        #mouse position
        self.m_pos = pygame.math.Vector2(pygame.mouse.get_pos())

    def render(self):#, player):
        #overlay
        #display.blit(white_ovly,self.overlay)
        display.fill(grey)
        
        #text
        self.top_large_txt.draw_c("Paused")
        # self.score_txt.draw_l("Score: " + str(player.score))
        # self.kills_txt.draw_l("Kills: " + str(player.kills))
        # self.lives_txt.draw_l("Lives: " + str(player.lives))
        
        #buttons
        self.cont_btn.render()
        self.main_btn.render()
        self.quit_btn.render()

#Shows the main game
class Playing(Game_State):
    def __init__(self, prev_state):
        super().__init__(prev_state)
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
        
        # self.game_state = "playing"
        
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
        
        self.show_stats = False
        
        self.clock = pygame.time.Clock()
        self.max_fps = 30
        self.current_fps = 0
    
    def update(self):
        while self.show:
            self.clock.tick(self.max_fps)
            self.current_fps = self.clock.get_fps()
            
            self.input_detection()
            
            # for b in self.buttons:
            #     if b.update(self.m_pos, self.click):
            #         self.moves = [False, False, False, False, False, False, False, False]
            #         self.game_state = b.next_state
            #         break
            
            for b in self.buttons:
                if b.update(self.m_pos, self.click):
                    return b.next_state
                
            if hasattr(self, 'next_state'):
                return self.next_state
            
            self.render()
                
            pygame.display.update()
    
    def input_detection(self):
        self.click = False
        self.moves[6] = False
        self.moves[7] = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                self.next_state = "Why are you leaving when you're still playing? Are you sure it's saved?"
                
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
                    self.next_state = 'Paused'#Paused()
            
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
      
    def render(self):#for now player
        display.fill(grey)
        
        if self.show_stats:
            self.fps_txt.draw_l("FPS:" + str(round(self.current_fps)) + " | Max:" + str(self.max_fps))
        # self.score_txt.draw_l("Score: " + str(player.score))

# class Quitting():
#     def __init__(self):
#         pass