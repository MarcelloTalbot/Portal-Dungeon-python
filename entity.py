import math,random#pygame,math,random
from textbox import *
from settings import *
#from pygame.locals import *

#objects (all sprites)
class Object(pygame.sprite.DirtySprite):
    def __init__(self,x,y,display,image):#I may not need image,arm,tail as args
        super().__init__()
        self.type = "object"
        self.display = display
        pygame.sprite.DirtySprite.__init__(self)
        self.pos = pygame.math.Vector2((x,y))
        self.solid = True
        self.health = 10
        self.healthmax = 10
        self.xvel = 4
        self.yvel = 4
        self.vel = 4
        self.z = 3
        self.image = image
        self.scal_image = pygame.transform.scale(self.image,(sprite_scale*18,sprite_scale*18))
        self.rot_image = self.scal_image
        self.rect = self.rot_image.get_rect(center = (round(self.pos.x),round(self.pos.y)))
        self.hitbox = self.scal_image.get_rect(center = (round(self.pos.x),round(self.pos.y)))

    def die(self,p,c_group):
        if self.health <= 0:
            p.score += self.healthmax
            for n in range(0,(self.healthmax//2 - random.randint(0,self.healthmax//4))):
                x = (self.hitbox.topleft[0] + random.randint(0,(self.hitbox.topright[0]-self.hitbox.topleft[0])))
                y = (self.hitbox.topleft[1] + random.randint(0,(self.hitbox.bottomleft[1]-self.hitbox.topleft[1])))
                num = random.randint(0,30)
                if num == 30:
                    self.create_ammo(x,y,c_group)
                else:
                    self.create_coin(x,y,c_group)
            p.kills += 1
            self.kill()
            
    def create_coin(self,x,y,c_group):
        coin = Coin(x,y,self.display,cn,1)
        c_group.add(coin)
        camera.add(coin)

    def create_ammo(self,x,y,c_group):
        ammo = Ammo(x,y,self.display,amo,30)
        c_group.add(ammo)
        camera.add(ammo)

    def sync(self):
        self.pos.x += (self.xvel * sprite_scale)
        self.pos.y += (self.yvel * sprite_scale)
        self.hitbox.center = self.pos.x, self.pos.y
        self.rect.center = self.pos.x, self.pos.y
        
#entities(moving sprites)
class Entity(Object):
    def __init__(self,x,y,display,image,arm):
        super().__init__(x,y,display,image)
        self.type = "entity"
        self.arm = arm
        self.scal_arm = pygame.transform.scale(self.arm,(sprite_scale*30,sprite_scale*30))
        self.rot_arm = self.scal_arm
        self.arm_rect = self.scal_arm.get_rect(center = (round(self.pos.x),round(self.pos.y)))

    def die(self,p,c_group,s_group):
        super().die(p,c_group)

    def create_coin(self,x,y,c_group):
        super().create_coin(x,y,c_group)

    def create_ammo(self,x,y,c_group):
        super().create_ammo(x,y,c_group)

    def sync(self):
        super().sync()
        self.arm_rect.center = self.pos.x,self.pos.y

#enemy spawners(factories)
#class spawner(object):
#    def __init__(self,x,y,display,image,s_type):
#        super().__init__(x,y,display,image)
#        self.health = 50
#        self.s_type = s_type
#        self.spawn_timer = 0

    #def create_enemy(self):
    #    self.spawn_timer += 1
    #    if self.spawn_timer >= 300:
    #        exec("%s = %d" % (self.s_type,self.s_type(self.pos.x,self.pos.y,display,)


#zombie + skeleton spawner
class Grave(Object):#spawner):
    def __init__(self,x,y,display,image,num):#,s_type):
        super().__init__(x,y,display,image)
        self.scal_image = pygame.transform.scale(self.image,(sprite_scale*48,sprite_scale*64))
        self.rot_image = self.scal_image
        self.rect = self.rot_image.get_rect(center = (round(self.pos.x),round(self.pos.y)))
        self.hitbox = self.scal_image.get_rect(center = (round(self.pos.x),round(self.pos.y)))
        #self.s_type = s_type
        self.health = 50
        self.healthmax = 50
        self.spawn_timer = 0
        self.e_count = 0
        self.e_count_max = 20
        self.s_spawn = False
        self.num = num
        self.type = "spawner"

    def update(self,group,p,c_group,offset):
        self.die(p,c_group)
        self.create(group)
        #self.render()
        self.render_bars(offset)

    def create_coin(self,x,y,c_group):
        super().create_coin(x,y,c_group)

    def create_ammo(self,x,y,c_group):
        super().create_ammo(x,y,c_group)

    def die(self,p,c_group):
        super().die(p,c_group)

    def create(self,group):
        self.spawn_timer += 1
        if self.spawn_timer >= 300 and self.e_count < self.e_count_max:
            spawn_list = [self.create_zombie, self.create_skeleton]
            random.choice(spawn_list)(group)#randomly chooses which function to perform
            self.e_count += 1
            self.spawn_timer = 0

    def create_zombie(self,group):
        zombie = Zombie(self.pos.x,self.pos.y,self.display,zmbhd,zmbrm,True,self.num)
        group.add(zombie)
        camera.add(zombie)

    def create_skeleton(self,group):
        skeleton = Skeleton(self.pos.x,self.pos.y,self.display,sklhd,sklrm,True,self.num)
        group.add(skeleton)
        camera.add(skeleton)

    def render_bars(self,offset):
        #progress rectangle stats
        hpbar_p_left = offset[0] - 3
        hpbar_p_top = offset[1] - 10
        hpbar_p_width = 50*(self.health/self.healthmax)
        hpbar_p_height = 6

        #border rectangle stats
        hpbar_b_left = hpbar_p_left - 2
        hpbar_b_top = hpbar_p_top - 2
        hpbar_b_width = 54
        hpbar_b_height = hpbar_p_height + 4

        #hp bar
        pygame.draw.rect(self.display,dark_red,pygame.Rect(hpbar_b_left,hpbar_b_top,hpbar_b_width,hpbar_b_height))
        pygame.draw.rect(self.display,red,pygame.Rect(hpbar_p_left,hpbar_p_top,hpbar_p_width,hpbar_p_height))

    def render(self):
        self.render_bars()
        self.display.blit(self.rot_image,self.rect)
                           
#enemies
class Enemy(Entity):
    def __init__(self,x,y,display,image,arm):
        super().__init__(x,y,display,image,arm)
        self.sight = 700 * sprite_scale
        self.idle_xvel = 1
        self.idle_yvel = 1
        self.xvel = 3
        self.yvel = 3
        self.idle = True

    def sync(self):
        super().sync()

    def die(self,p,c_group,s_group):
        super().die(p,c_group,s_group)
        #if self.s_spawn:
        #    s_group[self.s_num].e_count -= 1

    def create_coin(self,x,y,c_group):
        super().create_coin(x,y,c_group)

    def create_ammo(self,x,y,c_group):
        super().create_ammo(x,y,c_group)

    def idle_sync(self):
        self.pos.x += (self.idle_xvel * sprite_scale)
        self.pos.y += (self.idle_yvel * sprite_scale)
        self.hitbox.center = self.pos.x,self.pos.y
        self.rect.center = self.pos.x,self.pos.y
        self.arm_rect.center = self.pos.x,self.pos.y

    def tile_collisions(self,tiles):#not done abs() on mud + snow
        for t in tiles:
            #collision of impassible tiles
            if t.t_type == "wall" or t.t_type == "tree":#split normal and idle to functions
                #x axis collisions
                if t.rect.colliderect(self.hitbox.topleft[0] + (self.xvel * sprite_scale * 1.1),self.hitbox.topleft[1],self.hitbox.topright[0]-self.hitbox.topleft[0],self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                    if self.xvel > 0:
                        self.xvel = t.rect.left - self.hitbox.left
                        self.xvel = 0
                    elif self.xvel < 0:
                        self.xvel = self.hitbox.right - t.rect.right
                        self.xvel = 0
                if t.rect.colliderect(self.hitbox.topleft[0] + (self.idle_xvel * sprite_scale * 1.1),self.hitbox.topleft[1],self.hitbox.topright[0]-self.hitbox.topleft[0],self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                    if self.idle_xvel > 0:
                        self.idle_xvel = t.rect.left - self.hitbox.left
                        self.idle_xvel = 0
                    elif self.idle_xvel < 0:
                        self.idle_xvel = self.hitbox.right - t.rect.right
                        self.idle_xvel = 0
                #y axis collisions
                if t.rect.colliderect(self.hitbox.topleft[0],self.hitbox.topleft[1] + (self.yvel * sprite_scale * 1.1),self.hitbox.topright[0]-self.hitbox.topleft[0],self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                    if self.yvel < 0:
                        self.yvel = self.hitbox.bottom - t.rect.bottom
                        self.yvel = 0
                    elif self.yvel > 0:
                        self.yvel = t.rect.top - self.hitbox.top
                        self.yvel = 0
                if t.rect.colliderect(self.hitbox.topleft[0],self.hitbox.topleft[1] + (self.idle_yvel * sprite_scale * 1.1),self.hitbox.topright[0]-self.hitbox.topleft[0],self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                    if self.idle_yvel < 0:
                        self.idle_yvel = self.hitbox.bottom - t.rect.bottom
                        self.idle_yvel = 0
                    elif self.idle_yvel > 0:
                        self.idle_yvel = t.rect.top - self.hitbox.top
                        self.idle_yvel = 0
            #collision of mud
            elif t.t_type == "mud":
                if t.rect.colliderect(self.hitbox):
                    #reduces speed when on mud
                    if self.xvel != 0:
                        self.xvel = self.xvel / 2
                    if self.yvel != 0:
                        self.yvel = self.yvel / 2
                    if self.idle_xvel != 0:
                        self.idle_xvel = self.idle_xvel / 2
                    if self.idle_yvel != 0:
                        self.idle_yvel = self.idle_yvel / 2
                    #makes sure the speed doesn't decrease multiple times when overlapping tiles
                    if self.xvel < 1.5 and self.xvel > 0:
                        self.xvel = 1.5
                    elif self.xvel < 0 and self.xvel > -1.5:
                        self.xvel = -1.5
                    if self.yvel < 1.5 and self.yvel > 0:
                        self.yvel = 1.5
                    elif self.yvel < 0 and self.yvel > -1.5:
                        self.yvel = -1.5
                    if self.idle_xvel < 0.5 and self.idle_xvel > 0:
                        self.idle_xvel = 0.5
                    elif self.idle_xvel < 0 and self.idle_xvel > -0.5:
                        self.idle_xvel = -0.5
                    if self.idle_yvel < 0.5 and self.idle_yvel > 0:
                        self.idle_yvel = 0.5
                    elif self.idle_yvel < 0 and self.idle_yvel > -0.5:
                        self.idle_yvel = -0.5
            #collision of snow
            elif t.t_type == "snowy_grass":
                if t.rect.colliderect(self.hitbox):
                    #reduces speed when on snow
                    if self.xvel != 0:
                        self.xvel = self.xvel / 1.5
                    if self.yvel != 0:
                        self.yvel = self.yvel / 1.5
                    if self.idle_xvel != 0:
                        self.idle_xvel = self.idle_xvel / 1.5
                    if self.idle_yvel != 0:
                        self.idle_yvel = self.idle_yvel / 1.5
                    #makes sure the speed doesn't decrease multiple times when overlapping tiles
                    if self.xvel < 2 and self.xvel > 0:
                        self.xvel = 2
                    elif self.xvel < 0 and self.xvel > -2:
                        self.xvel = -2
                    if self.yvel < 2 and self.yvel > 0:
                        self.yvel = 2
                    elif self.yvel < 0 and self.yvel > -2:
                        self.yvel = -2
                    if self.idle_xvel < (2/3) and self.idle_xvel > 0:
                        self.idle_xvel = (2/3)
                    elif self.idle_xvel < 0 and self.idle_xvel > -(2/3):
                        self.idle_xvel = -(2/3)
                    if self.idle_yvel < (2/3) and self.idle_yvel > 0:
                        self.idle_yvel = (2/3)
                    elif self.idle_yvel < 0 and self.idle_yvel > -(2/3):
                        self.idle_yvel = -(2/3)
                
    def door_collisions(self,i_group):
        for d in i_group:
            #collision of doors
            if d.type == "door":#split normal and idle to functions
                #x axis collisions
                if d.rect.colliderect(self.hitbox.topleft[0] + (self.xvel * sprite_scale * 1.1),self.hitbox.topleft[1],self.hitbox.topright[0]-self.hitbox.topleft[0],self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                    if self.xvel > 0:
                        self.xvel = d.rect.left - self.hitbox.left
                        self.xvel = 0
                    elif self.xvel < 0:
                        self.xvel = self.hitbox.right - d.rect.right
                        self.xvel = 0
                if d.rect.colliderect(self.hitbox.topleft[0] + (self.idle_xvel * sprite_scale * 1.1),self.hitbox.topleft[1],self.hitbox.topright[0]-self.hitbox.topleft[0],self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                    if self.idle_xvel > 0:
                        self.idle_xvel = d.rect.left - self.hitbox.left
                        self.idle_xvel = 0
                    elif self.idle_xvel < 0:
                        self.idle_xvel = self.hitbox.right - d.rect.right
                        self.idle_xvel = 0
                #y axis collisions
                if d.rect.colliderect(self.hitbox.topleft[0],self.hitbox.topleft[1] + (self.yvel * sprite_scale * 1.1),self.hitbox.topright[0]-self.hitbox.topleft[0],self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                    if self.yvel < 0:
                        self.yvel = self.hitbox.bottom - d.rect.bottom
                        self.yvel = 0
                    elif self.yvel > 0:
                        self.yvel = d.rect.top - self.hitbox.top
                        self.yvel = 0
                if d.rect.colliderect(self.hitbox.topleft[0],self.hitbox.topleft[1] + (self.idle_yvel * sprite_scale * 1.1),self.hitbox.topright[0]-self.hitbox.topleft[0],self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                    if self.idle_yvel < 0:
                        self.idle_yvel = self.hitbox.bottom - d.rect.bottom
                        self.idle_yvel = 0
                    elif self.idle_yvel > 0:
                        self.idle_yvel = d.rect.top - self.hitbox.top
                        self.idle_yvel = 0
                        
    def enemy_collision(self,enemies):#not done yet
        for e in enemies.sprites():
            if e.pos != self.pos and e.solid == True:
                if e.hitbox.colliderect(self.hitbox.topleft[0] + self.xvel,self.hitbox.topleft[1],self.hitbox.topright[0]-self.hitbox.topleft[0],self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                    if self.xvel > 0:
                        if e.xvel == 0:
                            self.xvel = e.hitbox.left - self.hitbox.left
                            self.xvel = 0
                        elif e.xvel != 0:
                            self.xvel = e.hitbox.left - self.hitbox.left
                            self.xvel = e.xvel
                    elif self.xvel < 0:
                        if e.xvel == 0:
                            self.xvel = self.hitbox.right - e.hitbox.right
                            self.xvel = 0
                        elif e.xvel != 0:
                            self.xvel = self.hitbox.right - e.hitbox.right
                            self.xvel = e.xvel
                if e.hitbox.colliderect(self.hitbox.topleft[0] + self.idle_xvel,self.hitbox.topleft[1],self.hitbox.topright[0]-self.hitbox.topleft[0],self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                    if self.idle_xvel > 0:
                        if e.xvel == 0:
                            self.idle_xvel = e.hitbox.left - self.hitbox.left
                            self.idle_xvel = 0
                        elif e.xvel != 0:
                            self.idle_xvel = e.hitbox.left - self.hitbox.left
                            self.idle_xvel = e.xvel
                    elif self.idle_xvel < 0:
                        if e.xvel == 0:
                            self.idle_xvel = self.hitbox.right - e.hitbox.right
                            self.idle_xvel = 0
                        elif e.xvel != 0:
                            self.idle_xvel = self.hitbox.right - e.hitbox.right
                            self.idle_xvel = e.xvel
                #y axis collisions
                if e.hitbox.colliderect(self.hitbox.topleft[0],self.hitbox.topleft[1] + self.yvel,self.hitbox.topright[0]-self.hitbox.topleft[0],self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                    if self.yvel < 0:
                        if e.yvel == 0:
                            self.yvel = self.hitbox.bottom - e.hitbox.bottom
                            self.yvel = 0
                        elif e.yvel != 0:
                            self.yvel = self.hitbox.bottom - e.hitbox.bottom
                            self.yvel = e.yvel
                    elif self.yvel > 0:
                        if e.yvel == 0:
                            self.yvel = e.hitbox.top - self.hitbox.top
                            self.yvel = 0
                        elif e.yvel != 0:
                            self.yvel = e.hitbox.top - self.hitbox.top
                            self.yvel = e.yvel
                if e.hitbox.colliderect(self.hitbox.topleft[0],self.hitbox.topleft[1] + self.idle_yvel,self.hitbox.topright[0]-self.hitbox.topleft[0],self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                    if self.idle_yvel < 0:
                        if e.yvel == 0:
                            self.idle_yvel = self.hitbox.bottom - e.hitbox.bottom
                            self.idle_yvel = 0
                        elif e.yvel != 0:
                            self.idle_yvel = self.hitbox.bottom - e.hitbox.bottom
                            self.idle_yvel = e.yvel
                    elif self.idle_yvel > 0:
                        if e.yvel == 0:
                            self.idle_yvel = e.hitbox.top - self.hitbox.top
                            self.idle_yvel = 0
                        elif e.yvel != 0:
                            self.idle_yvel = e.hitbox.top - self.hitbox.top
                            self.idle_yvel = e.yvel

                self.push(e)

    def player_collision(self,p):#improve (there is a bit of sticking due equalling the speeds)
        if p.hitbox.colliderect(self.hitbox.topleft[0] + self.xvel,self.hitbox.topleft[1],self.hitbox.topright[0]-self.hitbox.topleft[0],self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
            if self.xvel > 0:
                if p.xvel == 0:
                    self.xvel = p.hitbox.left - self.hitbox.left
                    self.xvel = 0
                elif p.xvel != 0:
                    self.xvel = p.hitbox.left - self.hitbox.left
                    self.xvel = p.xvel
            elif self.xvel < 0:
                if p.xvel == 0:
                    self.xvel = self.hitbox.right - p.hitbox.right
                    self.xvel = 0
                elif p.xvel != 0:
                    self.xvel = self.hitbox.right - p.hitbox.right
                    self.xvel = p.xvel
        if p.hitbox.colliderect(self.hitbox.topleft[0] + self.idle_xvel,self.hitbox.topleft[1],self.hitbox.topright[0]-self.hitbox.topleft[0],self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
            if self.idle_xvel > 0:
                if p.xvel == 0:
                    self.idle_xvel = p.hitbox.left - self.hitbox.left
                    self.idle_xvel = 0
                elif p.xvel != 0:
                    self.idle_xvel = p.hitbox.left - self.hitbox.left
                    self.idle_xvel = p.xvel
            elif self.idle_xvel < 0:
                if p.xvel == 0:
                    self.idle_xvel = self.hitbox.right - p.hitbox.right
                    self.idle_xvel = 0
                elif p.xvel != 0:
                    self.idle_xvel = self.hitbox.right - p.hitbox.right
                    self.idle_xvel = p.xvel
        #y axis collisions
        if p.hitbox.colliderect(self.hitbox.topleft[0],self.hitbox.topleft[1] + self.yvel,self.hitbox.topright[0]-self.hitbox.topleft[0],self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
            if self.yvel < 0:
                if p.yvel == 0:
                    self.yvel = self.hitbox.bottom - p.hitbox.bottom
                    self.yvel = 0
                elif p.yvel != 0:
                    self.yvel = self.hitbox.bottom - p.hitbox.bottom
                    self.yvel = p.yvel
            elif self.yvel > 0:
                if p.yvel == 0:
                    self.yvel = p.hitbox.top - self.hitbox.top
                    self.yvel = 0
                elif p.yvel != 0:
                    self.yvel = p.hitbox.top - self.hitbox.top
                    self.yvel = p.yvel
        if p.hitbox.colliderect(self.hitbox.topleft[0],self.hitbox.topleft[1] + self.idle_yvel,self.hitbox.topright[0]-self.hitbox.topleft[0],self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
            if self.idle_yvel < 0:
                if p.yvel == 0:
                    self.idle_yvel = self.hitbox.bottom - p.hitbox.bottom
                    self.idle_yvel = 0
                elif p.yvel != 0:
                    self.idle_yvel = self.hitbox.bottom - p.hitbox.bottom
                    self.idle_yvel = p.yvel
            elif self.idle_yvel > 0:
                if p.yvel == 0:
                    self.idle_yvel = p.hitbox.top - self.hitbox.top
                    self.idle_yvel = 0
                elif p.yvel != 0:
                    self.idle_yvel = p.hitbox.top - self.hitbox.top
                    self.idle_yvel = p.yvel

        self.push(p)

    def push(self,p):
        dist = self.pos.distance_to(p.pos)
        if dist < 12:
            self.yvel += 1
                    
#ghost
class Ghost(Enemy):
    def __init__(self,x,y,display,image,arm,tail,s_spawn,s_num):
        super().__init__(x,y,display,image,arm)
        self.type = "tailed_entity"
        self.anim = tail
        self.tail = self.anim[0]
        self.scal_tail = pygame.transform.scale(self.tail,(sprite_scale*18,sprite_scale*54))
        self.rot_tail = self.scal_tail
        self.tail_rect = self.scal_tail.get_rect(center = (round(self.pos.x),round(self.pos.y)))
        self.xvel = 2
        self.yvel = 2
        self.health = 15
        self.healthmax = 15
        #self.s_spawn = s_spawn
        #self.s_num = s_num
        self.t = random.randint(0,960)
        self.sight = 800 * sprite_scale
        self.anim_t = 0
        self.anim_spd = 0
        self.solid = False
        self.hp_bar_p = pygame.Rect((0,0),(0,0))
        self.hp_bar_b = pygame.Rect((0,0),(0,0))
        self.damage = 10
        self.angle = 0
        self.attack_timer = 0
        self.attack_dist = 20

    def create_coin(self,x,y,c_group):
        super().create_coin(x,y,c_group)

    def create_ammo(self,x,y,c_group):
        super().create_ammo(x,y,c_group)

    def sync(self):
        super().sync()
        self.tail_rect.center = self.pos.x,self.pos.y

    def idle_sync(self):
        super().idle_sync()
        self.tail_rect.center = self.pos.x,self.pos.y

    def tile_collisions(self,tiles):
        for t in tiles:
            if t.t_type == "portal":
                if t.rect_1.colliderect(self.hitbox):
                    self.health -= 1
                elif t.rect_2.colliderect(self.hitbox):
                    self.health -= 1
            elif t.t_type == "b_portal":
                if t.rect.colliderect(self.hitbox):
                    self.health -= 1

    def attack(self,p,dist):
        if dist <= self.attack_dist and not(p.respawn_protection):
            self.attack_timer += 1
            if self.attack_timer >= 45:
                self.attack_timer = 0
                self.angle += 20
                self.rotate()
                p.health -= self.damage

    def timer(self):
        if self.t >= 960:
            self.t = 0
        else:
            self.t += 1

    def tail_anim(self):
        if self.anim_t >= 16:
            self.anim_t = 0
        else:
            self.anim_t += self.anim_spd
            
        if self.anim_t < 2:
            x = 0
        elif self.anim_t < 4 and self.anim_t >= 2:
            x = 1
        elif self.anim_t < 6 and self.anim_t >= 4:
            x = 2
        elif self.anim_t < 8 and self.anim_t >= 6:
            x = 3
        elif self.anim_t < 10 and self.anim_t >= 8:
            x = 4
        elif self.anim_t < 12 and self.anim_t >= 10:
            x = 5
        elif self.anim_t < 14 and self.anim_t >= 12:
            x = 6
        else:
            x = 7

        self.tail = self.anim[x]
        self.scal_tail = pygame.transform.scale(self.tail,(sprite_scale*18,sprite_scale*54))

    def die(self,p,c_group,s_group):
        super().die(p,c_group,s_group)
            
    def update(self,p,tiles,dist,c_group,s_group,offset):
        self.dirty = 1
        self.die(p,c_group,s_group)
        self.timer()
        self.move(p,tiles,dist)
        self.attack(p,dist)
        self.render_bars(offset)
        #self.render()

    def idle_move(self,tiles):
        if self.t <= 120:
            self.angle = 0
            self.idle_xvel = 0
            self.idle_yvel = -1
        elif self.t > 120 and self.t <= 240:
            self.angle = ((self.t-120)/120)*-90
            self.idle_xvel = 0
            self.idle_yvel = 0
            self.rotate()
        elif self.t > 240 and self.t <= 360:
            self.angle = 270
            self.idle_xvel = 1 
            self.idle_yvel = 0
        elif self.t > 360 and self.t <= 480:
            self.angle = ((self.t-240)/120)*-90
            self.idle_xvel = 0
            self.idle_yvel = 0
            self.rotate()
        elif self.t > 480 and self.t <= 600:
            self.angle = 180
            self.idle_xvel = 0
            self.idle_yvel = 1
        elif self.t > 600 and self.t <= 720:
            self.angle = ((self.t-360)/120)*-90
            self.idle_xvel = 0
            self.idle_yvel = 0
            self.rotate()
        elif self.t > 720 and self.t <= 840:
            self.angle = 90
            self.idle_xvel = -1
            self.idle_yvel = 0
        else:
            self.angle = ((self.t-480)/120)*-90
            self.idle_xvel = 0
            self.idle_yvel = 0
            self.rotate()

        self.rotate()

        self.tile_collisions(tiles)

        self.idle_sync()

    def move_to_player(self,p,tiles):#change to a better movement
        if (p.pos.x + 3) >= self.pos.x and (p.pos.x - 3) <= self.pos.x:
            self.xvel = 0
        elif (p.pos.x - 3) > self.pos.x:
            self.xvel = 2
        elif (p.pos.x + 3) < self.pos.x:
            self.xvel = -2
        if (p.pos.y + 3) >= self.pos.y and (p.pos.y - 3) <= self.pos.y:
            self.yvel = 0
        elif (p.pos.y - 3) > self.pos.y:
            self.yvel = 2
        elif (p.pos.y + 3) < self.pos.y:
            self.yvel = -2
        if abs(self.xvel) == 2 and abs(self.yvel) == 2:
            self.xvel = (self.xvel/2)*(2**0.5)
            self.yvel = (self.yvel/2)*(2**0.5)

        self.tile_collisions(tiles)

        self.sync()

    def rotatehead(self):
        self.rot_image = pygame.transform.rotate(self.scal_image,self.angle)
        self.rect = self.rot_image.get_rect(center = self.rect.center)

    def rotatearms(self):
        self.rot_arm = pygame.transform.rotate(self.scal_arm,self.angle)
        self.arm_rect = self.rot_arm.get_rect(center = self.arm_rect.center)

    def rotatetail(self):
        self.rot_tail = pygame.transform.rotate(self.scal_tail,self.angle)
        self.tail_rect = self.rot_tail.get_rect(center = self.tail_rect.center)

    def rotate(self):
        self.rotatehead()
        self.rotatearms()
        self.rotatetail()

    def chase_player(self,p,tiles):
        dx,dy = self.pos.x - p.pos.x, self.pos.y - p.pos.y
        self.angle = math.degrees(math.atan2(dx,dy))
        self.rotate()
        self.move_to_player(p,tiles)

    def move(self,p,tiles,dist):
        #dist = self.pos.distance_to(p.pos)
        if dist <= self.sight:
            self.anim_spd = 1.2
            self.idle = False
            self.chase_player(p,tiles)
        else:
            self.anim_spd = 0.2
            self.idle = True
            self.idle_move(tiles)
        self.tail_anim()

    def render_bars(self,offset):
        #progress rectangle variables
        hpbar_p_left = offset[0] - 9
        hpbar_p_top = offset[1] -10
        hpbar_p_width = 30*(self.health/self.healthmax)
        hpbar_p_height = 6

        #border rectangle variables
        hpbar_b_left = hpbar_p_left - 2
        hpbar_b_top = hpbar_p_top - 2
        hpbar_b_width = 34
        hpbar_b_height = hpbar_p_height + 4

        #hp bar
        pygame.draw.rect(self.display,dark_red,pygame.Rect(hpbar_b_left,hpbar_b_top,hpbar_b_width,hpbar_b_height))
        pygame.draw.rect(self.display,red,pygame.Rect(hpbar_p_left,hpbar_p_top,hpbar_p_width,hpbar_p_height))

    def render(self):
        self.display.blit(self.rot_arm,self.arm_rect)
        self.display.blit(self.rot_tail,self.tail_rect)
        self.display.blit(self.rot_image,self.rect)
        self.render_bars()

#skeleton
class Skeleton(Enemy):
    def __init__(self,x,y,display,image,arm,s_spawn,s_num):#,t,s_spawn,s_num):
        super().__init__(x,y,display,image,arm)
        self.sight = 600 * sprite_scale
        #self.s_spawn = s_spawn
        #self.s_num = s_num
        self.t = random.randint(0,960)
        self.attack_dist = self.sight / 2
        self.attack_timer = 0
        self.angle = 0

    def update(self,p,tiles,dist,c_group,s_group,b_group,e,offset,i_group):
        self.dirty = 1
        self.die(p,c_group,s_group)
        self.move(p,tiles,dist,e,i_group)
        self.attack(p,dist,b_group)
        self.render_bars(offset)
        #self.render()

    def attack(self,p,dist,b_group):
        if dist <= self.attack_dist and not(p.respawn_protection):
            self.attack_timer += 1
            if self.attack_timer >= 20:
                self.attack_timer = 0
                self.create_bullet(b_group)

    def create_coin(self,x,y,c_group):
        super().create_coin(x,y,c_group)

    def create_ammo(self,x,y,c_group):
        super().create_ammo(x,y,c_group)

    def die(self,p,c_group,s_group):
        super().die(p,c_group,s_group)

    def player_collision(self,p):
        super().player_collision(p)

    def enemy_collision(self,e):
        super().enemy_collision(e)

    def sync(self):
        super().sync()

    def idle_sync(self):
        super().idle_sync()

    def tile_collisions(self,tiles):
        super().tile_collisions(tiles)

    def door_collisions(self,i_group):
        super().door_collisions(i_group)

    def idle_move(self,tiles,p,e,i_group):
        if self.t >= 960:
            self.t = 0
        else:
            self.t += 1
        if self.t <= 120:
            self.idle_xvel = 0
            self.idle_yvel = -1
        elif self.t > 120 and self.t <= 240:
            self.angle = ((self.t-120)/120)*-90
            self.idle_xvel = 0
            self.idle_yvel = 0
            self.rotate()
        elif self.t > 240 and self.t <= 360:
            self.idle_xvel = 1 
            self.idle_yvel = 0
        elif self.t > 360 and self.t <= 480:
            self.angle = ((self.t-240)/120)*-90
            self.idle_xvel = 0
            self.idle_yvel = 0
            self.rotate()
        elif self.t > 480 and self.t <= 600:
            self.idle_xvel = 0
            self.idle_yvel = 1
        elif self.t > 600 and self.t <= 720:
            self.angle = ((self.t-360)/120)*-90
            self.idle_xvel = 0
            self.idle_yvel = 0
            self.rotate()
        elif self.t > 720 and self.t <= 840:
            self.idle_xvel = -1
            self.idle_yvel = 0
        else:
            self.angle = ((self.t-480)/120)*-90
            self.idle_xvel = 0
            self.idle_yvel = 0
            self.rotate()

        self.player_collision(p)

        self.enemy_collision(e)

        self.tile_collisions(tiles)

        self.door_collisions(i_group)

        self.idle_sync()

    def move_to_player(self,p,tiles,dist,e,i_group):
        if dist >= 152*sprite_scale:
            if (p.pos.x + 3) >= self.pos.x and (p.pos.x - 3) <= self.pos.x:
                self.xvel = 0
            elif (p.pos.x - 3) > self.pos.x:
                self.xvel = 3
            elif (p.pos.x + 3) < self.pos.x:
                self.xvel = -3
            if (p.pos.y + 3) >= self.pos.y and (p.pos.y - 3) <= self.pos.y:
                self.yvel = 0
            elif (p.pos.y - 3) > self.pos.y:
                self.yvel = 3
            elif (p.pos.y + 3) < self.pos.y:
                self.yvel = -3
            if abs(self.xvel) == 3 and abs(self.yvel) == 3:
                self.xvel = (self.xvel/3)*(3/(2**0.5))
                self.yvel = (self.yvel/3)*(3/(2**0.5))

        elif dist > 148*sprite_scale and dist < 152*sprite_scale:
            self.xvel = self.yvel = 0
            
        elif dist <= 148*sprite_scale:
            if (p.pos.x + 3) >= self.pos.x and (p.pos.x - 3) <= self.pos.x:
                self.xvel = 0
            elif (p.pos.x - 3) > self.pos.x:
                self.xvel = -2
            elif (p.pos.x + 3) < self.pos.x:
                self.xvel = 2
            if (p.pos.y + 3) >= self.pos.y and (p.pos.y - 3) <= self.pos.y:
                self.yvel = 0
            elif (p.pos.y - 3) > self.pos.y:
                self.yvel = -2
            elif (p.pos.y + 3) < self.pos.y:
                self.yvel = 2
            if abs(self.xvel) == 2 and abs(self.yvel) == 2:
                self.xvel = (self.xvel/2)*(2**0.5)
                self.yvel = (self.yvel/2)*(2**0.5)

        self.player_collision(p)

        self.enemy_collision(e)

        self.tile_collisions(tiles)

        self.door_collisions(i_group)

        self.sync()

    def create_bullet(self,b_group):
        bullet = Bullet(self.pos.x,self.pos.y,self.display,blt,self.angle,"skeleton")
        b_group.add(bullet)
        camera.add(bullet)

    def rotatehead(self):
        self.rot_image = pygame.transform.rotate(self.scal_image,self.angle)
        self.rect = self.rot_image.get_rect(center = self.rect.center)

    def rotatearms(self):
        self.rot_arm = pygame.transform.rotate(self.scal_arm,self.angle)
        self.arm_rect = self.rot_arm.get_rect(center = self.arm_rect.center)

    def rotate(self):
        self.rotatehead()
        self.rotatearms()

    def chase_player(self,p,tiles,dist,e,i_group):
        dx,dy = self.pos.x - p.pos.x, self.pos.y - p.pos.y
        self.angle = math.degrees(math.atan2(dx,dy))
        self.rotate()
        self.move_to_player(p,tiles,dist,e,i_group)

    def move(self,p,tiles,dist,e,i_group):
        if dist <= self.sight:
            self.idle = False
            self.chase_player(p,tiles,dist,e,i_group)
        else:
            self.idle = True
            self.idle_move(tiles,p,e,i_group)

    def render_bars(self,offset):
        #progress rectangle stats
        hpbar_p_left = offset[0] - 9
        hpbar_p_top = offset[1] - 10
        hpbar_p_width = 30*(self.health/self.healthmax)
        hpbar_p_height = 6

        #border rectangle stats
        hpbar_b_left = hpbar_p_left - 2
        hpbar_b_top = hpbar_p_top - 2
        hpbar_b_width = 34
        hpbar_b_height = hpbar_p_height + 4

        #hp bar
        pygame.draw.rect(self.display,dark_red,pygame.Rect(hpbar_b_left,hpbar_b_top,hpbar_b_width,hpbar_b_height))
        pygame.draw.rect(self.display,red,pygame.Rect(hpbar_p_left,hpbar_p_top,hpbar_p_width,hpbar_p_height))

    def render(self):
        self.display.blit(self.rot_arm,self.arm_rect)
        self.display.blit(self.rot_image,self.rect)
        self.render_bars()

#zombie
class Zombie(Enemy):
    def __init__(self,x,y,display,image,arm,s_spawn,s_num):
        super().__init__(x,y,display,image,arm)
        self.t = random.randint(0,960)
        self.damage = 5
        self.angle = 0
        self.attack_timer = 0
        self.attack_dist = 25

    def create_coin(self,x,y,c_group):
        super().create_coin(x,y,c_group)

    def create_ammo(self,x,y,c_group):
        super().create_ammo(x,y,c_group)

    def player_collision(self,p):
        super().player_collision(p)

    def enemy_collision(self,e):
        super().enemy_collision(e)

    def sync(self):
        super().sync()

    def idle_sync(self):
        super().idle_sync()

    def attack(self,p,dist):
        if dist <= self.attack_dist and not(p.respawn_protection):
            self.attack_timer += 1
            if self.attack_timer >= 30:
                self.attack_timer = 0
                self.angle += 20
                self.rotate()
                p.health -= self.damage

    def update(self,p,tiles,dist,c_group,s_group,b_group,e,offset,i_group):
        self.dirty = 1
        self.die(p,c_group,s_group)
        self.move(p,tiles,dist,e,i_group)
        self.attack(p,dist)
        self.render_bars(offset)
        #self.render()

    def die(self,p,c_group,s_group):
        super().die(p,c_group,s_group)

    #def push(self,p):
        #super().push(p)

    def tile_collisions(self,tiles):
        super().tile_collisions(tiles)

    def door_collisions(self,i_group):
        super().door_collisions(i_group)

    def idle_move(self,tiles,p,e,i_group):
        if self.t >= 960:
            self.t = 0
        else:
            self.t += 1
        if self.t <= 120:
            self.idle_xvel = 0
            self.idle_yvel = -1
        elif self.t > 120 and self.t <= 240:
            self.angle = ((self.t-120)/120)*-90
            self.idle_xvel = 0
            self.idle_yvel = 0
            self.rotate()
        elif self.t > 240 and self.t <= 360:
            self.idle_xvel = 1 
            self.idle_yvel = 0
        elif self.t > 360 and self.t <= 480:
            self.angle = ((self.t-240)/120)*-90
            self.idle_xvel = 0
            self.idle_yvel = 0
            self.rotate()
        elif self.t > 480 and self.t <= 600:
            self.idle_xvel = 0
            self.idle_yvel = 1
        elif self.t > 600 and self.t <= 720:
            self.angle = ((self.t-360)/120)*-90
            self.idle_xvel = 0
            self.idle_yvel = 0
            self.rotate()
        elif self.t > 720 and self.t <= 840:
            self.idle_xvel = -1
            self.idle_yvel = 0
        else:
            self.angle = ((self.t-480)/120)*-90
            self.idle_xvel = 0
            self.idle_yvel = 0
            self.rotate()

        self.player_collision(p)

        self.enemy_collision(e)

        self.tile_collisions(tiles)

        self.door_collisions(i_group)

        self.idle_sync()

    def move_to_player(self,p,tiles,e,i_group):#change to a better movement
        if (p.pos.x + 3) >= self.pos.x and (p.pos.x - 3) <= self.pos.x:
            self.xvel = 0
        elif (p.pos.x - 3) > self.pos.x:
            self.xvel = 3
        elif (p.pos.x + 3) < self.pos.x:
            self.xvel = -3
        if (p.pos.y + 3) >= self.pos.y and (p.pos.y - 3) <= self.pos.y:
            self.yvel = 0
        elif (p.pos.y - 3) > self.pos.y:
            self.yvel = 3
        elif (p.pos.y + 3) < self.pos.y:
            self.yvel = -3
        if abs(self.xvel) == 3 and abs(self.yvel) == 3:
            self.xvel = (self.xvel/3)*(3/(2**0.5))
            self.yvel = (self.yvel/3)*(3/(2**0.5))

        self.player_collision(p)

        self.enemy_collision(e)

        self.tile_collisions(tiles)

        self.door_collisions(i_group)

        self.sync()

    def rotatehead(self):
        self.rot_image = pygame.transform.rotate(self.scal_image,self.angle)
        self.rect = self.rot_image.get_rect(center = self.rect.center)

    def rotatearms(self):
        self.rot_arm = pygame.transform.rotate(self.scal_arm,self.angle)
        self.arm_rect = self.rot_arm.get_rect(center = self.arm_rect.center)

    def rotate(self):
        self.rotatehead()
        self.rotatearms()

    def chase_player(self,p,tiles,e,i_group):
        dx,dy = self.pos.x - p.pos.x, self.pos.y - p.pos.y
        self.angle = math.degrees(math.atan2(dx,dy))
        self.rotate()
        self.move_to_player(p,tiles,e,i_group)

    def move(self,p,tiles,dist,e,i_group):
        if dist <= self.sight:
            self.idle = False
            self.chase_player(p,tiles,e,i_group)
        else:
            self.idle = True
            self.idle_move(tiles,p,e,i_group)

        #self.push(p)

        #self.sync()?

    def take_damage(self):
        pass

    def render_bars(self,offset):
        #progress rectangle stats
        hpbar_p_left = offset[0] - 9
        hpbar_p_top = offset[1] - 10
        hpbar_p_width = 30*(self.health/self.healthmax)
        hpbar_p_height = 6

        #border rectangle stats
        hpbar_b_left = hpbar_p_left - 2
        hpbar_b_top = hpbar_p_top - 2
        hpbar_b_width = 34
        hpbar_b_height = hpbar_p_height + 4

        #hp bar
        pygame.draw.rect(self.display,dark_red,pygame.Rect(hpbar_b_left,hpbar_b_top,hpbar_b_width,hpbar_b_height))
        pygame.draw.rect(self.display,red,pygame.Rect(hpbar_p_left,hpbar_p_top,hpbar_p_width,hpbar_p_height))

    def render(self):
        self.display.blit(self.rot_arm,self.arm_rect)
        self.display.blit(self.rot_image,self.rect)
        self.render_bars()

#player
class Player(Entity):
    def __init__(self,x,y,display,image,arm):
        super().__init__(x,y,display,image,arm)
        self.type = "player"
        self.weapon = 0
        self.angle = 0
        self.attack_timer = 0
        self.wait = 0
        self.healthmax = 100
        self.health = 100
        self.healthregen = 1
        self.energyval = 50
        self.energyregen = 0.2
        self.energymax = 50
        self.sprintvelmult = 2
        self.footprint_timer = 0
        self.score = 0
        self.bullet_delay = 7
        self.cash = 0
        self.change_lvl = False
        self.damage = 2
        self.kills = 0
        self.bullets = 50
        self.attack_dist = 20
        self.weapon_hitbox = self.hitbox
        self.lives = 3
        self.z = 4
        self.portal_cost = 10
        self.respawn_protection = False
        self.respawn_protection_timer = 0

    def update(self,moves,tiles,mx,my,b_group,f_group,e_group,s_group,i_group):
        self.change_lvl = False
        #self.die()
        self.rotate_to_mouse(mx,my)
        self.move(moves,tiles,f_group,i_group)
        if self.bullet_delay < 7:
            self.bullet_delay += 1
        if moves[6]:
            self.change_weapon()
        self.attack_timer += 1
        if moves[5]:
            self.attack(mx,my,b_group,e_group,s_group)
        #self.render()
        self.dirty = 1
        self.respawn()
        return self.change_lvl

    def die(self):
        if self.health <= 0:
            self.lives -= 1
            self.pos = pygame.math.Vector2((200*sprite_scale,200*sprite_scale))
            self.respawn_protection = True
            return True
        
    def respawn(self):
        if self.respawn_protection:
            self.respawn_protection_timer += 1
            if self.respawn_protection_timer >= 30:
                self.respawn_protection = False
                self.respawn_protection_timer = 0

    def sync(self):
        super().sync()

    def collectable_coll(self,c_group):
        for c in c_group:
            if self.hitbox.colliderect(c.rect):
                if c.c_type == "coin":
                    self.cash += c.value
                    c.kill()
                elif c.c_type == "weapon":
                    pass
                elif c.c_type == "consumable":
                    pass

    def tile_collisions(self,tiles,moves,f_group):#not done abs() on mud + snow(when going diagonally)
        for t in tiles:
            #collision of impassible tiles
            if t.t_type == "wall" or t.t_type == "tree":
                #x axis collisions
                if t.rect.colliderect(self.hitbox.topleft[0] + (self.xvel * sprite_scale * 1.1),self.hitbox.topleft[1],self.hitbox.topright[0]-self.hitbox.topleft[0],self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                    if self.xvel > 0:
                        self.xvel = t.rect.left - self.hitbox.left
                        self.xvel = 0
                    elif self.xvel < 0:
                        self.xvel = self.hitbox.right - t.rect.right
                        self.xvel = 0
                #y axis collisions
                elif t.rect.colliderect(self.hitbox.topleft[0],self.hitbox.topleft[1] + (self.yvel * sprite_scale * 1.1),self.hitbox.topright[0]-self.hitbox.topleft[0],self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                    if self.yvel < 0:
                        self.yvel = self.hitbox.bottom - t.rect.bottom
                        self.yvel = 0
                    elif self.yvel > 0:
                        self.yvel = t.rect.top - self.hitbox.top
                        self.yvel = 0
            #collision of mud
            elif t.t_type == "mud":
                if t.rect.colliderect(self.hitbox):
                    if self.xvel != 0:
                        self.xvel = self.xvel / 2
                    if self.yvel != 0:
                        self.yvel = self.yvel / 2
                    #makes sure the speed doesn't decrease multiple times when overlapping tiles
                    if  not moves[4]:
                        if self.xvel < 2 and self.xvel > 0:
                            self.xvel = 2
                        elif self.xvel < 0 and self.xvel > -2:
                            self.xvel = -2
                        if self.yvel < 2 and self.yvel > 0:
                            self.yvel = 2
                        elif self.yvel < 0 and self.yvel > -2:
                            self.yvel = -2
                    else:#for sprint
                        if self.xvel < 3 and self.xvel > 0:
                            self.xvel = 3
                        elif self.xvel < 0 and self.xvel > -3:
                            self.xvel = -3
                        if self.yvel < 3 and self.yvel > 0:
                            self.yvel = 3
                        elif self.yvel < 0 and self.yvel > -3:
                            self.yvel = -3
                    self.footprint_timer += 1
                    if self.footprint_timer >= 15:
                        self.footprint_timer = 0
                        self.create_m_footprint(f_group)
            elif t.t_type == "snowy_grass":
                if t.rect.colliderect(self.hitbox):
                    #self.display.blit(pygame.transform.rotate(pygame.image.load(snow_footprints),self.hitbox.topleft),angle)
                    if self.xvel != 0:
                        self.xvel = self.xvel / 1.5
                    if self.yvel != 0:
                        self.yvel = self.yvel / 1.5
                    #makes sure the speed doesn't decrease multiple times when overlapping tiles
                    if  not moves[4]:
                        if self.xvel < (8/3) and self.xvel > 0:
                            self.xvel = (8/3)
                        elif self.xvel < 0 and self.xvel > -(8/3):
                            self.xvel = -(8/3)
                        if self.yvel < (8/3) and self.yvel > 0:
                            self.yvel = (8/3)
                        elif self.yvel < 0 and self.yvel > -(8/3):
                            self.yvel = -(8/3)
                    else:#for sprint
                        if self.xvel < 3 and self.xvel > 0:
                            self.xvel = 3
                        elif self.xvel < 0 and self.xvel > -3:
                            self.xvel = -3
                        if self.yvel < 3 and self.yvel > 0:
                            self.yvel = 3
                        elif self.yvel < 0 and self.yvel > -3:
                            self.yvel = -3
                    self.footprint_timer += 1
                    if self.footprint_timer >= 15:
                        self.footprint_timer = 0
                        self.create_s_footprint(f_group)
            elif t.t_type == "portal" and moves[7] and self.energyval >= 10:#t.timer == 90:
                if t.rect_1.colliderect(self.hitbox):
                    self.pos = t.pos_2 + (tile_scale/2,tile_scale/2)
                    self.energyval -= self.portal_cost
                    #t.timer = 0
                elif t.rect_2.colliderect(self.hitbox):
                    self.pos = t.pos_1 + (tile_scale/2,tile_scale/2)
                    self.energyval -= self.portal_cost
                    #t.timer = 0
            elif t.t_type == "b_portal" and moves[7]:
                if t.rect.colliderect(self.hitbox):
                    self.change_lvl = True

#need to add for when snow and mud are next to each other

    def door_collisions(self,i_group):
        for d in i_group:
            #collision of doors
            if d.type == "door":#split normal and idle to functions
                #x axis collisions
                if d.rect.colliderect(self.hitbox.topleft[0] + (self.xvel * sprite_scale * 1.1),self.hitbox.topleft[1],self.hitbox.topright[0]-self.hitbox.topleft[0],self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                    if self.xvel > 0:
                        self.xvel = d.rect.left - self.hitbox.left
                        self.xvel = 0
                    elif self.xvel < 0:
                        self.xvel = self.hitbox.right - d.rect.right
                        self.xvel = 0
                #y axis collisions
                if d.rect.colliderect(self.hitbox.topleft[0],self.hitbox.topleft[1] + (self.yvel * sprite_scale * 1.1),self.hitbox.topright[0]-self.hitbox.topleft[0],self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                    if self.yvel < 0:
                        self.yvel = self.hitbox.bottom - d.rect.bottom
                        self.yvel = 0
                    elif self.yvel > 0:
                        self.yvel = d.rect.top - self.hitbox.top
                        self.yvel = 0

    def move(self,moves,tiles,f_group,i_group):
        self.xvel = 4
        self.yvel = 4
        if moves[0] and not moves[1]:
            self.yvel = -self.yvel
        elif moves[1] and not moves[0]:
            self.yvel = self.yvel
        elif moves[0] and moves[1]:
            self.yvel = 0
        else:
            self.yvel = 0
        if moves[2] and not moves[3]:
            self.xvel = -self.xvel
        elif moves[3] and not moves[2]:
            self.xvel = self.xvel
        elif moves[2] and moves[3]:
            self.xvel = 0
        else:
            self.xvel = 0
        if abs(self.xvel) == 4 and abs(self.yvel) == 4:
            self.xvel = (self.xvel/4)*(8**0.5)
            self.yvel = (self.yvel/4)*(8**0.5)

        self.sprint(moves)

        self.tile_collisions(tiles,moves,f_group)

        self.door_collisions(i_group)

        self.sync()

    def rotatehead(self):
        self.rot_image = pygame.transform.rotate(self.scal_image,self.angle)
        self.rect = self.rot_image.get_rect(center = self.rect.center)

    def rotatearms(self):
        self.rot_arm = pygame.transform.rotate(self.scal_arm,self.angle)
        self.arm_rect = self.rot_arm.get_rect(center = self.arm_rect.center)

    def rotate_to_mouse(self,mx,my):
        dx,dy = (d_width / 2) - mx, (d_height / 2) - my
        self.angle = math.degrees(math.atan2(dx,dy))
        self.rotatehead()
        self.rotatearms()

    def rotate(self):
        self.rotatehead()
        self.rotatearms()

    def render_text(self):
        health = textbox((d_width/2)-30,(d_height * 0.96)+1,15,white,self.display)
        energy = textbox((d_width/2)-20,(d_height * 0.92)+1,15,white,self.display)
        energy.draw_l(str(self.energyval)+"/"+str(self.energymax))
        health.draw_l(str(self.health)+"/"+str(self.healthmax))

    def render_bars(self):
        energybar_p_left = hpbar_p_left = 300
        energybar_p_top, hpbar_p_top = d_height * 0.92, d_height * 0.96
        energybar_p_width, hpbar_p_width = ((d_width-(energybar_p_left*2))*(self.energyval/self.energymax)), ((d_width-(hpbar_p_left*2))*(self.health/self.healthmax))
        energybar_p_height = hpbar_p_height = 15

        energybar_b_left = hpbar_b_left = energybar_p_left - 3
        energybar_b_top, hpbar_b_top = energybar_p_top - 3, hpbar_p_top - 3
        energybar_b_width = hpbar_b_width = d_width - (energybar_b_left*2)
        energybar_b_height, hpbar_b_height = energybar_p_height + 6, hpbar_p_height + 6

        #energy bar
        pygame.draw.rect(self.display,dark_blue,pygame.Rect(energybar_b_left,energybar_b_top,energybar_b_width,energybar_b_height))
        pygame.draw.rect(self.display,blue,pygame.Rect(energybar_p_left,energybar_p_top,energybar_p_width,energybar_p_height))

        #hp bar
        pygame.draw.rect(self.display,dark_green,pygame.Rect(hpbar_b_left,hpbar_b_top,hpbar_b_width,hpbar_b_height))
        pygame.draw.rect(self.display,green,pygame.Rect(hpbar_p_left,hpbar_p_top,hpbar_p_width,hpbar_p_height))

    def render_hearts(self):
        for l in range(0,self.lives):
            hrt_rect = hrt.get_rect(topleft = (round(d_width - 48 - (l*33)),15))
            self.display.blit(hrt,hrt_rect)

    def render_weapon_show(self):
        rect = fist_show.get_rect(topleft = (round(d_width-140),round(d_height-140)))
        self.display.blit(w_show[self.weapon],rect)
    
    def sprint(self,moves):
        self.wait += 1
        if self.wait >= 30:
            self.energyval += self.energyregen
            if self.energyval >= self.energymax:
                self.energyval = self.energymax
                self.wait = 0
        if moves[4] and self.energyval > 0 and (self.xvel != 0 or self.yvel != 0):
            self.wait = 0
            self.energyval -= 0.5
            self.xvel = self.sprintvelmult * self.xvel
            self.yvel = self.sprintvelmult * self.yvel
            if self.energyval <= 0:
                self.energyval = 0
        self.energyval = round(self.energyval,1)

    def change_weapon(self):
        if self.weapon ==  0:
            self.weapon = 1
        elif self.weapon == 1:
            self.weapon = 0
        else:
            pass

    def attack(self,mx,my,b_group,e_group,s_group):#needs improving, click and hold rotates player back and forth
        if self.weapon == 0:
            if self.attack_timer >= 15:
                self.angle += 20
                for e in e_group.sprites():
                    if self.weapon_hitbox.colliderect(e.hitbox.topleft[0]-5,e.hitbox.topright[1]-5,(e.hitbox.topright[0]-e.hitbox.topleft[0]+10),(e.hitbox.bottomleft[1]-e.hitbox.topleft[1]+10)):
                        if e.solid == True:
                            e.health -= self.damage
                for s in s_group.sprites():
                    if self.weapon_hitbox.colliderect(s.hitbox.topleft[0]-5,s.hitbox.topright[1]-5,(s.hitbox.topright[0]-s.hitbox.topleft[0]+10),(s.hitbox.bottomleft[1]-s.hitbox.topleft[1]+10)):
                        s.health -= self.damage
            
                self.rotate()
                self.attack_timer = 0
            #self.attack = True
        #bullet spawn has longer delay and max shoot before reload(just max bullets now)
        if self.weapon == 1:
            if self.bullets > 0:
                if self.bullet_delay >= 7:
                    self.bullets -= 1
                    self.create_bullet(b_group)
                    self.bullet_delay = 0

    def create_s_footprint(self,f_group):
        footprint = Footprint(self.pos.x,self.pos.y,self.display,snow_footprints,self.angle)
        f_group.add(footprint)
        camera.add(footprint)

    def create_m_footprint(self,f_group):
        footprint = Footprint(self.pos.x,self.pos.y,self.display,mud_footprints,self.angle)
        f_group.add(footprint)
        camera.add(footprint)

    def create_bullet(self,b_group):
        bullet = Bullet(self.pos.x,self.pos.y,self.display,blt,self.angle,"player")
        b_group.add(bullet)
        camera.add(bullet)

    def render(self,arm_offset_pos,img_offset_pos):
        self.display.blit(self.rot_arm,arm_offset_pos)#order matters as arms look weird if drawn over head
        self.display.blit(self.rot_image,img_offset_pos)
        self.render_bars()
        self.render_text()
        self.render_hearts()
        self.render_weapon_show()

class Bullet(Object):
    def __init__(self,x,y,display,image,angle,b_type):
        super().__init__(x,y,display,image)
        self.scal_image = pygame.transform.scale(self.image,(sprite_scale*4,sprite_scale*4))
        self.rot_image = self.scal_image
        self.rect = self.rot_image.get_rect(center = (round(self.pos.x),round(self.pos.y)))
        self.hitbox = self.scal_image.get_rect(center = (round(self.pos.x),round(self.pos.y)))
        self.angle = math.radians(angle) + math.pi
        self.xvel = (10 * math.sin(self.angle)) + random.randint(0,1) - 0.5
        self.yvel = (10 * math.cos(self.angle)) + random.randint(0,1) - 0.5
        self.damage = 2
        self.t = 0
        self.z = 1
        self.type = "bullet"
        self.b_type = b_type

    def update(self,tiles,mx,my,player,enemies,spawners,i_group):
        self.move(tiles,mx,my,player,enemies,spawners,i_group)
        self.stop()
        #self.render()

    def move(self,tiles,mx,my,player,enemies,spawners,i_group):

        self.tile_collisions(tiles)

        self.entity_collisions(player,enemies,spawners)

        self.door_collisions(i_group)
        
        self.sync()

    def stop(self):
        self.t += 1
        if self.t >= 60:
            self.kill()

    def tile_collisions(self,tiles):
        for t in tiles:
            #collision of impassible tiles
            if t.t_type == "wall" or t.t_type == "tree" or t.t_type == "door":
                if t.rect.colliderect(self.hitbox.topleft[0] + (self.xvel * sprite_scale),self.hitbox.topleft[1] + (self.yvel * sprite_scale),self.hitbox.topright[0]-self.hitbox.topleft[0],self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                    self.kill()

    def door_collisions(self,i_group):
        for d in i_group:
            #collision of impassible tiles
            if d.type == "door":
                if d.rect.colliderect(self.hitbox.topleft[0] + (self.xvel * sprite_scale),self.hitbox.topleft[1] + (self.yvel * sprite_scale),self.hitbox.topright[0]-self.hitbox.topleft[0],self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                    self.kill()

    def enemy_collisions(self,enemies,spawners):
        for e in enemies:
            #collision of enemy hitbox
            if e.solid and e.hitbox.colliderect(self.hitbox.topleft[0] + (self.xvel * sprite_scale),self.hitbox.topleft[1] + (self.yvel * sprite_scale),self.hitbox.topright[0]-self.hitbox.topleft[0],self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                self.deal_damage(e)
                self.kill()
        for s in spawners:
            #collision of spawner hitbox
            if s.solid and s.hitbox.colliderect(self.hitbox.topleft[0] + (self.xvel * sprite_scale),self.hitbox.topleft[1] + (self.yvel * sprite_scale),self.hitbox.topright[0]-self.hitbox.topleft[0],self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                self.deal_damage(s)
                self.kill()

    def player_collision(self,player):
        if player.hitbox.colliderect(self.hitbox.topleft[0] + (self.xvel * sprite_scale),self.hitbox.topleft[1] + (self.yvel * sprite_scale),self.hitbox.topright[0]-self.hitbox.topleft[0],self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
            self.deal_damage(player)
            self.kill()

    def entity_collisions(self,player,enemies,spawners):
        if self.b_type == "player":
            self.enemy_collisions(enemies,spawners)
        else:
            self.player_collision(player)

    def deal_damage(self,entity):
        entity.health -= self.damage

    def sync(self):
        super().sync()

    def rotate(self):
        self.rot_image = pygame.transform.rotate(self.scal_image,self.angle)
        self.rect = self.rot_image.get_rect(center = self.rect.center)

    def render(self):
        self.display.blit(self.rot_image,self.rect)

class Footprint(Object):
    def __init__(self,x,y,display,image,angle):
        super().__init__(x,y,display,image)
        self.type = "particle"
        self.scal_image = pygame.transform.scale(self.image,(sprite_scale*18,sprite_scale*18))
        self.rot_image = pygame.transform.rotate(self.scal_image,angle)
        self.rect = self.rot_image.get_rect(center = (round(self.pos.x),round(self.pos.y)))
        self.t = 0
        self.xvel = 0
        self.yvel = 0
        self.angle = angle
        self.z = 1

    def update(self):
        self.rotate()
        self.fade()
        #self.render()

    def fade(self):
        self.t += 1
        if self.t >= 600:
            self.t = 0
            self.kill()

    def rotate(self):
        self.rot_image = pygame.transform.rotate(self.scal_image,self.angle)
        self.rect = self.rot_image.get_rect(center = self.rect.center)

    def render(self):
        self.display.blit(self.rot_image,self.rect)

class Collectable(Object):
    def __init__(self,x,y,display,image,value):
        super().__init__(x,y,display,image)
        self.type = "collectable"
        self.value = value
        self.fade_timer = 0

    def fade(self):
        self.fade_timer += 1
        if self.fade_timer >= self.fade_limit:
            self.kill()

    #pushes them out of walls and portals
    #def push(self,tiles):
    #    pass

class Ammo(Collectable):
    def __init__(self,x,y,display,image,value):
        super().__init__(x,y,display,image,value)
        self.fade_limit = random.randint(1250,1500)
        self.scal_image = pygame.transform.scale(self.image,(sprite_scale*32,sprite_scale*32))
        self.rot_image = self.scal_image

    def update(self,p):
        self.collect(p)
        self.fade()

    def collect(self,p):
        if p.hitbox.colliderect(self.hitbox):
            p.bullets += self.value
            self.kill()

    def fade(self):
        super().fade()

class Coin(Collectable):
    def __init__(self,x,y,display,image,value):
        super().__init__(x,y,display,image,value)
        self.fade_limit = random.randint(850,950)

    def update(self,p):
        self.collect(p)
        self.fade()

    def collect(self,p):
        if p.hitbox.colliderect(self.hitbox):
            p.cash += self.value
            self.kill()

    def fade(self):
        super().fade()

class Menu_player(Entity):
    def __init__(self,x,y,display,image,arm):
        super().__init__(x,y,display,image,arm)
        self.energyval = 50
        self.energyregen = 0.2
        self.energymax = 50
        self.sprintvelmult = 2
        self.wait = 0

    def update(self,moves,mx,my,m_p_rect,play_group,quit_group,ctrl_group):
        self.rotate(mx,my)
        self.move(moves,play_group,quit_group,ctrl_group)
        self.render()
        self.die(m_p_rect)

    def move(self,moves,play_group,quit_group,ctrl_group):
        self.xvel = 4
        self.yvel = 4
        if moves[0] and not moves[1]:
            self.yvel = -self.yvel
        elif moves[1] and not moves[0]:
            self.yvel = self.yvel
        elif moves[0] and moves[1]:
            self.yvel = 0
        else:
            self.yvel = 0
        if moves[2] and not moves[3]:
            self.xvel = -self.xvel
        elif moves[3] and not moves[2]:
            self.xvel = self.xvel
        elif moves[2] and moves[3]:
            self.xvel = 0
        else:
            self.xvel = 0
        if abs(self.xvel) == 4 and abs(self.yvel) == 4:
            self.xvel = (self.xvel/4)*(8**0.5)
            self.yvel = (self.yvel/4)*(8**0.5)

        self.sprint(moves)

        self.border_collision()

        self.button_collision(play_group)
        self.button_collision(quit_group)
        self.button_collision(ctrl_group)

        self.sync()

    def die(self,m_p_rect):
        if self.hitbox.colliderect(m_p_rect):
            self.dirty = 0
            self.kill()
        else:
            self.dirty = 1

    def sync(self):
        super().sync()

    def border_collision(self):
        if self.pos.x <= ((9 * sprite_scale) - self.xvel):
            self.xvel = 0
        elif self.pos.x >= ((d_width - (9 * sprite_scale)) - self.xvel):
            self.xvel = 0
        if self.pos.y <= ((9 * sprite_scale) - self.yvel):
            self.yvel = 0
        elif self.pos.y >= ((d_height - (9 * sprite_scale)) - self.yvel):
            self.yvel = 0

    def button_collision(self,group):
        if group[1] == group[2]:
            if self.hitbox.colliderect((group[0].topleft[0] - self.xvel),group[0].topleft[1],1,(group[0].bottomleft[1] - group[0].topleft[1])):
                if self.xvel > 0:
                    self.xvel = 0
            elif self.hitbox.colliderect((group[0].topright[0] - 1),group[0].topright[1],(1 - self.xvel),(group[0].bottomright[1] - group[0].topright[1])):
                if self.xvel < 0:
                    self.xvel = 0
            if self.hitbox.colliderect(group[0].topleft[0],(group[0].topleft[1] - self.yvel),(group[0].topright[0] - group[0].topleft[0]),1):
                if self.yvel > 0:
                    self.yvel = 0
            elif self.hitbox.colliderect(group[0].bottomleft[0],(group[0].bottomleft[1] - 1),(group[0].topright[0] - group[0].topleft[0]),(1 - self.yvel)):
                if self.yvel < 0:
                    self.yvel = 0
            elif self.hitbox.colliderect(group[0].bottomleft[0],group[0].bottomleft[1]-16+(9*sprite_scale),(group[0].bottomright[0]-group[0].bottomleft[0]),2):
                self.pos.y = group[0].bottomleft[1] + (9*sprite_scale)

    def sprint(self,moves):
        self.wait += 1
        if self.wait >= 60:
            self.energyval += self.energyregen
            if self.energyval >= self.energymax:
                self.energyval = self.energymax
                self.wait = 0
        if moves[4] and self.energyval > 0 and (self.xvel != 0 or self.yvel != 0):
            self.wait = 0
            self.energyval -= 0.5
            self.xvel = self.sprintvelmult * self.xvel
            self.yvel = self.sprintvelmult * self.yvel
            if self.energyval <= 0:
                self.energyval = 0
        self.energyval = round(self.energyval,1)
        
    def rotatehead(self):
        self.rot_image = pygame.transform.rotate(self.scal_image,self.angle)
        self.rect = self.rot_image.get_rect(center = self.rect.center)

    def rotatearms(self):
        self.rot_arm = pygame.transform.rotate(self.scal_arm,self.angle)
        self.arm_rect = self.rot_arm.get_rect(center = self.arm_rect.center)

    def rotate(self,mx,my):
        dx,dy = self.pos.x - mx, self.pos.y - my
        self.angle = math.degrees(math.atan2(dx,dy))
        self.rotatehead()
        self.rotatearms()

    def render_bar(self,play_rect,play_img):
        x = play_rect.topleft[0] + 8
        if play_img == play_u:
            y = play_rect.topleft[1] + 8
        elif play_img == play_d:
            y = play_rect.topleft[1] + 24
        w = (play_rect.topright[0] - play_rect.topleft[0] - 16) * (self.energyval/self.energymax)
        h = play_rect.bottomleft[1] - play_rect.topleft[1] - 32

        pygame.draw.rect(self.display,blue,pygame.Rect(x,y,w,h))
        
    def render(self):
        self.display.blit(self.rot_image,self.rect)
        self.display.blit(self.rot_arm,self.arm_rect)

class Interactable(pygame.sprite.DirtySprite):
    def __init__(self,x,y,display,image1,image2):
        super().__init__()
        pygame.sprite.DirtySprite.__init__(self)
        self.pos = pygame.math.Vector2((x,y))
        self.display = display
        self.image1 = image1
        self.image2 = image2
        self.image = self.image1
        self.rect1 = self.image1.get_rect(bottomleft = (round(x),round(y)))
        self.rect2 = self.image2.get_rect(bottomleft = (round(x),round(y)))
        self.rect = self.rect1
        self.hitbox = pygame.Rect(x-10,y-58,68,68)
        self.once = False
        self.type = "interactable"
        self.z = 2
        self.dirty = 1
        self.needs_key = False

    #def render(self):
    #    self.display.blit(self.image,self.rect)

class Chest(Interactable):
    def __init__(self,x,y,display,image1,image2,c_type):
        super().__init__(x,y,display,image1,image2)
        self.once = True
        self.c_type = c_type
        self.type = "chest"

    def update(self,moves,player,c_group):
        self.change_state(moves,player,c_group)
        #self.render()

    def change_state(self,moves,player,c_group):
        if moves[7] and player.hitbox.colliderect(self.hitbox):
            if self.image == self.image1:
                self.image = self.image2
                self.rect = self.rect2
                self.action(c_group)
            elif self.image == self.image2 and self.once == False:
                self.image = self.image1
                self.rect = self.rect1
            else:
                pass

    def action(self,c_group):
        for n in range (0,self.c_type*5):
            x = (self.hitbox.topleft[0] + random.randint(0,(self.hitbox.topright[0]-self.hitbox.topleft[0])))
            y = (self.hitbox.topleft[1] + random.randint(0,(self.hitbox.bottomleft[1]-self.hitbox.topleft[1])))
            num = random.randint(0,30)
            if num == 30:
                self.create_ammo(x,y,c_group)
            else:
                self.create_coin(x,y,c_group)

    def create_coin(self,x,y,c_group):
        coin = Coin(x,y,self.display,cn,1)
        c_group.add(coin)
        camera.add(coin)

    def create_ammo(self,x,y,c_group):
        ammo = Ammo(x,y,self.display,amo,30)
        c_group.add(ammo)
        camera.add(ammo)

    #def render(self):
    #    super().render()

class Door(Interactable):
    def __init__(self, x, y, display, image1, image2, d_type):
        super().__init__(x, y, display, image1, image2)
        if d_type == "ur":
            self.rect1 = self.image1.get_rect(bottomleft = (round(x),round(y)))
            self.rect2 = self.image2.get_rect(bottomleft = (round(x),round(y)))
        elif d_type == "ul":
            self.rect1 = self.image1.get_rect(bottomright = (round(x),round(y)))
            self.rect2 = self.image2.get_rect(bottomright = (round(x),round(y)))
        elif d_type == "dr":
            self.rect1 = self.image1.get_rect(topleft = (round(x),round(y)))
            self.rect2 = self.image2.get_rect(topleft = (round(x),round(y)))
        elif d_type == "dl":
            self.rect1 = self.image1.get_rect(topright = (round(x),round(y)))
            self.rect2 = self.image2.get_rect(topright = (round(x),round(y)))
        self.rect = self.rect1
        self.hitbox = pygame.Rect(self.rect.topleft[0]-10,self.rect.topleft[1]-10,self.rect.topright[0]-self.rect.topleft[0]+20,self.rect.bottomleft[1]-self.rect.topleft[1]+20)
        self.type = "door"

    def update(self,moves,player):
        self.change_state(moves,player)
        self.hitbox = pygame.Rect(self.rect.topleft[0]-10,self.rect.topleft[1]-10,self.rect.topright[0]-self.rect.topleft[0]+20,self.rect.bottomleft[1]-self.rect.topleft[1]+20)

    def change_state(self,moves,player):
        if moves[7] and player.hitbox.colliderect(self.hitbox):
            if self.image == self.image1:
                self.image = self.image2
                self.rect = self.rect2
            elif self.image == self.image2 and self.once == False:
                self.image = self.image1
                self.rect = self.rect1
            else:
                pass
