from settings import *
from tile import *
from textbox import *
import pygame, sys, random, math
from pygame.locals import *
from entity import *
from button import *

#clock for fps
clock = pygame.time.Clock()

#icon
pygame.display.set_icon(portal)

#button creation
play_btn = Button(d_width/2,d_height/2,play_u,play_d)#,display)
ctrl_btn = Button(d_width/2,d_height/1.45,ctrl_u,ctrl_d)#,display)
quit_btn = Button(d_width/2,d_height/1.13,quit_u,quit_d)#,display)
back_btn = Button(d_width/2,d_height*0.92,back_u,back_d)#,display)
main_btn = Button(d_width/2,d_height/1.45,main_u,main_d)#,display)
yes_btn = Button(d_width*0.4,d_height/1.45,yes_u,yes_d)#,display)
no_btn = Button(d_width*0.6,d_height/1.45,no_u,no_d)#,display)
rtry_btn = Button(d_width/2,d_height/2,rtry_u,rtry_d)#,display)
cont_btn = Button(d_width/2,d_height/2,cont_u,cont_d)#,display)
rspn_btn = Button(d_width/2,d_height/2,rspn_u,rspn_d)#,display)

#main menu images
title_rect = title_img.get_rect(center = (round(d_width/2),round(d_height/4)))
menu_portal_rect = pygame.Rect((round(d_width/2) + 212),(round(d_height/4) + 30),32,56)

#controls image
ctrls_rect = ctrls_img.get_rect(topleft = (0,0))

#varying grass tile creation
def grass_obj(group,c,r):
    newTile = Tile("grass",grass,tile_scale*c,tile_scale*r)
    group.add(newTile)
    camera.add(newTile)

def f_grass_obj(group,c,r):
    newTile = Tile("flower_grass",flower_grass,tile_scale*c,tile_scale*r)
    group.add(newTile)
    camera.add(newTile)

grass_list = [grass_obj,grass_obj,grass_obj,grass_obj,grass_obj,grass_obj,f_grass_obj]

#level loading
def load_level(group):
    p_1 = []
    p_2 = []
    p_3 = []
    p_4 = []
    p_5 = []
    p_6 = []
    p_7 = []
    p_8 = []
    p_9 = []
    p_0 = []
    f = open(f"levels/level_{level}.txt")
    lines = f.readlines()
    for r in range(0,len(lines)):
        for c in range(0,len(lines[r])):
            if lines[r][c] == " ":
                random.choice(grass_list)(group,c,r)
            elif lines[r][c] == "W":
                newTile = Tile("wall",wall,tile_scale*c,tile_scale*r)
                group.add(newTile)
                camera.add(newTile)
            elif lines[r][c] == "B":
                newTile = Tile("b_portal",b_portal,tile_scale*c,tile_scale*r)
                group.add(newTile)
                camera.add(newTile)
            elif lines[r][c] == "T":
                newTile = Tile("tree",tree,tile_scale*c,tile_scale*r)
                group.add(newTile)
                camera.add(newTile)
            elif lines[r][c] == "M":
                newTile = Tile("mud",mud,tile_scale*c,tile_scale*r)
                group.add(newTile)
                camera.add(newTile)
            elif lines[r][c] == ".":
                newTile = Tile("snowy_grass",snowy_grass,tile_scale*c,tile_scale*r)
                group.add(newTile)
                camera.add(newTile)
            #else:
            #    for i in range(0,9):
            #        if lines[r][c] == str(i):
            #            p_{i}.append(c*tile_scale)
            #            p_{i}.append(r*tile_scale)
            elif lines[r][c] == "1":
                p_1.append(c*tile_scale)
                p_1.append(r*tile_scale)
            elif lines[r][c] == "2":
                p_2.append(c*tile_scale)
                p_2.append(r*tile_scale)
            elif lines[r][c] == "3":
                p_3.append(c*tile_scale)
                p_3.append(r*tile_scale)
            elif lines[r][c] == "4":
                p_4.append(c*tile_scale)
                p_4.append(r*tile_scale)
            elif lines[r][c] == "5":
                p_5.append(c*tile_scale)
                p_5.append(r*tile_scale)
            elif lines[r][c] == "6":
                p_6.append(c*tile_scale)
                p_6.append(r*tile_scale)
            elif lines[r][c] == "7":
                p_7.append(c*tile_scale)
                p_7.append(r*tile_scale)
            elif lines[r][c] == "8":
                p_8.append(c*tile_scale)
                p_8.append(r*tile_scale)
            elif lines[r][c] == "9":
                p_9.append(c*tile_scale)
                p_9.append(r*tile_scale)
            elif lines[r][c] == "0":
                p_0.append(c*tile_scale)
                p_0.append(r*tile_scale)
    #for i in range(0,9):
    #    if len(p_{i}) == 4:
    #        newTile = Portal("portal",portal,p_{i})
    #        group.add(newTile)
    #        camera.add(newTile)
    if len(p_1) == 4:
        newTile = Portal("portal",portal,p_1)
        group.add(newTile)
        camera.add(newTile)
    if len(p_2) == 4:
        newTile = Portal("portal",portal,p_2)
        group.add(newTile)
        camera.add(newTile)
    if len(p_3) == 4:
        newTile = Portal("portal",portal,p_3)
        group.add(newTile)
        camera.add(newTile)
    if len(p_4) == 4:
        newTile = Portal("portal",portal,p_4)
        group.add(newTile)
        camera.add(newTile)
    if len(p_5) == 4:
        newTile = Portal("portal",portal,p_5)
        group.add(newTile)
        camera.add(newTile)
    if len(p_6) == 4:
        newTile = Portal("portal",portal,p_6)
        group.add(newTile)
        camera.add(newTile)
    if len(p_7) == 4:
        newTile = Portal("portal",portal,p_7)
        group.add(newTile)
        camera.add(newTile)
    if len(p_8) == 4:
        newTile = Portal("portal",portal,p_8)
        group.add(newTile)
        camera.add(newTile)
    if len(p_9) == 4:
        newTile = Portal("portal",portal,p_9)
        group.add(newTile)
        camera.add(newTile)
    if len(p_0) == 4:
        newTile = Portal("portal",portal,p_0)
        group.add(newTile)
        camera.add(newTile)
    
    lvl_dim = [len(lines[0])-1,len(lines)]
    #print(lvl_dim)
    #return lvl_dim

def load_sprites(e_group,s_group,i_group):
    f = open(f"levels/level_{level}_e.txt")
    lines = f.readlines()
    for r in range(0,len(lines)):
        for c in range(0,len(lines[r])):
            if lines[r][c] == "Z":
                zombie = Zombie(tile_scale*(c+0.5),tile_scale*(r+0.5),display,zmbhd,zmbrm,False,-1)
                e_group.add(zombie)
                camera.add(zombie)
            elif lines[r][c] == "S":
                skeleton = Skeleton(tile_scale*(c+0.5),tile_scale*(r+0.5),display,sklhd,sklrm,False,-1)
                e_group.add(skeleton)
                camera.add(skeleton)
            elif lines[r][c] == "G":
                ghost = Ghost(tile_scale*(c+0.5),tile_scale*(r+0.5),display,gsthdV,gstrmV,gsttlAnim,False,-1)
                e_group.add(ghost)
                camera.add(ghost)
            elif lines[r][c] == "g":
                grave = Grave(tile_scale*(c+0.5),tile_scale*(r+0.5),display,grvstn,0,0)
                s_group.add(grave)
                camera.add(grave)
            elif lines[r][c] == "D":#up to right
                door = Door(tile_scale*c,tile_scale*(r+1),display,door_clock_up,door_anticlock_right,"ur")
                i_group.add(door)
                camera.add(door)
            elif lines[r][c] == "d":#up to left
                door = Door(tile_scale*(c+1),tile_scale*(r+1),display,door_anticlock_up,door_clock_left,"ul")
                i_group.add(door)
                camera.add(door)
            elif lines[r][c] == "O":#down to right
                door = Door(tile_scale*c,tile_scale*r,display,door_anticlock_down,door_clock_right,"dr")
                i_group.add(door)
                camera.add(door)
            elif lines[r][c] == "o":#down to left
                door = Door(tile_scale*(c+1),tile_scale*r,display,door_clock_down,door_anticlock_left,"dl")
                i_group.add(door)
                camera.add(door)
            elif lines[r][c] == "1":
                w_chest = Chest(tile_scale*c,tile_scale*r + 48,display,wood_closed,wood_open,1)
                i_group.add(w_chest)
                camera.add(w_chest)
            elif lines[r][c] == "2":
                i_chest = Chest(tile_scale*c,tile_scale*r + 48,display,iron_closed,iron_open,2)
                i_group.add(i_chest)
                camera.add(i_chest)
            elif lines[r][c] == "3":
                g_chest = Chest(tile_scale*c,tile_scale*r + 48,display,gold_closed,gold_open,3)
                i_group.add(g_chest)
                camera.add(g_chest)

#sprite groups
level_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
spawner_group = pygame.sprite.Group()
footprint_group = pygame.sprite.Group()
collectable_group = pygame.sprite.Group()
interactable_group = pygame.sprite.Group()

level = 0

#hear for now(maybe)
#load_level(level_group)
#load_sprites(enemy_group,spawner_group)

#menu sprite
m_player = Menu_player(d_width/10,d_height/10,display,plrhd,plrrm)
m_group = pygame.sprite.Group()#why does it not die??
m_group.add(m_player)

#player = Player(200*sprite_scale,200*sprite_scale,display,plrhd,plrrm)

#prev_score = player.score
#prev_health = player.health
#prev_energy = player.energyval
#prev_bullets = player.bullets
#prev_cash = player.cash
#prev_kills = player.kills

#camera.add(player)

#textbox creation
cash_txt = textbox(d_width - 260,(d_height * 0.92)-2,20,yellow,display)
ammo_txt = textbox(d_width - 260,(d_height * 0.96)-2,20,yellow,display)
playing_score_txt = textbox(5,5,20,white,display)
fps_txt = textbox(5,d_height - 20,20,red,display)
middle_large_txt = textbox(d_width/2,d_height/2,150, white, display)
top_large_txt = textbox(d_width/2,100,150,white,display)
current_score_txt = textbox(d_width/2 - 450,200,50,white,display)
kills_txt = textbox(d_width/2 - 450,250,50,white,display)
lives_txt = textbox(d_width/2 - 450,300,50,white,display)


#icon surfaces
cash_rect = cn.get_rect(topleft = (round(d_width - 290),round((d_height * 0.92)-2)))#pygame.Rect(d_width - 290, (d_height * 0.92)-2,18,18)
ammo_rect = amo.get_rect(topleft = (round(d_width - 297),round((d_height * 0.96)-5)))#pygame.Rect(d_width - 297, (d_height * 0.96)-5,18,18)

#game clock + fps
current_fps = 0
dt = 0
max_fps = 30#60
framerate = 60
multiplier = 1

#main game loop
g_running = True
while g_running:
    display.fill(grey)
    camera.display_surface.fill(grey)
    clock.tick(max_fps)
    current_fps = clock.get_fps()
    dt = current_fps/max_fps
    
    weapon_swap_pressed = False
    click = False
    use = False
    
    #events
    for event in pygame.event.get():
        if event.type == QUIT:
            g_running = False
        #inputs
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                up_pressed = True
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                down_pressed = True
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                left_pressed = True
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                right_pressed = True
            elif event.key == pygame.K_1:
                player.weapon = 0
            elif event.key == pygame.K_2:
                player.weapon = 1
            elif event.key == pygame.K_LSHIFT:
                dash_pressed = True
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                attack_pressed = True
            elif event.key == pygame.K_l:
                game_stats = True
            elif event.key == pygame.K_ESCAPE:
                if game_state == "quit":
                    game_state = prev_state
                elif game_state == "playing":
                    game_paused = not game_paused
                elif game_state == "shop":
                    game_state = "playing"
                else:
                    game_state = "quit"
            elif event.key == pygame.K_p:
                if game_state == "playing":
                    game_paused = not game_paused
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                attack_pressed = True
                click = True
            elif event.button == 3:
                use = True
                #dash_pressed = True
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                up_pressed = False
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                down_pressed = False
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                left_pressed = False
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                right_pressed = False
            elif event.key == pygame.K_LSHIFT:
                dash_pressed = False
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                attack_pressed = False
            elif event.key == pygame.K_l:
                game_stats = False
            elif event.key == pygame.K_q:
                weapon_swap_pressed = True
            #if event.key == pygame.K_e:
            #    heal = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                attack_pressed = False
                #click = True
            #if event.button == 3:
            #    use = False
                #dash_pressed = False

        elif event.type == pygame.MOUSEWHEEL:
            weapon_swap_pressed = True

    #mouse position
    mx,my = pygame.mouse.get_pos()
    #tuple of all input variables
    moves = (up_pressed,down_pressed,left_pressed,right_pressed,dash_pressed,attack_pressed,weapon_swap_pressed,use)
    
    #game states
    if game_state == "main_menu":#i can fix the menu class
        prev_state = game_state

        display.blit(title_img,title_rect)

        m_player.render_bar(play_btn.rect,play_btn.image)

        #play_btn.render()
        #ctrl_btn.render()
        #quit_btn.render()

        #play button
        if play_btn.update(mx,my,click,m_player):
            game_state = "playing"
            m_player.pos = pygame.math.Vector2((d_width/10,d_height/10))#i may be able to remove later

        #controls button
        if ctrl_btn.update(mx,my,click,m_player):
            game_state = "ctrl_menu"

        #quit button
        if quit_btn.update(mx,my,click,m_player):
            game_state = "quit"

        m_player.update(moves,mx,my,menu_portal_rect,play_btn.group,quit_btn.group,ctrl_btn.group)

        if m_player.hitbox.colliderect(menu_portal_rect):
            #m_player.kill()
            game_state = "playing"
            m_player.pos = pygame.math.Vector2((d_width/10,d_height/10))#i may be able to remove later

    elif game_state == "ctrl_menu":
        prev_state = game_state

        display.blit(ctrls_img,ctrls_rect)

        #back_btn.render()

        #controls button
        if back_btn.update(mx,my,click,m_player):
            game_state = "main_menu"

    elif game_state == "playing":
        if player_count < 1:
            player = Player(200*sprite_scale,200*sprite_scale,display,plrhd,plrrm)
            camera.add(player)

            prev_score = player.score
            prev_health = player.health
            prev_energy = player.energyval
            prev_bullets = player.bullets
            prev_cash = player.cash
            prev_kills = player.kills

            load_level(level_group)
            load_sprites(enemy_group,spawner_group,interactable_group)

            player_count += 1

        prev_state = game_state

        if game_paused:#paused
            #pygame.draw.rect(display,black,pygame.Rect(0,0,d_width,d_height))
            top_large_txt.draw_c("Paused")
            current_score_txt.draw_l("Score: "+str(player.score))
            kills_txt.draw_l("Kills: "+str(player.kills))
            lives_txt.draw_l("Lives: "+str(player.lives))

            #continue button
            if cont_btn.update(mx,my,click,m_player):
                game_paused = False

            #main button
            if main_btn.update(mx,my,click,m_player):
                game_state = "main_menu"
                game_paused = False

            #quit button
            if quit_btn.update(mx,my,click,m_player):
                game_state = "quit"

        else:#not paused
            timer += 1
            if camera.c_draw(player,moves,level_group,mx,my,enemy_group,spawner_group,collectable_group,bullet_group,footprint_group,interactable_group):
                level += 1
                prev_score = player.score
                prev_bullets = player.bullets
                prev_cash = player.cash
                prev_kills = player.kills
                player.energyval = player.energymax
                
                if level > 2:
                    game_state = "You Win!"
                else:
                    for t in level_group:
                        t.kill()
                    level_group.empty()
                    bullet_group.empty()
                    enemy_group.empty()
                    spawner_group.empty()
                    footprint_group.empty()
                    collectable_group.empty()
                    camera.c_empty()

                    player.pos = pygame.math.Vector2((200*sprite_scale,200*sprite_scale))
                    load_level(level_group)
                    load_sprites(enemy_group,spawner_group,interactable_group)

            if player.die():
                player.score = prev_score - 100
                player.health = player.healthmax
                player.energyval = player.energymax
                player.bullets = prev_bullets
                player.kills = prev_kills
                player.cash = prev_cash - 50
                if player.cash < 0:
                    player.cash = 0
                if player.score < 0:
                    player.score = 0

                for t in level_group:
                    t.kill()
                level_group.empty()
                bullet_group.empty()
                enemy_group.empty()
                spawner_group.empty()
                footprint_group.empty()
                collectable_group.empty()
                camera.c_empty()

                load_level(level_group)
                load_sprites(enemy_group,spawner_group,interactable_group)
                game_state = "You Died"
            
            if game_stats:
                fps_txt.draw_l("FPS:"+str(int(current_fps))+" | Max:"+str(max_fps))
                
            playing_score_txt.draw_l("Score: "+str(player.score))
            cash_txt.draw_l(str(player.cash))
            ammo_txt.draw_l(str(player.bullets))
            display.blit(cn,cash_rect)
            display.blit(amo,ammo_rect)
            
            if player.lives == 0:
                game_state = "Game Over"

    elif game_state == "You Died":
        prev_state = game_state

        top_large_txt.draw_c(game_state)
        
        if player.lives == 1:
            kills_txt.draw_l(str(player.lives)+" life remaining")
        else:
            kills_txt.draw_l(str(player.lives)+" lives remaining")

        #respawn button
        if rspn_btn.update(mx,my,click,m_player):
            game_state = "playing"

        #main button
        if main_btn.update(mx,my,click,m_player):
            game_state = "main_menu"

        #quit button
        if quit_btn.update(mx,my,click,m_player):
            game_state = "quit"
                
    elif game_state == "Game Over" or game_state == "You Win!":
        prev_state = game_state
        
        level = 0
        
        level_group.empty()
        bullet_group.empty()
        enemy_group.empty()
        spawner_group.empty()
        footprint_group.empty()
        collectable_group.empty()
        camera.empty()
                
        player.kill()

        player_count = 0
        
        top_large_txt.draw_c(game_state)
        current_score_txt.draw_l("Score: "+str(player.score))
        kills_txt.draw_l("Kills: "+str(player.kills))

        if game_state == "You Win!":
            lives_txt.draw_l("Lives: "+str(player.lives))

        #main_btn.render()

        #retry button
        if rtry_btn.update(mx,my,click,m_player):
            game_state = "playing"

        #main button
        if main_btn.update(mx,my,click,m_player):
            game_state = "main_menu"

        #quit button
        if quit_btn.update(mx,my,click,m_player):
            game_state = "quit"

    elif game_state == "quit":
        top_large_txt.draw_c("Are you sure?")

        #yes_btn.render()
        #no_btn.render()

        #yes button
        if yes_btn.update(mx,my,click,m_player):
            #if prev_state == "shop" or prev_state == "playing":
            #    game_state = "main_menu"
            #    game_paused = False
            #else:
            g_running = False
        
        #no button
        if no_btn.update(mx,my,click,m_player):
            game_state = prev_state

    elif game_state == "shop":
        prev_state = game_state
        
    
    pygame.display.update()
    
pygame.quit()
sys.exit()
