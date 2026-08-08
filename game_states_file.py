from button import *
from textbox import *
from settings import *
from camera import *
from entity import *
from tile import *
# import pickle

#common functions that can occur in the __init__ funcs can go here? and others I think?
# def

class Game_State():
    def __init__(self, prev_state):
        self.show = True
        
        #mouse inputs
        self.m_pos = pygame.math.Vector2((0, 0))
        self.click = False
        
        self.prev_state = prev_state
        
    def update(self):
        pass
        
    def input_detection(self):
        pass

    def render(self):
        pass
    
    def load_images(self):
        for name, directory in self.images.items():
            exec(f'global {name}\n{name} = pygame.image.load("{directory}").convert_alpha()')
    
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
        self.m_player = Menu_Player(d_width/10, d_height/10)
        # with open('save.pkl', 'w') as file:
        #     pickle.dump(self.m_player, file)
        #fps
        self.clock = pygame.time.Clock()
        self.max_fps = 30
        self.current_fps = 0
        
        #input variables
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        self.sprint = False
        self.moves = [self.move_up, self.move_down, self.move_left, self.move_right, self.sprint]
            
    def update(self):#does this need clock
        while self.show:
            self.clock.tick(self.max_fps)
            
            self.input_detection()
            
            for b in self.buttons:
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
                    self.next_state = 'Quit_Menu'

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
        
    def update(self):
        while self.show:
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
                self.next_state = "Fair well"
            
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
        self.no_btn = No_Button(prev_state)
        self.buttons = [self.yes_btn, self.no_btn]
        
        #textbox creation
        self.top_large_txt = textbox(d_width/2, 50, 150, white, display)
    
    def update(self):
        while self.show:
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
        self.rspn_btn = Respawn_Button()
        self.main_btn = Main_Button()
        self.quit_btn = Quit_Button_2()
        self.buttons = [self.rspn_btn, self.main_btn, self.quit_btn]
        
        #textbox creation
        self.top_large_txt = textbox(d_width/2, 50, 150, white, display)
        self.lives_txt = textbox(d_width/2 - 450, 250, 50, white, display)
        
        with open('stats.txt') as file:
            self.lines = file.readlines()
        
    def update(self):
        while self.show:
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
                self.next_state = "D:"
            
            #key presses
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_state = "Main_Menu"
                    
            #mouse presses
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True
                    
        #mouse position
        self.m_pos = pygame.math.Vector2(pygame.mouse.get_pos())
        
    def render(self):
        display.fill(grey)
        
        #text
        self.top_large_txt.draw_c("You Died")
        
        self.lives_txt.draw_l(self.lines[0])
            
        #buttons
        self.rspn_btn.render()
        self.main_btn.render()
        self.quit_btn.render()

#When player looses all their lives and shows the players statistics the moment they died
class Game_Over(Game_State):
    def __init__(self, prev_state):
        super().__init__(prev_state)
        #button creation
        self.rtry_btn = Retry_Button()
        self.main_btn = Main_Button()
        self.quit_btn = Quit_Button_2()
        self.buttons = [self.rtry_btn, self.main_btn, self.quit_btn]
        
        #textbox creation
        self.top_large_txt = textbox(d_width/2, 50, 150, white, display)
        self.score_txt = textbox(d_width/2 - 450, 200, 50, white, display)
        self.kills_txt = textbox(d_width/2 - 450, 250, 50, white, display)
        
        with open('stats.txt') as file:
            self.lines = file.readlines()
        
    def update(self):
        while self.show:
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
                self.next_state = "):"
            
            #key presses
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_state = "Main_Menu"
                    
            #mouse presses
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True
                    
        #mouse position
        self.m_pos = pygame.math.Vector2(pygame.mouse.get_pos())
        
    def render(self):
        display.fill(grey)
        
        #text
        self.top_large_txt.draw_c("Game Over")
        
        self.score_txt.draw_l(self.lines[0][:-1])
        self.kills_txt.draw_l(self.lines[1])
        
        #buttons
        self.rtry_btn.render()
        self.main_btn.render()
        self.quit_btn.render()

#Shows when player reaches the end of the game
class Win_Screen(Game_State):
    def __init__(self, prev_state):
        super().__init__(prev_state)
        
        #button creation
        self.rtry_btn = Retry_Button()
        self.main_btn = Main_Button()
        self.quit_btn = Quit_Button_2()
        self.buttons = [self.rtry_btn, self.main_btn, self.quit_btn]
        
        #textbox creation
        self.top_large_txt = textbox(d_width/2, 50, 150, white, display)
        self.score_txt = textbox(d_width/2 - 450, 200, 50, white, display)
        self.kills_txt = textbox(d_width/2 - 450, 250, 50, white, display)
        self.deaths_txt = textbox(d_width/2 - 450, 300, 50, white, display)
        
        with open('stats.txt') as file:
            self.lines = file.readlines()
        
    def update(self):
        while self.show:
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
                self.next_state = ":("
            
            #key presses
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_state = "Main_Menu"
                    
            #mouse presses
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True
                    
        #mouse position
        self.m_pos = pygame.math.Vector2(pygame.mouse.get_pos())
    
    def render(self):
        display.fill(grey)
        
        #text
        self.top_large_txt.draw_c("You Win!")
        
        self.score_txt.draw_l(self.lines[0][:-1])
        self.kills_txt.draw_l(self.lines[1][:-1])
        self.deaths_txt.draw_l(self.lines[2])
        
        #buttons
        self.rtry_btn.render()
        self.main_btn.render()
        self.quit_btn.render()

#Shows when the game is paused
class Paused(Game_State):
    def __init__(self, prev_state):
        super().__init__(prev_state)
        
        #button creation
        self.cont_btn = Continue_Button()
        self.main_btn = Main_Button()
        self.quit_btn = Quit_Button_2()
        self.buttons = [self.cont_btn, self.main_btn, self.quit_btn]
        
        #textbox creation
        self.top_large_txt = textbox(d_width/2, 50, 150, white, display)
        self.score_txt = textbox(d_width/2 - 450, 200, 50, white, display)
        self.kills_txt = textbox(d_width/2 - 450, 250, 50, white, display)
        self.lives_txt = textbox(d_width/2 - 450, 300, 50, white, display)
        
        with open('stats.txt') as file:
            self.lines = file.readlines()
    
    def update(self):
        while self.show:
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
                    self.next_state = 'Playing'
                    
            #mouse presses
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True
                    
        #mouse position
        self.m_pos = pygame.math.Vector2(pygame.mouse.get_pos())

    def render(self):
        display.fill(grey)
        
        #text
        self.top_large_txt.draw_c("Paused")
        
        self.score_txt.draw_l(self.lines[0][:-1])
        self.kills_txt.draw_l(self.lines[1][:-1])
        self.lives_txt.draw_l(self.lines[2])
        
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
        self.info_txt = textbox(d_width/2, d_height*0.88, 20, white, display)
        
        #image boxes
        self.cash_rect = cn.get_rect(topleft = (round(d_width - 290), round((d_height * 0.92)-2)))
        self.ammo_rect = amo.get_rect(topleft = (round(d_width - 297), round((d_height * 0.96)-5)))
        
        #camera for following player
        self.sim_dist = 800
        self.camera = Camera(self.sim_dist)
        
        self.level_matrix = []
        
        #sprite groups
        self.player_group = pygame.sprite.Group()
        self.level_group = pygame.sprite.Group()#maybe need to remove
        self.bullet_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.spawner_group = pygame.sprite.Group()
        self.footprint_group = pygame.sprite.Group()
        self.collectable_group = pygame.sprite.Group()
        self.interactable_group = pygame.sprite.Group()
        self.portal_group = pygame.sprite.Group()
        
        self.save_groups = {'self.bullet_group': self.bullet_group, 'self.enemy_group': self.enemy_group, 'self.spawner_group': self.spawner_group, 'self.collectable_group': self.collectable_group}#, 'self.interactable_group': self.interactable_group}
        self.save_angle_groups = {'self.footprint_group': self.footprint_group}#probably can combine with save_groups
        #specific save values might be better for each class not in one long list
        self.save_vals = ['once', 'c_type', 'needs_key', 'fade_limit', 'fade_timer', 'value', 'b_type', 'vel_back', 'anim_spd', 'idle_start_time', 'sight', 'spawn_timer', 'num', 'e_count_max', 'e_count', 's_spawn', 's_type', 'solid', 'health', 'healthmax', 'xvel', 'yvel', 'vel', 't', 'idle_vel', 'collidable_tiles', 'angle', 'attack_timer', 'wait', 'healthregen', 'footprint_timer', 'bullet_delay', 'damage', 'attack_dist']
        self.player_save_vals = ['prev_cash', 'prev_bullets', 'prev_kills', 'prev_score', 'solid', 'health', 'healthmax', 'xvel', 'yvel', 'vel', 't', 'idle_vel', 'collidable_tiles', 'weapon', 'attack_timer', 'wait', 'healthregen', 'energyval', 'energyregen', 'energymax', 'sprintvelmult', 'footprint_timer', 'score', 'bullet_delay', 'cash', 'change_lvl', 'damage', 'kills', 'bullets', 'attack_dist', 'portal_cost', 'respawn_protection', 'respawn_protection_timer']
        
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
        
        #fps
        self.clock = pygame.time.Clock()
        self.max_fps = 30#change to 60 maybe
        self.base_fps = 30#change to 60 maybe
        self.current_fps = 0
        self.dt = 0
        
        self.level = 0
        
        self.grass_list = [self.grass_obj, self.grass_obj, self.grass_obj, self.grass_obj, self.grass_obj, self.grass_obj, self.f_grass_obj]
    
    def update(self):
        with open('save.txt') as file:
            lines = file.readlines()
            if len(lines) == 0:
                self.player = Player(0, 0)
                self.player_group.add(self.player)
                self.load_sprites()
            else:
                self.load_save()
                
        self.load_level()
        self.load_portals()
        
        self.player.sync()
        
        while self.show:
            display.fill(grey)
            
            self.clock.tick(self.max_fps)
            self.current_fps = self.clock.get_fps()
            # self.dt = self.base_fps/self.current_fps
            # raw_time = self.clock.get_rawtime()
            # print(raw_time)
            self.input_detection()
            if not self.show:#immediately stop the loop when the game state is changed so player can't die in the same frame
                break#could also just check if the player dies above the input detection and not bother doing this if statement (and changes level above I think)
            
            self.camera.draw(self.player, self.moves, self.player_group, self.portal_group, self.level, self.level_matrix, self.level_group, self.m_pos, self.enemy_group, self.spawner_group, self.collectable_group, self.bullet_group, self.footprint_group, self.interactable_group, self.info_txt)
            
            if self.player.change_lvl:
                self.level += 1
                self.player.change_lvl = False
                
                if self.level > 2:
                    with open('save.txt', 'r+') as file:
                        file.seek(0)
                        file.truncate()
                        
                    with open('stats.txt', 'w') as file:
                        file.write(f'Score: {self.player.score}\nKills: {self.player.kills}\nDeaths: {self.player.deaths}')
                    
                    self.next_state = "Win_Screen"
                    self.show = False
                    
                else:
                    for t in self.level_group:
                        t.kill()
                    self.level_group.empty()
                    self.bullet_group.empty()
                    self.enemy_group.empty()
                    self.spawner_group.empty()
                    self.footprint_group.empty()
                    self.collectable_group.empty()
                    self.interactable_group.empty()
                    self.portal_group.empty()
                    
                    self.load_level()
                    self.load_sprites()
                    self.load_portals()
                    
                    self.player.sync()
            
            elif self.player.die():#maybe change to load and not save when die
                for t in self.level_group:
                    t.kill()
                self.level_group.empty()
                self.bullet_group.empty()
                self.enemy_group.empty()
                self.spawner_group.empty()
                self.footprint_group.empty()
                self.collectable_group.empty()
                self.interactable_group.empty()
                self.portal_group.empty()
                
                if self.player.lives > 0:
                    self.load_sprites()
                    self.save()
                    
                    with open('stats.txt', 'w') as file:
                        if self.player.lives == 1:
                            file.write('1 life remaining!!')
                        else:
                            file.write(str(self.player.lives) + ' lives remaining')
                            
                    self.next_state = "Death_Screen"
                    self.show = False
            
                elif self.player.lives == 0:
                    with open('save.txt', 'r+') as file:
                        file.seek(0)
                        file.truncate()
                        
                    with open('stats.txt', 'w') as file:
                        file.write(f'Score: {self.player.score}\nKills: {self.player.kills}')
                        
                    self.next_state = "Game_Over"
                    self.show = False
            
            for b in self.buttons:
                if b.update(self.m_pos, self.click):
                    return b.next_state
            
            self.render()
                
            pygame.display.update()
            
        return self.next_state
    
    def input_detection(self):#try set moves[4] to false instead of is new press
        self.click = False
        self.moves[6] = False
        self.moves[7] = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                self.next_state = "Why are you leaving when you're still playing? Are you sure it's saved?"
                self.save()#Few it's saved :D ...or did you not want to it be :P
                self.show = False
                break
            
            elif event.type == pygame.VIDEORESIZE:
                self.next_state = 'Paused'
                
                with open('stats.txt', 'w') as file:
                        file.write(f'Score: {self.player.score}\nKills: {self.player.kills}\nLives: {self.player.lives}')
                    
                self.save()
                self.show = False
                
                
            #key presses
            elif event.type == pygame.KEYDOWN:
                #movement
                if event.key == K_w or event.key == pygame.K_UP:#I don't need pygame.?!?!?!?!?
                    self.moves[0] = True
                    # self.player.dir.y -= 1
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.moves[1] = True
                    # self.player.dir.y += 1
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.moves[2]= True
                    # self.player.dir.x -= 1
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.moves[3] = True
                    # self.player.dir.x += 1
                #actions
                elif event.key == pygame.K_LSHIFT:
                    self.moves[4] = True
                    
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.moves[5] = True
                
                #weapon selection
                elif event.key == pygame.K_1:
                    self.player.weapon = 0
                    
                elif event.key == pygame.K_2:
                    self.player.weapon = 1
                    
                #game statistics (like Minecraft's F3 but worse)
                elif event.key == pygame.K_l:
                    self.show_stats = not self.show_stats
                    
                #pausing
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    self.next_state = 'Paused'
                    
                    with open('stats.txt', 'w') as file:
                        file.write(f'Score: {self.player.score}\nKills: {self.player.kills}\nLives: {self.player.lives}')
                    
                    self.save()
                    self.show = False
                    break
            
            elif event.type == pygame.KEYUP:
                #movement
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.moves[0] = False
                    # self.player.dir.y += 1
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.moves[1] = False
                    # self.player.dir.y -= 1
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.moves[2] = False
                    # self.player.dir.x += 1
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.moves[3] = False
                    # self.player.dir.x -= 1
                #actions
                elif event.key == pygame.K_LSHIFT:
                    self.moves[4] = False
                    self.player.is_new_press = True
                    
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.moves[5] = False
                    
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
        
    def render(self):
        if self.show_stats:
            self.fps_txt.draw_l(f"FPS:{round(self.current_fps)} | Max:{self.max_fps}")
            
        self.score_txt.draw_l(f"Score: {self.player.score}")
        
        self.cash_txt.draw_l(str(self.player.cash))
        self.ammo_txt.draw_l(str(self.player.bullets))
        display.blit(cn, self.cash_rect)
        display.blit(amo, self.ammo_rect)
        
    #saving the game
    def save(self):#use repr instead?
        with open('save.txt', 'w') as file:
            file.write(f'self.level={self.level}')
            
            file.write(f'\nself.player = {self.player.__class__.__name__}({self.player.pos.x}, {self.player.pos.y}, lives = {self.player.lives})\n')
            for attribute, value in self.player.__dict__.items():
                if attribute in self.player_save_vals:
                    if type(value) == str:
                        file.write(f'self.player.{attribute} = "{value}"\n')
                    else:
                        file.write(f'self.player.{attribute} = {value}\n')
            
            file.write('self.player_group.add(self.player)\n')
                    
            for name, value in self.save_groups.items():
                for sprite in value.sprites():
                    file.write(f'sprite = {sprite.__class__.__name__}({sprite.pos.x}, {sprite.pos.y})\n')
                    for attribute, value in sprite.__dict__.items():
                        if attribute in self.save_vals:
                            if type(value) == str:
                                file.write(f'sprite.{attribute} = "{value}"\n')
                            else:
                                file.write(f'sprite.{attribute} = {value}\n')
                    file.write(f'{name}.add(sprite)\n')
                    
            for name, value in self.save_angle_groups.items():
                for sprite in value.sprites():
                    file.write(f'sprite = {sprite.__class__.__name__}({sprite.pos.x}, {sprite.pos.y}, {sprite.angle})\n')
                    for attribute, value in sprite.__dict__.items():
                        if attribute in self.save_vals:
                            if type(value) == str:
                                file.write(f'sprite.{attribute} = "{value}"\n')
                            else:
                                file.write(f'sprite.{attribute} = {value}\n')
                    file.write(f'{name}.add(sprite)\n')
                    
            for sprite in self.interactable_group.sprites():
                if sprite.type == "chest":
                    file.write(f'sprite = {sprite.__class__.__name__}({sprite.pos.x}, {sprite.pos.y}, {sprite.state})\n')
                else:
                    file.write(f'sprite = {sprite.__class__.__name__}({sprite.pos.x}, {sprite.pos.y}, {sprite.state}, "{sprite.d_type}")\n')
                for attribute, value in sprite.__dict__.items():
                    if attribute in self.save_vals:
                        if type(value) == str:
                            file.write(f'sprite.{attribute} = "{value}"\n')
                        else:
                            file.write(f'sprite.{attribute} = {value}\n')
                file.write('self.interactable_group.add(sprite)\n')
    
    def load_save(self):
        with open('save.txt') as file:
            exec(file.read())
        
    def load_level(self):#load_level_matrix
        self.level_matrix.clear()
        
        with open(f'levels/level_{self.level}.txt') as f:#'levels/test_level.txt'
            lines = f.readlines()
            
            for r in range(len(lines)):
                self.level_matrix.append([])
                
                for c in range(len(lines[r])):
                    if lines[r][c] == " ":
                        tile = random.choice(self.grass_list)(c, r)
                        self.level_matrix[r].append(tile)
                        self.level_group.add(tile)
                        
                    elif lines[r][c] == "W":
                        tile = Tile("wall", wall, tile_scale*c, tile_scale*r)
                        self.level_matrix[r].append(tile)
                        self.level_group.add(tile)
                        
                    elif lines[r][c] == "B":
                        tile = Tile("b_portal", b_portal, tile_scale*c, tile_scale*r)
                        self.level_matrix[r].append(tile)
                        self.level_group.add(tile)
                        
                    elif lines[r][c] == "T":
                        tile = Tile("tree", tree, tile_scale*c, tile_scale*r)
                        self.level_matrix[r].append(tile)
                        self.level_group.add(tile)
                        
                    elif lines[r][c] == "M":
                        tile = Tile("mud", mud, tile_scale*c, tile_scale*r)
                        self.level_matrix[r].append(tile)
                        self.level_group.add(tile)
                        
                    elif lines[r][c] == ".":
                        tile = Tile("snowy_grass", snowy_grass, tile_scale*c, tile_scale*r)
                        self.level_matrix[r].append(tile)
                        self.level_group.add(tile)
        
    def load_sprites(self):
        f = open(f"levels/level_{self.level}_e.txt")
        lines = f.readlines()
        for r in range(0, len(lines)):
            for c in range(0, len(lines[r])):
                if lines[r][c] == "P":
                    self.player.pos.x = tile_scale*(c+0.5)
                    self.player.pos.y = tile_scale*(r+0.5)
                elif lines[r][c] == "Z":
                    zombie = Zombie(tile_scale*(c+0.5), tile_scale*(r+0.5))
                    self.enemy_group.add(zombie)
                    
                elif lines[r][c] == "S":
                    skeleton = Skeleton(tile_scale*(c+0.5), tile_scale*(r+0.5))
                    self.enemy_group.add(skeleton)
                    
                elif lines[r][c] == "G":
                    ghost = Ghost(tile_scale*(c+0.5), tile_scale*(r+0.5))
                    self.enemy_group.add(ghost)
                    
                elif lines[r][c] == "g":
                    grave = Grave(tile_scale*(c+0.5), tile_scale*(r+0.5))
                    self.spawner_group.add(grave)
                    
                elif lines[r][c] == "D":#up to right
                    door = Door(tile_scale*c, tile_scale*(r+1), 0)
                    self.interactable_group.add(door)
                    
                elif lines[r][c] == "d":#up to left
                    door = Door(tile_scale*(c+1), tile_scale*(r+1), 0, "tl")
                    self.interactable_group.add(door)
                    
                elif lines[r][c] == "O":#down to right
                    door = Door(tile_scale*c, tile_scale*r, 1, "br")
                    self.interactable_group.add(door)
                    
                elif lines[r][c] == "o":#down to left
                    door = Door(tile_scale*(c+1), tile_scale*r, 1, "bl")
                    self.interactable_group.add(door)
                    
                elif lines[r][c] == "1":
                    w_chest = Chest(tile_scale*c, tile_scale*r + 48, 0)
                    self.interactable_group.add(w_chest)
                    
                elif lines[r][c] == "2":
                    i_chest = Iron_Chest(tile_scale*c, tile_scale*r + 48, 0)
                    self.interactable_group.add(i_chest)
                    
                elif lines[r][c] == "3":
                    g_chest = Gold_Chest(tile_scale*c, tile_scale*r + 48, 0)
                    self.interactable_group.add(g_chest)
        
    def load_portals(self):
        with open(f"levels/level_{self.level}_p.txt") as f:
            lines = f.readlines()
            portals = {}
            for r in range(len(lines)):
                for c in range(len(lines[r])):
                    if lines[r][c] != '#' and lines[r][c] != ' ' and lines[r][c] != '\n':
                        if not lines[r][c] in portals:
                            portals[lines[r][c]] = [c * tile_scale, r * tile_scale]
                        else:
                            portals[lines[r][c]].extend((c * tile_scale, r * tile_scale))
                            newPortal = Portal("portal", portal, portals[lines[r][c]])
                            self.portal_group.add(newPortal)
                            del portals[lines[r][c]]
    
    #varying grass tile creation
    def grass_obj(self, c, r):
        tile = Tile("grass", grass, tile_scale*c, tile_scale*r)
        return tile

    def f_grass_obj(self, c, r):
        tile = Tile("flower_grass", flower_grass, tile_scale*c, tile_scale*r)
        return tile