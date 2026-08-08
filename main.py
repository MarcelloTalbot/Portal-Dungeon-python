from settings import *
from tile import *
from textbox import *
import pygame, sys, random, math
from pygame.locals import *
from entity import *

#clock for FPS
clock = pygame.time.Clock()

#icon
pygame.display.set_icon(portal)

play_img = play_u
play_rect = play_img.get_rect(center = (round(d_width/2),round(d_height/2)))
play_group = [play_rect,play_img,play_u,play_d]

ctrl_img = ctrl_u
ctrl_rect = ctrl_img.get_rect(center = (round(d_width/2),round(d_height/1.45)))
ctrl_group = [ctrl_rect,ctrl_img,ctrl_u,ctrl_d]

quit_img = quit_u
quit_rect = quit_img.get_rect(center = (round(d_width/2),round(d_height/1.13)))
quit_group = [quit_rect,quit_img,quit_u,quit_d]

back_img = back_u
back_rect = back_img.get_rect(center = (round(d_width/2),round(d_height-64)))
back_group = [back_rect,back_img,back_u,back_d]
                                                               
title_rect = title_img.get_rect(center = (round(d_width/2),round(d_height/4)))
menu_portal_rect = pygame.Rect((round(d_width/2) + 212),(round(d_height/4) + 30),32,56)

ctrls_rect = ctrls_img.get_rect(topleft = (0,0))

def grass_obj(group,c,r):
    newTile = Tile("grass",grass,tile_scale*c,tile_scale*r)
    group.add(newTile)
    camera.add(newTile)

def f_grass_obj(group,c,r):
    newTile = Tile("flower_grass",flower_grass,tile_scale*c,tile_scale*r)
    group.add(newTile)
    camera.add(newTile)

grass_list = [grass_obj,grass_obj,grass_obj,grass_obj,grass_obj,grass_obj,f_grass_obj]

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

def load_sprites(e_group,s_group):
    f = open(f"levels/level_{level}_e.txt")
    lines = f.readlines()
    for r in range(0,len(lines)):
        for c in range(0,len(lines[r])):
            if lines[r][c] == "Z":
                zombie = Zombie(c*tile_scale,r*tile_scale,display,zmbhd,zmbrm,False,-1)
                e_group.add(zombie)
                camera.add(zombie)
            elif lines[r][c] == "S":
                skeleton = Skeleton(c*tile_scale,r*tile_scale,display,sklhd,sklrm,False,-1)
                e_group.add(skeleton)
                camera.add(skeleton)
            elif lines[r][c] == "G":
                ghost = Ghost(c*tile_scale,r*tile_scale,display,gsthdV,gstrmV,gsttlAnim,False,-1)
                e_group.add(ghost)
                camera.add(ghost)
            elif lines[r][c] == "g":
                grave = Grave(c*tile_scale,r*tile_scale,display,grvstn,0)
                s_group.add(grave)
                camera.add(grave)

#sprite groups
level_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
spawner_group = pygame.sprite.Group()
footprint_group = pygame.sprite.Group()
collectable_group = pygame.sprite.Group()

level = 0

#hear for now(maybe)
load_level(level_group)
load_sprites(enemy_group,spawner_group)

#menu sprite
m_player = Menu_player(d_width/10,d_height/10,display,plrhd,plrrm)
m_group = pygame.sprite.Group()#why does it not die??
m_group.add(m_player)

player = Player(200*sprite_scale,200*sprite_scale,display,plrhd,plrrm)

prev_score = player.score
prev_health = player.health
prev_energy = player.energyval
prev_bullets = player.bullets
prev_cash = player.cash
prev_kills = player.kills

camera.add(player)

#text
cash_txt = textbox(d_width - 260,(d_height * 0.92)-2,20,yellow,display)
ammo_txt = textbox(d_width - 260,(d_height * 0.96)-2,20,yellow,display)
score_txt = textbox(5,5,20,white,display)
fpslabel = textbox(5,d_height - 20,20,red,display)
paused_txt = textbox(d_width/2 - 250 ,d_height/2 - 75,150, white, display)
game_over_txt = textbox(d_width/2 - 450,50,150,white,display)
win_txt = textbox(d_width/2 - 450,50,150,white,display)
f_score_txt = textbox(d_width/2 - 450,200,50,white,display)
kills_txt = textbox(d_width/2 - 450,250,50,white,display)

#icon surfaces
cash_rect = cn.get_rect(topleft = (round(d_width - 290),round((d_height * 0.92)-2)))#pygame.Rect(d_width - 290, (d_height * 0.92)-2,18,18)
ammo_rect = amo.get_rect(topleft = (round(d_width - 297),round((d_height * 0.96)-5)))#pygame.Rect(d_width - 297, (d_height * 0.96)-5,18,18)

#game clock + fps
fps = 0
dt = 0
ogframerate = 30#60
framerate = 60
multiplier = 1

#main game loop
g_running = True
while g_running:
    display.fill(grey)
    camera.display_surface.fill(grey)
    clock.tick(ogframerate)
    fps = clock.get_fps()
    dt = fps/ogframerate
    
    weapon_swap_pressed = False
    click = False
    
    #events
    for event in pygame.event.get():
        if event.type == QUIT:
            g_running = False
        #inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                up_pressed = True
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                down_pressed = True
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                left_pressed = True
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                right_pressed = True
            if event.key == pygame.K_1:
                player.weapon = 0
            if event.key == pygame.K_2:
                player.weapon = 1
            if event.key == pygame.K_LSHIFT:
                dash_pressed = True
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                attack_pressed = True
            if event.key == pygame.K_l:
                game_stats = True
            if event.key == pygame.K_ESCAPE:
                g_running = False
            if event.key == pygame.K_p:
                if game_state == "playing":
                    game_paused = not game_paused
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                attack_pressed = True
            if event.button == 3:
                dash_pressed = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                up_pressed = False
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                down_pressed = False
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                left_pressed = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                right_pressed = False
            if event.key == pygame.K_LSHIFT:
                dash_pressed = False
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                attack_pressed = False
            if event.key == pygame.K_l:
                game_stats = False
            if event.key == pygame.K_q:
                weapon_swap_pressed = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                attack_pressed = False
                click = True
            if event.button == 3:
                dash_pressed = False

        if event.type == pygame.MOUSEWHEEL:
            weapon_swap_pressed = True

    #mouse position
    mx,my = pygame.mouse.get_pos()
    #tuple of all input variables
    moves = (up_pressed,down_pressed,left_pressed,right_pressed,dash_pressed,attack_pressed,weapon_swap_pressed)
    
    #game states
    if game_state == "main_menu":#i can fix the menu class
        display.blit(title_img,title_rect)
        m_player.render_bar(play_rect,play_img)
        display.blit(play_img,play_rect)
        display.blit(quit_img,quit_rect)
        display.blit(ctrl_img,ctrl_rect)

        #play button
        if play_rect.collidepoint((mx,my)):
            if play_img != play_d:
                play_img = play_d
                if m_player.hitbox.colliderect(play_rect.topleft[0]+8,play_rect.topleft[1]+8,play_rect.topright[0]-play_rect.topleft[0]-16,play_rect.bottomleft[1]-play_rect.topleft[1]-32):
                    m_player.pos.y += 16
            if click:
                game_state = "playing"
        else:
            if play_img != play_u:
                play_img = play_u
                if m_player.hitbox.colliderect(play_rect.topleft[0]+8,play_rect.topleft[1]+8+16,play_rect.topright[0]-play_rect.topleft[0]-16,play_rect.bottomleft[1]-play_rect.topleft[1]-32):
                    m_player.pos.y -= 16

        #quit button
        if quit_rect.collidepoint((mx,my)):
            if quit_img != quit_d:
                quit_img = quit_d
                if m_player.hitbox.colliderect(quit_rect.topleft[0]+8,quit_rect.topleft[1]+8,quit_rect.topright[0]-quit_rect.topleft[0]-16,quit_rect.bottomleft[1]-quit_rect.topleft[1]-32):
                    m_player.pos.y += 16
            if click:
                g_running = False
        else:
            if quit_img != quit_u:
                quit_img = quit_u
                if m_player.hitbox.colliderect(quit_rect.topleft[0]+8,quit_rect.topleft[1]+8+16,quit_rect.topright[0]-quit_rect.topleft[0]-16,quit_rect.bottomleft[1]-quit_rect.topleft[1]-32):
                    m_player.pos.y -= 16

        #controls button
        if ctrl_rect.collidepoint((mx,my)):
            if ctrl_img != ctrl_d:
                ctrl_img = ctrl_d
                if m_player.hitbox.colliderect(ctrl_rect.topleft[0]+8,ctrl_rect.topleft[1]+8,ctrl_rect.topright[0]-ctrl_rect.topleft[0]-16,ctrl_rect.bottomleft[1]-ctrl_rect.topleft[1]-32):
                    m_player.pos.y += 16
            if click:
                game_state = "ctrl_menu"
        else:
            if ctrl_img != ctrl_u:
                ctrl_img = ctrl_u
                if m_player.hitbox.colliderect(ctrl_rect.topleft[0]+8,ctrl_rect.topleft[1]+8+16,ctrl_rect.topright[0]-ctrl_rect.topleft[0]-16,ctrl_rect.bottomleft[1]-ctrl_rect.topleft[1]-32):
                    m_player.pos.y -= 16

        play_group = [play_rect,play_img,play_u,play_d]
        quit_group = [quit_rect,quit_img,quit_u,quit_d]
        ctrl_group = [ctrl_rect,ctrl_img,ctrl_u,ctrl_d]

        m_player.update(moves,mx,my,menu_portal_rect,play_group,quit_group,ctrl_group)

        if m_player.hitbox.colliderect(menu_portal_rect):
            m_player.kill()
            game_state = "playing"

    elif game_state == "ctrl_menu":
        display.blit(ctrls_img,ctrls_rect)
        display.blit(back_img,back_rect)
        #controls button
        if back_rect.collidepoint((mx,my)):
            if back_img != back_d:
                back_img = back_d
                if m_player.hitbox.colliderect(back_rect.topleft[0]+8,back_rect.topleft[1]+8,back_rect.topright[0]-back_rect.topleft[0]-16,back_rect.bottomleft[1]-back_rect.topleft[1]-32):
                    m_player.pos.y += 16
            if click:
                game_state = "main_menu"
                
        else:
            if back_img != back_u:
                back_img = back_u
                if m_player.hitbox.colliderect(back_rect.topleft[0]+8,back_rect.topleft[1]+8+16,back_rect.topright[0]-back_rect.topleft[0]-16,back_rect.bottomleft[1]-back_rect.topleft[1]-32):
                    m_player.pos.y -= 16

        back_group = [back_rect,back_img,back_u,back_d]

    elif game_state == "playing":
        if game_paused:
            pygame.draw.rect(display,black,pygame.Rect(0,0,d_width,d_height))
            paused_txt.draw("Paused")

        else:
            if camera.c_draw(player,moves,level_group,mx,my,enemy_group,spawner_group,collectable_group,bullet_group,footprint_group):
                level += 1
                prev_score = player.score
                prev_bullets = player.bullets
                prev_cash = player.cash
                #prev_kills = player.kills
                player.energyval = player.energymax
                
                if level > 2:
                    game_state = "win_screen"
                else:
                    for t in level_group:
                        t.kill()
                    level_group.empty()
                    bullet_group.empty()
                    enemy_group.empty()
                    spawner_group.empty()
                    footprint_group.empty()
                    collectable_group.empty()
                    camera.empty()

                    player.pos = pygame.math.Vector2((200*sprite_scale,200*sprite_scale))
                    load_level(level_group)
                    load_sprites(enemy_group,spawner_group)

            if player.die():
                player.score = prev_score - 100
                player.health = player.healthmax
                player.energyval = player.energymax
                player.bullets = prev_bullets
                #player.kills = prev_kills
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
                camera.empty()

                player.pos = pygame.math.Vector2((200*sprite_scale,200*sprite_scale))
                load_level(level_group)
                load_sprites(enemy_group,spawner_group)
            
            if game_stats:
                fpslabel.draw("FPS:"+str(int(fps))+"(max"+str(ogframerate)+")")
                
            score_txt.draw("Score: "+str(player.score))
            cash_txt.draw(str(player.cash))
            ammo_txt.draw(str(player.bullets))
            display.blit(cn,cash_rect)
            display.blit(amo,ammo_rect)
            
            if player.lives == 0:
                game_state = "game_over"
                
    elif game_state == "game_over":
        game_over_txt.draw("Game Over")
        f_score_txt.draw("Score: "+str(player.score))
        kills_txt.draw("Kills: "+str(player.kills))

    elif game_state == "win_screen":
        win_txt.draw("You Win!!")
        f_score_txt.draw("Score: "+str(player.score))
        kills_txt.draw("Kills: "+str(player.kills))
    
    pygame.display.update()
    
pygame.quit()
sys.exit()
