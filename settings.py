import pygame, math
from pygame.locals import *
# from camera import *
# import os

# pygame.init()

#get data of the monitor being used
computer = pygame.display.Info()

#display resolution variables
d_width = computer.current_w#1536
d_height = computer.current_h#864

#sets the disply resolution
display = pygame.display.set_mode((d_width, d_height), FULLSCREEN)#(d_width+2, d_height+2), RESIZABLE)
# print(display)
# pygame.display.toggle_fullscreen()
#display name
pygame.display.set_caption('Portal Dungeon')

#colours
red = 255, 0, 0
dark_red = 128, 0, 0
green = 0, 200, 0
dark_green = 0, 128, 0
blue = 0, 0, 255
dark_blue = 0, 0, 128
orange = 240, 130, 35
white = 255, 255, 255
yellow = 255, 255, 0
black = 0, 0, 0
grey = 88, 88, 88

#useful numbers (might remove if not used for different moving methods)
root_2 = math.sqrt(2)

#settings level variables
lvl_dir = "levels/"
levels = {
    lvl_0 := lvl_dir+"level_1.txt", 
    lvl_1 := lvl_dir+"level_2.txt", 
}



#loading all the images
img_dir = "images/"#directories for correct path

misc_dir = img_dir + "misc/"
misc_imgs = {
    title_img := pygame.image.load(misc_dir+"title.png").convert_alpha(), 
    ctrls_img := pygame.transform.scale(pygame.image.load(misc_dir+"control_menu.png").convert_alpha(), (d_width, d_height-128)), 
    hrt := pygame.image.load(misc_dir+"heart.png").convert_alpha(), 
    fist_show := pygame.image.load(misc_dir+"fist_show.png").convert_alpha(), 
    gun_show := pygame.image.load(misc_dir+"gun_show.png").convert_alpha(), 
    #white_ovly := pygame.transform.scale(pygame.image.load(img_dir+misc_dir+"white_overlay.png").convert_alpha(64), (d_width, d_height)), 
}

w_show = [fist_show, gun_show]

til_dir = img_dir + "tiles/"
tile_imgs = {
    grass := pygame.image.load(til_dir+"grass.png").convert_alpha(), 
    wall := pygame.image.load(til_dir+"wall.png").convert_alpha(), 
    tree := pygame.image.load(til_dir+"tree.png").convert_alpha(), 
    portal := pygame.image.load(til_dir+"portal.png").convert_alpha(), 
    b_portal := pygame.image.load(til_dir+"big_portal.png").convert_alpha(), 
    mud := pygame.image.load(til_dir+"mud.png").convert_alpha(), 
    snowy_grass := pygame.image.load(til_dir+"snowy_grass.png").convert_alpha(), 
    flower_grass := pygame.image.load(til_dir+"flower_grass.png").convert_alpha(), 
}
plr_dir = img_dir + "player/"
player_imgs = {
    plrhd := pygame.image.load(plr_dir+"playerHead.png").convert_alpha(), 
    plrrm := pygame.image.load(plr_dir+"playerArms.png").convert_alpha(), 
}
enm_dir = img_dir + "enemies/"
gst_dir = enm_dir + "ghost/"
enemy_imgs = {
    zmbhd := pygame.image.load(enm_dir+"zombieHead.png").convert_alpha(), 
    zmbrm := pygame.image.load(enm_dir+"zombieArms.png").convert_alpha(), 
    sklhd := pygame.image.load(enm_dir+"skeletonHead.png").convert_alpha(), 
    sklrm := pygame.image.load(enm_dir+"skeletonArms.png").convert_alpha(), 
    gsthdV := pygame.image.load(gst_dir+"ghostHeadV.png").convert_alpha(), 
    gstrmV := pygame.image.load(gst_dir+"ghostArmsV.png").convert_alpha(), 
    gsttlV_1 := pygame.image.load(gst_dir+"ghostTailV_1.png").convert_alpha(), 
    gsttlV_2 := pygame.image.load(gst_dir+"ghostTailV_2.png").convert_alpha(), 
    gsttlV_3 := pygame.image.load(gst_dir+"ghostTailV_3.png").convert_alpha(), 
    gsttlV_4 := pygame.image.load(gst_dir+"ghostTailV_4.png").convert_alpha(), 
    gsttlV_5 := pygame.image.load(gst_dir+"ghostTailV_5.png").convert_alpha(), 
    gsttlV_6 := pygame.image.load(gst_dir+"ghostTailV_6.png").convert_alpha(), 
    gsttlV_7 := pygame.image.load(gst_dir+"ghostTailV_7.png").convert_alpha(), 
    gsttlV_8 := pygame.image.load(gst_dir+"ghostTailV_8.png").convert_alpha(), 
}#possibly add ghost dissaperaing every now and then

#ghosts animation group
gsttlAnim = (gsttlV_1, gsttlV_2, gsttlV_3, gsttlV_4, gsttlV_5, gsttlV_6, gsttlV_7, gsttlV_8)

spwn_dir = img_dir + "spawners/"
spawner_imgs = {
    grvstn := pygame.image.load(spwn_dir+"grave.png").convert_alpha(), 
}
ptcl_dir = img_dir + "particles/"
particle_imgs = {
    snow_footprints := pygame.image.load(ptcl_dir+"snow_footprints.png").convert_alpha(), 
    mud_footprints := pygame.image.load(ptcl_dir+"mud_footprints.png").convert_alpha(), 
    blt := pygame.image.load(ptcl_dir+"bullet.png").convert_alpha(), 
}
col_dir = img_dir + "collectables/"
collectable_imgs = {
    cn := pygame.image.load(col_dir+"coin.png").convert_alpha(), 
    amo := pygame.image.load(col_dir+"ammo.png").convert_alpha(), 
}
btn_dir = img_dir + "buttons/"
button_imgs = {
    play_u := pygame.image.load(btn_dir+"play_up.png").convert_alpha(), 
    play_d := pygame.image.load(btn_dir+"play_down.png").convert_alpha(), 
    quit_u := pygame.image.load(btn_dir+"quit_up.png").convert_alpha(), 
    quit_d := pygame.image.load(btn_dir+"quit_down.png").convert_alpha(), 
    ctrl_u := pygame.image.load(btn_dir+"control_up.png").convert_alpha(), 
    ctrl_d := pygame.image.load(btn_dir+"control_down.png").convert_alpha(), 
    back_u := pygame.image.load(btn_dir+"back_up.png").convert_alpha(), 
    back_d := pygame.image.load(btn_dir+"back_down.png").convert_alpha(), 
    main_u := pygame.image.load(btn_dir+"main_up.png").convert_alpha(), 
    main_d := pygame.image.load(btn_dir+"main_down.png").convert_alpha(), 
    yes_u := pygame.image.load(btn_dir+"yes_up.png").convert_alpha(), 
    yes_d := pygame.image.load(btn_dir+"yes_down.png").convert_alpha(), 
    no_u := pygame.image.load(btn_dir+"no_up.png").convert_alpha(), 
    no_d := pygame.image.load(btn_dir+"no_down.png").convert_alpha(), 
    rtry_u := pygame.image.load(btn_dir+"retry_up.png").convert_alpha(), 
    rtry_d := pygame.image.load(btn_dir+"retry_down.png").convert_alpha(), 
    cont_u := pygame.image.load(btn_dir+"continue_up.png").convert_alpha(), 
    cont_d := pygame.image.load(btn_dir+"continue_down.png").convert_alpha(), 
    rspn_u := pygame.image.load(btn_dir+"respawn_up.png").convert_alpha(), 
    rspn_d := pygame.image.load(btn_dir+"respawn_down.png").convert_alpha(), 
}
int_dir = img_dir + "interactables/"
interactable_imgs = {
    wood_closed := pygame.image.load(int_dir+"wood_chest_closed.png").convert_alpha(), 
    wood_open := pygame.image.load(int_dir+"wood_chest_open.png").convert_alpha(), 
    iron_closed := pygame.image.load(int_dir+"iron_chest_closed.png").convert_alpha(), 
    iron_open := pygame.image.load(int_dir+"iron_chest_open.png").convert_alpha(), 
    gold_closed := pygame.image.load(int_dir+"gold_chest_closed.png").convert_alpha(), 
    gold_open := pygame.image.load(int_dir+"gold_chest_open.png").convert_alpha(), 
    # door_anticlock_right := pygame.image.load(img_dir+int_dir+"door_anticlockwise_right.png").convert_alpha(), 
    # door_clock_up := pygame.image.load(img_dir+int_dir+"door_clockwise_up.png").convert_alpha(), 
    # door_clock_left := pygame.image.load(img_dir+int_dir+"door_clockwise_left.png").convert_alpha(), 
    # door_anticlock_up := pygame.image.load(img_dir+int_dir+"door_anticlockwise_up.png").convert_alpha(), 
    # door_clock_right := pygame.image.load(img_dir+int_dir+"door_clockwise_right.png").convert_alpha(), 
    # door_anticlock_down := pygame.image.load(img_dir+int_dir+"door_anticlockwise_down.png").convert_alpha(), 
    # door_clock_down := pygame.image.load(img_dir+int_dir+"door_clockwise_down.png").convert_alpha(), 
    # door_anticlock_left := pygame.image.load(img_dir+int_dir+"door_anticlockwise_left.png").convert_alpha(), 
    wood_door := pygame.image.load(int_dir+"wood_door.png").convert_alpha(),
}
wpn_dir = img_dir + "weapons/"
weapon_imgs = {
    pistol := pygame.image.load(wpn_dir+"pistol.png").convert_alpha(),
}

#icon
pygame.display.set_icon(portal)

#image scaling(not needed)
aspect_ratio = d_width / d_width

entity_x_scale = aspect_ratio * 18
entity_y_scale = aspect_ratio * 18

sprite_scale = 1
tile_size = 48
tile_scale = sprite_scale * tile_size
# for attribute, value in tile_size.__setattr__():
#     print(attribute + f' = {value}')
# #key presses
# up_pressed = False
# down_pressed = False
# left_pressed = False
# right_pressed = False
# dash_pressed = False
# attack_pressed = False
# weapon_swap_pressed = False
# game_stats = False
# game_paused = False
# use = False
# click = False

# game_state = "main_menu"

# sim_dist = 800
# render_dist = (((d_width/2)**2 + (d_height/2)**2)**0.5) + (48*sprite_scale)
# camera = Camera(render_dist, sim_dist)

player_count = 0
timer = 0

# ok = 4
# def change_it(ok):
#     ok -= 2
#     return ok
# print(ok)
# ok = change_it(ok)
# print(ok)

# for num in range(1,4):
#     print(num)

# my_string = "yes\nno"
# split_string = my_string.split('\n')
# print(split_string[0])
# print(split_string[1])

# print(None)

# class new_string(str):
#     def __init__(self, object: object = ...):
#         # super(type).__init__()
#         super().__init__()
        
# class new_string(str):
#     def __init__(self, string:str=..., x=0):
#         pass
#         # super(type).__init__()
#         str.__init__(string)
# # me = type("yes")
# # print(me)
# my_new_string = new_string("no", 100)
# print(my_new_string)
# my_new_string += "yes"
# print(my_new_string)
# my_list = [2]
# print(my_list)
# my_list += [1]
# print(my_list)
# my_string = "no"
# print(my_string[0])

# class new_list(list):
#     def __init__(self):
#         super().__init__()

# my_new_list = new_list([2])
# print(my_new_list)
# my_list = list([1])
# print(my_list)

# my_list = []
# my_list += "yes"
# print(my_list)

# ns = []
# current_x = 481
# xvel = -4
# for n in range(int((current_x + xvel)/tile_scale), int(current_x/tile_scale)+1):
#     ns.append(n)

# print(int(current_x/tile_scale), ns)

