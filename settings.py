import pygame
from pygame.locals import *
from camera import *

pygame.init()

#get data of the monitor being used
computer = pygame.display.Info()

#display resolution variables
d_width = 1200#computer.current_w
d_height = 800#computer.current_h

#sets the disply resolution
display = pygame.display.set_mode((d_width, d_height),FULLSCREEN)

#display name
pygame.display.set_caption('Portal Dungeon')

#colours
red = 255,0,0
dark_red = 128,0,0
green = 0,200,0
dark_green = 0,128,0
blue = 0,0,255
dark_blue = 0,0,128
orange = 240,130,35
white = 255,255,255
yellow = 255,255,0
black = 0,0,0
grey = 88,88,88

#settings level variables
lvl_dir = "levels/"
levels = {
    lvl_0 := lvl_dir+"level_1.txt",
    lvl_1 := lvl_dir+"level_2.txt",
}

#loading all the images
img_dir = "images/"#directories for correct path

misc_dir = "misc/"
misc = {
    title_img := pygame.image.load(img_dir+misc_dir+"title.png").convert_alpha(),
    ctrls_img := pygame.transform.scale(pygame.image.load(img_dir+misc_dir+"control_menu.png").convert_alpha(),(d_width,d_height-128)),
    hrt := pygame.image.load(img_dir+misc_dir+"heart.png").convert_alpha(),
    fist_show := pygame.image.load(img_dir+misc_dir+"fist_show.png").convert_alpha(),
    gun_show := pygame.image.load(img_dir+misc_dir+"gun_show.png").convert_alpha(),
}

w_show = [fist_show,gun_show]

til_dir = "tiles/"
tiles = {
    grass := pygame.image.load(img_dir+til_dir+"grass.png").convert_alpha(),
    wall := pygame.image.load(img_dir+til_dir+"wall.png").convert_alpha(),
    tree := pygame.image.load(img_dir+til_dir+"tree.png").convert_alpha(),
    portal := pygame.image.load(img_dir+til_dir+"portal.png").convert_alpha(),
    b_portal := pygame.image.load(img_dir+til_dir+"big_portal.png").convert_alpha(),
    mud := pygame.image.load(img_dir+til_dir+"mud.png").convert_alpha(),
    snowy_grass := pygame.image.load(img_dir+til_dir+"snowy_grass.png").convert_alpha(),
    flower_grass := pygame.image.load(img_dir+til_dir+"flower_grass.png").convert_alpha(),
}
plr_dir = "player/"
players = {
    plrhd := pygame.image.load(img_dir+plr_dir+"playerHead.png").convert_alpha(),
    plrrm := pygame.image.load(img_dir+plr_dir+"playerArms.png").convert_alpha(),
}
enm_dir = "enemies/"
gst_dir = "ghost/"
enemies = {
    zmbhd := pygame.image.load(img_dir+enm_dir+"zombieHead.png").convert_alpha(),
    zmbrm := pygame.image.load(img_dir+enm_dir+"zombieArms.png").convert_alpha(),
    sklhd := pygame.image.load(img_dir+enm_dir+"skeletonHead.png").convert_alpha(),
    sklrm := pygame.image.load(img_dir+enm_dir+"skeletonArms.png").convert_alpha(),
    gsthdV := pygame.image.load(img_dir+enm_dir+gst_dir+"ghostHeadV.png").convert_alpha(),
    gstrmV := pygame.image.load(img_dir+enm_dir+gst_dir+"ghostArmsV.png").convert_alpha(),
    gsttlV_1 := pygame.image.load(img_dir+enm_dir+gst_dir+"ghostTailV_1.png").convert_alpha(),
    gsttlV_2 := pygame.image.load(img_dir+enm_dir+gst_dir+"ghostTailV_2.png").convert_alpha(),
    gsttlV_3 := pygame.image.load(img_dir+enm_dir+gst_dir+"ghostTailV_3.png").convert_alpha(),
    gsttlV_4 := pygame.image.load(img_dir+enm_dir+gst_dir+"ghostTailV_4.png").convert_alpha(),
    gsttlV_5 := pygame.image.load(img_dir+enm_dir+gst_dir+"ghostTailV_5.png").convert_alpha(),
    gsttlV_6 := pygame.image.load(img_dir+enm_dir+gst_dir+"ghostTailV_6.png").convert_alpha(),
    gsttlV_7 := pygame.image.load(img_dir+enm_dir+gst_dir+"ghostTailV_7.png").convert_alpha(),
    gsttlV_8 := pygame.image.load(img_dir+enm_dir+gst_dir+"ghostTailV_8.png").convert_alpha(),
}#possibly add ghost dissaperaing every now and then

#ghosts animation group
gsttlAnim = (gsttlV_1,gsttlV_2,gsttlV_3,gsttlV_4,gsttlV_5,gsttlV_6,gsttlV_7,gsttlV_8)

spwn_dir = "spawners/"
spawners = {
    grvstn := pygame.image.load(img_dir+spwn_dir+"grave.png").convert_alpha(),
}
ptcl_dir = "particles/"
partciles = {
    snow_footprints := pygame.image.load(img_dir+ptcl_dir+"snow_footprints.png").convert_alpha(),
    mud_footprints := pygame.image.load(img_dir+ptcl_dir+"mud_footprints.png").convert_alpha(),
    blt := pygame.image.load(img_dir+ptcl_dir+"bullet.png").convert_alpha(),
}
col_dir = "collectables/"
collectables = {
    cn := pygame.image.load(img_dir+col_dir+"coin.png").convert_alpha(),
    amo := pygame.image.load(img_dir+col_dir+"ammo.png").convert_alpha(),
}
btn_dir = "buttons/"
buttons = {
    play_u := pygame.image.load(img_dir+btn_dir+"play_up.png").convert_alpha(),
    play_d := pygame.image.load(img_dir+btn_dir+"play_down.png").convert_alpha(),
    quit_u := pygame.image.load(img_dir+btn_dir+"quit_up.png").convert_alpha(),
    quit_d := pygame.image.load(img_dir+btn_dir+"quit_down.png").convert_alpha(),
    ctrl_u := pygame.image.load(img_dir+btn_dir+"control_up.png").convert_alpha(),
    ctrl_d := pygame.image.load(img_dir+btn_dir+"control_down.png").convert_alpha(),
    back_u := pygame.image.load(img_dir+btn_dir+"back_up.png").convert_alpha(),
    back_d := pygame.image.load(img_dir+btn_dir+"back_down.png").convert_alpha(),
}

#image scaling(not needed)
aspect_ratio = d_width / d_width

entity_x_scale = aspect_ratio * 18
entity_y_scale = aspect_ratio * 18

sprite_scale = 1

tile_scale = sprite_scale * 48

#key presses
up_pressed = False
down_pressed = False
left_pressed = False
right_pressed = False
dash_pressed = False
attack_pressed = False
weapon_swap_pressed = False
game_stats = False
game_paused = False
game_state = "main_menu"

sim_dist = 800
render_dist = (((d_width/2)**2 + (d_height/2)**2)**0.5) + (48*sprite_scale)
camera = camera(render_dist,sim_dist)
