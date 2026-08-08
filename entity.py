import math, random#pygame, math, random
from textbox import *
from settings import *
#from pygame.locals import *

# def get_timer():
#     return timer

#objects (all sprites)
class Object(pygame.sprite.DirtySprite):
    def __init__(self, x, y, display, image):#I may not need image, arm, tail as args
        super().__init__()
        self.type = "object"
        self.display = display
        pygame.sprite.DirtySprite.__init__(self)
        self.pos = pygame.math.Vector2((x, y))
        self.solid = True#might remove?
        self.health = 10
        self.healthmax = 10
        self.xvel = 0
        self.yvel = 0
        self.vel = 4
        self.z = 3
        self.image = image
        self.scal_image = pygame.transform.scale(self.image, (sprite_scale*18, sprite_scale*18))
        self.rot_image = self.scal_image
        self.rect = self.rot_image.get_rect(center = (round(self.pos.x), round(self.pos.y)))
        self.hitbox = self.scal_image.get_rect(center = (round(self.pos.x), round(self.pos.y)))
        # self.save_vals = ['solid', 'health', 'healthmax', 'xvel', 'yvel', 'vel']
        
    def die(self, p, c_group):#, camera):
        if self.health <= 0:
            p.score += self.healthmax
            for n in range(0, (self.healthmax//2 - random.randint(0, self.healthmax//4))):
                x = (self.hitbox.topleft[0] + random.randint(0, (self.hitbox.topright[0]-self.hitbox.topleft[0])))
                y = (self.hitbox.topleft[1] + random.randint(0, (self.hitbox.bottomleft[1]-self.hitbox.topleft[1])))
                num = random.randint(0, 30)
                if num == 30:
                    self.create_ammo(x, y, c_group)#, camera)
                else:
                    self.create_coin(x, y, c_group)#, camera)
            p.kills += 1
            self.kill()
            
    def create_coin(self, x, y, c_group):#, camera):
        coin = Coin(x, y)
        c_group.add(coin)
        # camera.add(coin)

    def create_ammo(self, x, y, c_group):#, camera):
        ammo = Ammo(x, y)
        c_group.add(ammo)
        # camera.add(ammo)

    def sync(self):
        self.pos.x += (self.xvel * sprite_scale)
        self.pos.y += (self.yvel * sprite_scale)
        self.hitbox.center = self.pos.x, self.pos.y#just do self.pos
        self.rect.center = self.pos.x, self.pos.y
        
    def push(self):
        pass
        
#entities(moving sprites)
class Entity(Object):
    def __init__(self, x, y, display, image, arm):
        super().__init__(x, y, display, image)
        self.type = "entity"
        self.arm = arm
        self.scal_arm = pygame.transform.scale(self.arm, (sprite_scale*30, sprite_scale*30))
        self.rot_arm = self.scal_arm
        self.arm_rect = self.scal_arm.get_rect(center = (round(self.pos.x), round(self.pos.y)))
        self.t = random.randint(0, 960)
        self.idle_vel = 1
        self.z = 4
        self.next_pos = pygame.math.Vector2((0,0))
        self.collidable_tiles = []
        # self.save_vals.extend(['t', 'idle_vel', 'next_pos', 'collidable_tiles'])

    def die(self, p, c_group, s_group):#, camera):
        super().die(p, c_group)#, camera)

    def create_coin(self, x, y, c_group):#, camera):
        super().create_coin(x, y, c_group)#, camera)

    def create_ammo(self, x, y, c_group):#, camera):
        super().create_ammo(x, y, c_group)#, camera)

    def sync(self):
        super().sync()
        self.arm_rect.center = self.pos.x, self.pos.y
        
    def random_move(self):
        if self.idle == False:
            self.t = 0
            self.next_pos.x = random.randint(0, int(self.pos.x) + 200) - 100
            self.next_pos.y = random.randint(0, int(self.pos.y) + 200) - 100
            # self.next_pos.x, self.next_pos.y = next_x, next_y
            self.idle = True
        
        if self.t > 60 and self.t < 210:
            if self.pos.x <= self.next_pos.x - 3:
                self.xvel = self.idle_vel
            elif self.pos.x >= self.next_pos.x + 3:
                self.xvel = -self.idle_vel
            else:
                self.xvel = 0
                
            if self.pos.y <= self.next_pos.y - 3:
                self.yvel = self.idle_vel
            elif self.pos.y >= self.next_pos.y + 3:
                self.yvel = -self.idle_vel
            else:
                self.yvel = 0
                
            if self.pos.distance_to(self.next_pos) < 3:
                self.idle = False
            
        if self.t >= 210:
            self.idle = False
            
        self.t += 1
        
        if abs(self.xvel) == abs(self.yvel) and self.xvel != 0:
            abs_vel = (self.vel/root_2)
            self.xvel = (self.xvel/self.idle_vel) * abs_vel
            self.yvel = (self.yvel/self.idle_vel) * abs_vel
            
    def square_move(self):
        if self.t >= 960:
            self.t = 0
        else:
            self.t += 1
            
        if self.t <= 120:
            self.angle = 0
            self.xvel = 0
            self.yvel = -self.idle_vel
        elif self.t > 120 and self.t <= 240:
            self.angle = ((self.t-120)/120)*-90
            self.xvel = 0
            self.yvel = 0
            self.rotate()
        elif self.t > 240 and self.t <= 360:
            self.angle = 270
            self.xvel = self.idle_vel 
            self.yvel = 0
        elif self.t > 360 and self.t <= 480:
            self.angle = ((self.t-240)/120)*-90
            self.xvel = 0
            self.yvel = 0
            self.rotate()
        elif self.t > 480 and self.t <= 600:
            self.angle = 180
            self.xvel = 0
            self.yvel = self.idle_vel
        elif self.t > 600 and self.t <= 720:
            self.angle = ((self.t-360)/120)*-90
            self.xvel = 0
            self.yvel = 0
            self.rotate()
        elif self.t > 720 and self.t <= 840:
            self.angle = 90
            self.xvel = -self.idle_vel
            self.yvel = 0
        else:
            self.angle = ((self.t-480)/120)*-90
            self.xvel = 0
            self.yvel = 0
            self.rotate()
            
        #self.rotate()
            
    def square_move_2(self, timer):#would need to reset idle when not updating as timer would tick when not moving making it janky
        #timer = get_timer()
        
        if self.idle == False:
            self.idle_start_time = timer
            self.idle = True   
            
        if timer <= self.idle_start_time + 120:
            self.angle = 0
            self.xvel = 0
            self.yvel = -1
        elif timer <= self.idle_start_time + 240:
            self.angle = ((timer-self.idle_start_time-120)/120)*-90
            self.xvel = 0
            self.yvel = 0
            self.rotate()
        elif timer <= self.idle_start_time + 360:
            self.angle = 270
            self.xvel = 1
            self.yvel = 0
        elif timer <= self.idle_start_time + 480:
            self.angle = ((timer-self.idle_start_time-240)/120)*-90
            self.xvel = 0
            self.yvel = 0
            self.rotate()
        elif timer <= self.idle_start_time + 600:
            self.angle = 180
            self.xvel = 0
            self.yvel = 1
        elif timer <= self.idle_start_time + 720:
            self.angle = ((timer-self.idle_start_time-360)/120)*-90
            self.xvel = 0
            self.yvel = 0
            self.rotate()
        elif timer <= self.idle_start_time + 840:
            self.angle = 90
            self.xvel = -1
            self.yvel = 0
        elif timer <= self.idle_start_time + 959:
            self.angle = ((timer-self.idle_start_time-480)/120)*-90
            self.xvel = 0
            self.yvel = 0
            self.rotate()
        else:
            self.angle = ((timer-self.idle_start_time-480)/120)*-90
            self.xvel = 0
            self.yvel = 0
            self.rotate()
            self.idle = False
            
    def rotate(self):
        pass

#enemy spawners(factories)
class Spawner(Object):
    def __init__(self, x, y, display, image, s_type, num):
       super().__init__(x, y, display, image)
       self.health = 50
       self.healthmax = 50
       self.s_type = s_type
       self.spawn_timer = 0
       self.e_count = 0
       self.e_count_max = 20
       self.num = num
       self.type = "spawner"
       # self.save_vals.extend(['s_type', 'spawn_timer', 'e_count', 'e_count_max', 'num'])
       
    def create_zombie(self, e_group):#, camera):
        zombie = Zombie(self.pos.x, self.pos.y)#, self.display, zmbhd, zmbrm, True, self.num)
        e_group.add(zombie)
        # camera.add(zombie)

    def create_skeleton(self, e_group):#, camera):
        skeleton = Skeleton(self.pos.x, self.pos.y)#, self.display, sklhd, sklrm, True, self.num)
        e_group.add(skeleton)
        # camera.add(skeleton)
        
    def create_ghost(self, e_group):#, camera):
        ghost = Ghost(self.pos.x, self.pos.y, self.display, gsthdV, gstrmV, gsttlAnim)
        e_group.add(ghost)
        # camera.add(ghost)

# def create_enemy(self):
#    self.spawn_timer += 1
#    if self.spawn_timer >= 300:
#        exec("%s = %d" % (self.s_type, self.s_type(self.pos.x, self.pos.y, display, )

#zombie + skeleton spawner
class Grave(Spawner):#Object):
    def __init__(self, x, y, display = display, image = grvstn, s_type = 0, num = 0):#, s_type):
        super().__init__(x, y, display, image, s_type, num)
        self.scal_image = pygame.transform.scale(self.image, (sprite_scale*48, sprite_scale*64))
        self.rot_image = self.scal_image
        self.rect = self.rot_image.get_rect(center = (round(self.pos.x), round(self.pos.y)))
        self.hitbox = self.scal_image.get_rect(center = (round(self.pos.x), round(self.pos.y)))
        #self.s_type = s_type
        self.health = 50
        self.healthmax = 50
        # self.spawn_timer = 0
        # self.e_count = 0
        self.e_count_max = 20
        self.s_spawn = False
        # self.num = num
        # self.spawn_list = [self.create_zombie, self.create_skeleton]
        self.spawn_list = [super().create_zombie, super().create_skeleton]
        # self.save_vals.extend(['s_spawn'])

    def update(self, e_group, p, c_group, offset):#, camera):
        self.die(p, c_group)#, camera)
        self.create(e_group)#, camera)
        #self.render()
        self.render_bars(offset)

    def create_coin(self, x, y, c_group):#, camera):
        super().create_coin(x, y, c_group)#, camera)

    def create_ammo(self, x, y, c_group):#, camera):
        super().create_ammo(x, y, c_group)#, camera)

    def die(self, p, c_group):#, camera):
        super().die(p, c_group)#, camera)

    def create(self, e_group):#, camera):
        self.spawn_timer += 1
        if self.spawn_timer >= 300 and self.e_count < self.e_count_max:
            # spawn_list = [self.create_zombie, self.create_skeleton]
            random.choice(self.spawn_list)(e_group)#, camera)#randomly chooses which function to perform
            self.e_count += 1
            self.spawn_timer = 0
            
    # def create_grave(self, s_group, camera):
    #     grave = Grave(self.pos.x, self.pos.y)
    #     s_group.add(grave)
    #     camera.add(grave)

    # def create_zombie(self, e_group):
    #     zombie = Zombie(self.pos.x, self.pos.y, self.display, zmbhd, zmbrm, True, self.num)
    #     e_group.add(zombie)
    #     camera.add(zombie)

    # def create_skeleton(self, e_group):
    #     skeleton = Skeleton(self.pos.x, self.pos.y, self.display, sklhd, sklrm, True, self.num)
    #     e_group.add(skeleton)
    #     camera.add(skeleton)
    
    # def create_zombie(self, e_group, camera):
    #     super().create_zombie(e_group, camera)
        
    # def create_skeleton(self, e_group, camera):
    #     super().create_skeleton(e_group, camera)

    def render_bars(self, offset):
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
        pygame.draw.rect(self.display, dark_red, pygame.Rect(hpbar_b_left, hpbar_b_top, hpbar_b_width, hpbar_b_height))
        pygame.draw.rect(self.display, red, pygame.Rect(hpbar_p_left, hpbar_p_top, hpbar_p_width, hpbar_p_height))

    def render(self):
        self.render_bars()
        self.display.blit(self.rot_image, self.rect)
                           
#enemies
class Enemy(Entity):
    def __init__(self, x, y, display, image, arm):
        super().__init__(x, y, display, image, arm)
        self.sight = 700 * sprite_scale
        self.vel = 3
        self.idle = False
        self.idle_start_time = 0
        # self.save_vals.extend(['sight', 'idle', 'idle_start_time'])

    def sync(self):
        super().sync()

    def die(self, p, c_group, s_group):#, camera):
        super().die(p, c_group, s_group)#, camera)
        #if self.s_spawn:
        #    s_group[self.s_num].e_count -= 1

    def create_coin(self, x, y, c_group):#, camera):
        super().create_coin(x, y, c_group)#, camera)

    def create_ammo(self, x, y, c_group):#, camera):
        super().create_ammo(x, y, c_group)#, camera)

    def tile_collisions(self, tiles):
        for t in tiles:
            #collision of impassible tiles
            if t.t_type in self.collidable_tiles:
                #x axis collisions
                if t.rect.colliderect(self.hitbox.topleft[0] + (self.xvel * sprite_scale * 1.1), self.hitbox.topleft[1], self.hitbox.topright[0]-self.hitbox.topleft[0], self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                    if self.xvel > 0:
                        self.xvel = t.rect.left - self.hitbox.left
                        self.xvel = 0
                    elif self.xvel < 0:
                        self.xvel = self.hitbox.right - t.rect.right
                        self.xvel = 0
                #y axis collisions
                if t.rect.colliderect(self.hitbox.topleft[0], self.hitbox.topleft[1] + (self.yvel * sprite_scale * 1.1), self.hitbox.topright[0]-self.hitbox.topleft[0], self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                    if self.yvel < 0:
                        self.yvel = self.hitbox.bottom - t.rect.bottom
                        self.yvel = 0
                    elif self.yvel > 0:
                        self.yvel = t.rect.top - self.hitbox.top
                        self.yvel = 0
                        
            #collision of speed changing tiles
            if t.speed_mult != 1:
                if t.rect.collidepoint(self.pos):
                    #changes speed when on tile
                    self.xvel *= t.speed_mult
                    self.yvel *= t.speed_mult
                
    def door_collisions(self, i_group):
        for d in i_group:
            #collision of doors
            if d.type == "door":
                #x axis collisions
                if d.rect.colliderect(self.hitbox.topleft[0] + (self.xvel * sprite_scale * 1.1), self.hitbox.topleft[1], self.hitbox.topright[0]-self.hitbox.topleft[0], self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                    if self.xvel > 0:
                        self.xvel = d.rect.left - self.hitbox.left
                        self.xvel = 0
                    elif self.xvel < 0:
                        self.xvel = self.hitbox.right - d.rect.right
                        self.xvel = 0
                #y axis collisions
                if d.rect.colliderect(self.hitbox.topleft[0], self.hitbox.topleft[1] + (self.yvel * sprite_scale * 1.1), self.hitbox.topright[0]-self.hitbox.topleft[0], self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                    if self.yvel < 0:
                        self.yvel = self.hitbox.bottom - d.rect.bottom
                        self.yvel = 0
                    elif self.yvel > 0:
                        self.yvel = d.rect.top - self.hitbox.top
                        self.yvel = 0
                        
    def enemy_collision(self, enemies):#not done yet
        for e in enemies.sprites():#is .sprites() needed?
            if e.pos != self.pos and e.solid == True:
                if e.hitbox.colliderect(self.hitbox.topleft[0] + self.xvel, self.hitbox.topleft[1], self.hitbox.topright[0]-self.hitbox.topleft[0], self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
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
                #y axis collisions
                if e.hitbox.colliderect(self.hitbox.topleft[0], self.hitbox.topleft[1] + self.yvel, self.hitbox.topright[0]-self.hitbox.topleft[0], self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
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

                self.push(e)

    def player_collision(self, p):#improve (there is a bit of sticking due equalling the speeds)
        if p.hitbox.colliderect(self.hitbox.topleft[0] + self.xvel, self.hitbox.topleft[1], self.hitbox.topright[0]-self.hitbox.topleft[0], self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
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
        #y axis collisions
        if p.hitbox.colliderect(self.hitbox.topleft[0], self.hitbox.topleft[1] + self.yvel, self.hitbox.topright[0]-self.hitbox.topleft[0], self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
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

        self.push(p)

    def push(self, p):
        dist = self.pos.distance_to(p.pos)
        if dist < 12:
            self.yvel += 1
            
    def move_to_player(self, p):
        direction = (p.pos - self.pos).normalize()
        self.xvel =  direction[0] * self.vel
        self.yvel = direction[1] * self.vel
                    
#ghost
class Ghost(Enemy):
    def __init__(self, x, y, display = display, image = gsthdV, arm = gstrmV, tail = gsttlAnim, s_spawn = False, s_num = 0):
        super().__init__(x, y, display, image, arm)
        self.type = "tailed_entity"
        self.anim = tail
        self.tail = self.anim[0]
        self.scal_tail = pygame.transform.scale(self.tail, (sprite_scale*18, sprite_scale*54))
        self.rot_tail = self.scal_tail
        self.tail_rect = self.scal_tail.get_rect(center = (round(self.pos.x), round(self.pos.y)))
        self.vel = 2
        self.health = 15
        self.healthmax = 15
        #self.s_spawn = s_spawn
        #self.s_num = s_num
        self.sight = 800 * sprite_scale
        self.anim_t = 0
        self.anim_spd = 0
        self.solid = False
        self.hp_bar_p = pygame.Rect((0, 0), (0, 0))
        self.hp_bar_b = pygame.Rect((0, 0), (0, 0))
        self.damage = 10
        self.angle = 0
        self.attack_timer = 0
        self.attack_dist = 20
        # self.save_vals.extend(['anim_spd', 'damage', 'angle', 'attack_timer', 'attack_dist'])
        
    def update(self, p, tiles, dist, c_group, s_group, offset):#, camera):
        self.dirty = 1
        self.die(p, c_group, s_group)#, camera)
        #self.timer()
        self.move(p, tiles, dist)
        self.tail_anim()
        self.attack(p, dist)
        self.render_bars(offset)
        #self.render()
        
    def move(self, p, tiles, dist):
        if dist <= self.sight:
            self.anim_spd = 1.2
            self.idle = False
            self.chase_player(p)
            
        else:
            self.anim_spd = 0.2
            # self.idle = True
            self.idle_move()
            
        self.tile_collisions(tiles)
        self.sync()
            
    # def idle(self):
    #     if not self.idle:
    #         self.change_idling = True
        
    #     if self.changing_idling == True:
    #         self.idle = not self.idle
    #         self.change_idling = False

    def tile_collisions(self, tiles):
        for t in tiles:
            if t.t_type == "portal":
                if t.rect_1.colliderect(self.hitbox):
                    self.health -= 1
                elif t.rect_2.colliderect(self.hitbox):
                    self.health -= 1
            elif t.t_type == "b_portal":
                if t.rect.colliderect(self.hitbox):
                    self.health -= 1

    def attack(self, p, dist):
        if dist <= self.attack_dist and not(p.respawn_protection):
            self.attack_timer += 1
            if self.attack_timer >= 45:
                self.attack_timer = 0
                self.angle += 20
                self.rotate()
                p.health -= self.damage

    # def timer(self):
    #     if self.t >= 960:
    #         self.t = 0
    #     else:
    #         self.t += 1

    def tail_anim(self):
        if self.anim_t >= 16:
            self.anim_t = 0
        else:
            self.anim_t += self.anim_spd
            
        if self.anim_t < 2:
            x = 0
        elif self.anim_t >= 2 and self.anim_t < 4:
            x = 1
        elif self.anim_t >= 4 and self.anim_t < 6:
            x = 2
        elif self.anim_t >= 6 and self.anim_t < 8:
            x = 3
        elif self.anim_t >= 8 and self.anim_t < 10:
            x = 4
        elif self.anim_t >= 10 and self.anim_t < 12:
            x = 5
        elif self.anim_t >= 12 and self.anim_t < 14:
            x = 6
        else:
            x = 7

        self.tail = self.anim[x]
        self.scal_tail = pygame.transform.scale(self.tail, (sprite_scale*18, sprite_scale*54))
        self.rotate()
        

    def idle_move(self):
        # self.square_move()
        self.random_move()

    # def move_to_player(self, p):#change to a better movement
    #     if (p.pos.x + 3) >= self.pos.x and (p.pos.x - 3) <= self.pos.x:
    #         self.xvel = 0
    #     elif (p.pos.x - 3) > self.pos.x:
    #         self.xvel = self.vel
    #     elif (p.pos.x + 3) < self.pos.x:
    #         self.xvel = -self.vel
            
    #     if (p.pos.y + 3) >= self.pos.y and (p.pos.y - 3) <= self.pos.y:
    #         self.yvel = 0
    #     elif (p.pos.y - 3) > self.pos.y:
    #         self.yvel = self.vel
    #     elif (p.pos.y + 3) < self.pos.y:
    #         self.yvel = -self.vel
            
    #     if abs(self.xvel) ==  abs(self.yvel) and self.xvel != 0:
    #         abs_vel = (self.vel/root_2)
    #         self.xvel = (self.xvel/self.vel) * abs_vel
    #         self.yvel = (self.yvel/self.vel) * abs_vel
            
    def move_to_player(self, p):
        super().move_to_player(p)

    def rotatehead(self):
        self.rot_image = pygame.transform.rotate(self.scal_image, self.angle)
        self.rect = self.rot_image.get_rect(center = self.rect.center)

    def rotatearms(self):
        self.rot_arm = pygame.transform.rotate(self.scal_arm, self.angle)
        self.arm_rect = self.rot_arm.get_rect(center = self.arm_rect.center)

    def rotatetail(self):
        self.rot_tail = pygame.transform.rotate(self.scal_tail, self.angle)
        self.tail_rect = self.rot_tail.get_rect(center = self.tail_rect.center)

    def rotate(self):
        self.rotatehead()
        self.rotatearms()
        self.rotatetail()

    def chase_player(self, p):
        dx, dy = self.pos.x - p.pos.x, self.pos.y - p.pos.y
        self.angle = math.degrees(math.atan2(dx, dy))
        self.rotate()
        self.move_to_player(p)

    def render_bars(self, offset):
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
        pygame.draw.rect(self.display, dark_red, pygame.Rect(hpbar_b_left, hpbar_b_top, hpbar_b_width, hpbar_b_height))
        pygame.draw.rect(self.display, red, pygame.Rect(hpbar_p_left, hpbar_p_top, hpbar_p_width, hpbar_p_height))

    def render(self):
        self.display.blit(self.rot_arm, self.arm_rect)
        self.display.blit(self.rot_tail, self.tail_rect)
        self.display.blit(self.rot_image, self.rect)
        self.render_bars()
        
    def random_move(self):
        super().random_move()
        
    def square_move(self):
        super().square_move()
        
    def die(self, p, c_group, s_group):#, camera):
        super().die(p, c_group, s_group)#, camera)
        
    def create_coin(self, x, y, c_group):#, camera):
        super().create_coin(x, y, c_group)#, camera)

    def create_ammo(self, x, y, c_group):#, camera):
        super().create_ammo(x, y, c_group)#, camera)

    def sync(self):
        super().sync()
        self.tail_rect.center = self.pos.x, self.pos.y

    def idle_sync(self):
        super().idle_sync()
        self.tail_rect.center = self.pos.x, self.pos.y

#skeleton
class Skeleton(Enemy):
    def __init__(self, x, y, display = display, image = sklhd, arm = sklrm, s_spawn = False, s_num = 0):#, t, s_spawn, s_num):
        super().__init__(x, y, display, image, arm)
        self.sight = 600 * sprite_scale
        #self.s_spawn = s_spawn
        #self.s_num = s_num
        self.attack_dist = self.sight / 2
        self.attack_timer = 0
        self.angle = 0
        self.vel = 3
        self.vel_back = 2
        self.collidable_tiles = ["wall", "tree"]
        # self.save_vals.extend(['attack_dist', 'attack_timer', 'angle', 'vel_back', 'collidable_tiles'])

    def update(self, p, tiles, dist, c_group, s_group, b_group, e, offset, i_group):#, camera):
        self.dirty = 1
        self.die(p, c_group, s_group)#, camera)
        self.move(p, tiles, dist, e, i_group)
        self.attack(p, dist, b_group)#, camera)
        self.render_bars(offset)
        #self.render()
        
    def move(self, p, tiles, dist, e, i_group):
        if dist <= self.sight:
            self.idle = False
            self.chase_player(p, dist)
            
        else:
            # self.idle = True
            self.idle_move()
            
        self.player_collision(p)
        self.enemy_collision(e)
        self.tile_collisions(tiles)
        self.door_collisions(i_group)
        
        self.sync()

    def attack(self, p, dist, b_group):#, camera):
        if dist <= self.attack_dist and not(p.respawn_protection):
            self.attack_timer += 1
            if self.attack_timer >= 20:
                self.attack_timer = 0
                self.create_bullet(b_group)#, camera)

    def idle_move(self):
        # self.square_move()
        self.random_move()

    def move_to_player(self, p):
        super().move_to_player(p)

    def move_around_player(self, p, dist):
        if dist >= 152*sprite_scale:
            self.move_to_player(p)

        elif dist > 148*sprite_scale and dist < 152*sprite_scale:
            self.xvel = self.yvel = 0
            
        elif dist <= 148*sprite_scale:
            if (p.pos.x + 3) >= self.pos.x and (p.pos.x - 3) <= self.pos.x:
                self.xvel = 0
            elif (p.pos.x - 3) > self.pos.x:
                self.xvel = -self.vel_back
            elif (p.pos.x + 3) < self.pos.x:
                self.xvel = self.vel_back
                
            if (p.pos.y + 3) >= self.pos.y and (p.pos.y - 3) <= self.pos.y:
                self.yvel = 0
            elif (p.pos.y - 3) > self.pos.y:
                self.yvel = -self.vel_back
            elif (p.pos.y + 3) < self.pos.y:
                self.yvel = self.vel_back
                
            if abs(self.xvel) == abs(self.yvel) and self.xvel != 0:
                abs_vel = (self.vel_back/root_2)
                self.xvel = (self.xvel/self.vel_back) * abs_vel
                self.yvel = (self.yvel/self.vel_back) * abs_vel

    def create_bullet(self, b_group):#, camera):
        bullet = Bullet(self.pos.x, self.pos.y, angle = self.angle, b_type = "skeleton")
        b_group.add(bullet)
        # camera.add(bullet)

    def rotatehead(self):
        self.rot_image = pygame.transform.rotate(self.scal_image, self.angle)
        self.rect = self.rot_image.get_rect(center = self.rect.center)

    def rotatearms(self):
        self.rot_arm = pygame.transform.rotate(self.scal_arm, self.angle)
        self.arm_rect = self.rot_arm.get_rect(center = self.arm_rect.center)

    def rotate(self):
        self.rotatehead()
        self.rotatearms()

    def chase_player(self, p, dist):
        dx, dy = self.pos.x - p.pos.x, self.pos.y - p.pos.y
        self.angle = math.degrees(math.atan2(dx, dy))
        self.rotate()
        self.move_around_player(p, dist)

    def render_bars(self, offset):
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
        pygame.draw.rect(self.display, dark_red, pygame.Rect(hpbar_b_left, hpbar_b_top, hpbar_b_width, hpbar_b_height))
        pygame.draw.rect(self.display, red, pygame.Rect(hpbar_p_left, hpbar_p_top, hpbar_p_width, hpbar_p_height))

    def render(self):
        self.display.blit(self.rot_arm, self.arm_rect)
        self.display.blit(self.rot_image, self.rect)
        self.render_bars()
        
    def square_move(self):
        super().square_move()
        
    def create_coin(self, x, y, c_group):#, camera):
        super().create_coin(x, y, c_group)#, camera)

    def create_ammo(self, x, y, c_group):#, camera):
        super().create_ammo(x, y, c_group)#, camera)

    def die(self, p, c_group, s_group):#, camera):
        super().die(p, c_group, s_group)#, camera)

    def player_collision(self, p):
        super().player_collision(p)

    def enemy_collision(self, e):
        super().enemy_collision(e)

    def sync(self):
        super().sync()

    def idle_sync(self):
        super().idle_sync()

    def tile_collisions(self, tiles):
        super().tile_collisions(tiles)

    def door_collisions(self, i_group):
        super().door_collisions(i_group)

#zombie
class Zombie(Enemy):
    def __init__(self, x, y, display = display, image = zmbhd, arm = zmbrm, s_spawn = False, s_num = 0):
        super().__init__(x, y, display, image, arm)
        self.damage = 5
        self.angle = 0
        self.vel = 3
        self.attack_timer = 0
        self.attack_dist = 25
        self.sight = 700 * sprite_scale
        self.collidable_tiles = ["wall", "tree"]
        # self.save_vals.extend(['damage', 'angle', 'attack_timer', 'attack_dist', 'collidable_tiles'])
        
    def update(self, p, tiles, dist, c_group, s_group, b_group, e, offset, i_group):#, camera):
        self.dirty = 1
        self.die(p, c_group, s_group)#, camera)
        self.move(p, tiles, dist, e, i_group)
        self.attack(p, dist)
        self.render_bars(offset)
        #self.render()
        
    def move(self, p, tiles, dist, e, i_group):
        if dist <= self.sight:
            self.idle = False
            self.chase_player(p)
        
        else:
            # self.idle = True
            self.idle_move()
            
        self.player_collision(p)
        self.enemy_collision(e)
        self.tile_collisions(tiles)
        self.door_collisions(i_group)
        
        self.sync()

        #self.push(p)

    def attack(self, p, dist):
        if dist <= self.attack_dist and not(p.respawn_protection):
            self.attack_timer += 1
            if self.attack_timer >= 30:
                self.attack_timer = 0
                self.angle += 20
                self.rotate()
                p.health -= self.damage

    def die(self, p, c_group, s_group):#, camera):
        super().die(p, c_group, s_group)#, camera)

    #def push(self, p):
        #super().push(p)

    def tile_collisions(self, tiles):
        super().tile_collisions(tiles)

    def door_collisions(self, i_group):
        super().door_collisions(i_group)

    def idle_move(self):
        # self.square_move()
        self.random_move()

    # def move_to_player(self, p):#change to a better movement
    #     if (p.pos.x + 3) >= self.pos.x and (p.pos.x - 3) <= self.pos.x:
    #         self.xvel = 0
    #     elif (p.pos.x - 3) > self.pos.x:
    #         self.xvel = self.vel
    #     elif (p.pos.x + 3) < self.pos.x:
    #         self.xvel = -self.vel
            
    #     if (p.pos.y + 3) >= self.pos.y and (p.pos.y - 3) <= self.pos.y:
    #         self.yvel = 0
    #     elif (p.pos.y - 3) > self.pos.y:
    #         self.yvel = self.vel
    #     elif (p.pos.y + 3) < self.pos.y:
    #         self.yvel = -self.vel
            
    #     if abs(self.xvel) == abs(self.yvel) and self.xvel != 0:
    #         abs_vel = (self.vel/root_2)
    #         self.xvel = (self.xvel/self.vel) * abs_vel
    #         self.yvel = (self.yvel/self.vel) * abs_vel
            
    def move_to_player(self, p):
        super().move_to_player(p)

    def rotatehead(self):
        self.rot_image = pygame.transform.rotate(self.scal_image, self.angle)
        self.rect = self.rot_image.get_rect(center = self.rect.center)

    def rotatearms(self):
        self.rot_arm = pygame.transform.rotate(self.scal_arm, self.angle)
        self.arm_rect = self.rot_arm.get_rect(center = self.arm_rect.center)

    def rotate(self):
        self.rotatehead()
        self.rotatearms()

    def chase_player(self, p):
        dx, dy = self.pos.x - p.pos.x, self.pos.y - p.pos.y
        self.angle = math.degrees(math.atan2(dx, dy))
        self.rotate()
        self.move_to_player(p)

    def take_damage(self):
        pass

    def render_bars(self, offset):
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
        pygame.draw.rect(self.display, dark_red, pygame.Rect(hpbar_b_left, hpbar_b_top, hpbar_b_width, hpbar_b_height))
        pygame.draw.rect(self.display, red, pygame.Rect(hpbar_p_left, hpbar_p_top, hpbar_p_width, hpbar_p_height))

    def render(self):
        self.display.blit(self.rot_arm, self.arm_rect)
        self.display.blit(self.rot_image, self.rect)
        self.render_bars()
        
    def square_move(self):
        super().square_move()
        
    def create_coin(self, x, y, c_group):#, camera):
        super().create_coin(x, y, c_group)#, camera)

    def create_ammo(self, x, y, c_group):#, camera):
        super().create_ammo(x, y, c_group)#, camera)

    def player_collision(self, p):
        super().player_collision(p)

    def enemy_collision(self, e):
        super().enemy_collision(e)

    def sync(self):
        super().sync()

    def idle_sync(self):
        super().idle_sync()

#player
class Player(Entity):
    def __init__(self, x, y, display = display, image = plrhd, arm = plrrm, lives = 3):
        super().__init__(x, y, display, image, arm)
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
        self.regen_energy = False
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
        self.lives = lives
        self.z = 5
        self.portal_cost = 10
        self.respawn_protection = False
        self.respawn_protection_timer = 0
        self.collidable_tiles = ["wall", "tree"]
        self.vel = 4
        self.hp_textbox = textbox((d_width*0.5), (d_height * 0.96), int(d_height*0.02), white, display)
        self.ep_textbox = textbox((d_width*0.5), (d_height * 0.92), int(d_height*0.02), white, display)
        # self.level = 0
        self.prev_score = 0
        self.prev_kills = 0
        self.prev_bullets = self.bullets
        self.prev_cash = 0
        self.deaths = 0
        self.is_new_press = True
        self.dir = pygame.math.Vector2(0,0)
        # self.path = []
        # my_list = []
        # for num in range(0,0):
        #     list.append(num)
        # print(my_list)
        self.hrt_rects = []
        for i in range(0, self.lives):
            hrt_rect = hrt.get_rect(topleft = (round(d_width - 48 - (i*33)), 15))
            self.hrt_rects.append(hrt_rect)
            # print(repr(self.hrt_rects))
            
        # self.save_vals = ['solid', 'health', 'healthmax', 'xvel', 'yvel', 'vel', 't', 'idle_vel', 'next_pos', 'collidable_tiles', 'weapon', 'angle', 'attack_timer', 'wait', 'healthregen', 'energyval', 'energyregen', 'energymax', 'sprintvelmult', 'footprint_timer', 'score', 'bullet_delay', 'cash', 'change_lvl', 'damage', 'kills', 'bullets', 'attack_dist', 'lives', 'portal_cost', 'respawn_protection', 'respawn_protection_timer']

        self.healthbarborder = pygame.Rect(d_width*0.2 - 3, d_height*0.96 - 3, d_width*0.6 + 6, d_height*0.02 + 6)
        self.healthbar = pygame.Rect(d_width*0.2, d_height*0.96, d_width*0.6, d_height*0.02)
        self.energybarborder = pygame.Rect(d_width*0.2 - 3, d_height*0.92 - 3, d_width*0.6 + 6, d_height*0.02 + 6)
        self.energybar = pygame.Rect(d_width*0.2, d_height*0.92, d_width*0.6, d_height*0.02)
        
    def update(self, moves, tiles, m_pos, portals, b_group, f_group, e_group, s_group, i_group, infobox):#, camera):
        # self.change_lvl = False
        #self.die()
        self.rotate_to_mouse(m_pos)
        self.move(moves, tiles, f_group, i_group, portals, infobox)#, camera)
        if self.bullet_delay < 7:
            self.bullet_delay += 1
        if moves[6]:
            self.change_weapon()
        self.attack_timer += 1
        if moves[5]:
            self.attack(m_pos, b_group, e_group, s_group)#, camera)
        #self.render()
        self.dirty = 1
        self.respawn()
        # return self.change_lvl

    def die(self):
        if self.health <= 0:
            self.lives -= 1
            self.deaths += 1
            if len(self.hrt_rects) > 0:
                del self.hrt_rects[-1]
            # self.pos = pygame.math.Vector2((200*sprite_scale, 200*sprite_scale))
            self.respawn_protection = True
            self.score = self.prev_score - 100
            self.health = self.healthmax
            self.energyval = self.energymax
            self.bullets = self.prev_bullets
            self.kills = self.prev_kills
            self.cash = self.prev_cash - 50
            if self.cash < 0:
                self.cash = 0
            if self.score < 0:
                self.score = 0
            return True
        
    def respawn(self):
        if self.respawn_protection:
            self.respawn_protection_timer += 1
            if self.respawn_protection_timer >= 30:
                self.respawn_protection = False
                self.respawn_protection_timer = 0

    def collectable_coll(self, c_group):
        for c in c_group:
            if self.hitbox.colliderect(c.rect):
                if c.c_type == "coin":
                    self.cash += c.value
                    c.kill()
                elif c.c_type == "weapon":
                    pass
                elif c.c_type == "consumable":
                    pass

    # def tile_collisions(self, portals, moves, tiles, infobox):
    #     for p in portals:
    #         if moves[7] and self.energyval >= self.portal_cost:
    #             if p.rect_1.colliderect(self.hitbox):
    #                 self.pos = p.pos_2 + (tile_scale/2, tile_scale/2)
    #                 self.energyval -= self.portal_cost
    #             elif p.rect_2.colliderect(self.hitbox):
    #                 self.pos = p.pos_1 + (tile_scale/2, tile_scale/2)
    #                 self.energyval -= self.portal_cost
    #     for t in tiles:
    #         if t.t_type == "b_portal" and moves[7]:
    #             if t.rect.colliderect(self.hitbox):
    #                 self.change_lvl = True
    #                 self.level += 1
    #                 self.prev_score = self.score
    #                 self.prev_kills = self.kills
    #                 self.prev_bullets = self.bullets
    #                 self.prev_cash = self.cash
    #                 self.pos.x = self.pos.y = 200
                    
    def tile_collisions(self, portals, moves, infobox, tiles, f_group):
        for p in portals:
            if p.rect_1.colliderect(self.hitbox):
                infobox.draw_c("Right click to travel")
                if moves[7] and self.energyval >= self.portal_cost:
                    self.pos = p.pos_2 + (tile_scale/2, tile_scale/2)
                    self.energyval -= self.portal_cost
            elif p.rect_2.colliderect(self.hitbox):
                infobox.draw_c("Right click to travel")
                if moves[7] and self.energyval >= self.portal_cost:
                    self.pos = p.pos_1 + (tile_scale/2, tile_scale/2)
                    self.energyval -= self.portal_cost
        
        #calculates which tile we are on
        tile_pos = self.pos//tile_scale
        tile = tiles[int(tile_pos.y)][int(tile_pos.x)]
        self.xvel *= tile.speed_mult
        self.yvel *= tile.speed_mult
        
        if tile.t_type == "mud":
            if tile.rect.colliderect(self.hitbox):
                self.footprint_timer += 1
                if self.footprint_timer >= 15:
                    self.footprint_timer = 0
                    self.create_m_footprint(f_group)
            
        elif tile.t_type == "snowy_grass":
            if tile.rect.colliderect(self.hitbox):
                self.footprint_timer += 1
                if self.footprint_timer >= 15:
                    self.footprint_timer = 0
                    self.create_s_footprint(f_group)
            
        elif tile.t_type == "b_portal":
            infobox.draw_c("Right click to go to next level")
            if moves[7]:
                self.change_lvl = True
                # self.level += 1
                self.prev_score = self.score
                self.prev_kills = self.kills
                self.prev_bullets = self.bullets
                self.prev_cash = self.cash
                # self.pos.x = self.pos.y = 200
        
        # for t in tile_group:
        #     if t.t_type == "b_portal" and t.rect.colliderect(self.hitbox):
        #         infobox.draw_c("Right click to go to next level")
        #         if moves[7]:
        #             self.change_lvl = True
        #             self.level += 1
        #             self.prev_score = self.score
        #             self.prev_kills = self.kills
        #             self.prev_bullets = self.bullets
        #             self.prev_cash = self.cash
        #             self.pos.x = self.pos.y = 200
                    
    # def tile_collisions(self, tiles, moves, f_group):#, camera):
    #     for t in tiles:
    #         #collision of impassible tiles
    #         if t.t_type in self.collidable_tiles:
    #             #x axis collisions
    #             if t.rect.colliderect(self.hitbox.topleft[0] + (self.xvel * sprite_scale * 1.1), self.hitbox.topleft[1], self.hitbox.topright[0]-self.hitbox.topleft[0], self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
    #                 if self.xvel > 0:
    #                     self.xvel = t.rect.left - self.hitbox.left
    #                     self.xvel = 0
    #                     # self.pos.x = self.pos.x + self.xvel - (self.hitbox.right + self.xvel - t.rect.left)
    #                     self.xvel = 0
    #                 elif self.xvel < 0:
    #                     # self.xvel = self.hitbox.right - t.rect.right
    #                     self.xvel = 0
    #             #y axis collisions
    #             elif t.rect.colliderect(self.hitbox.topleft[0], self.hitbox.topleft[1] + (self.yvel * sprite_scale * 1.1), self.hitbox.topright[0]-self.hitbox.topleft[0], self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
    #                 if self.yvel < 0:
    #                     # self.yvel = self.hitbox.bottom - t.rect.bottom
    #                     self.yvel = 0
    #                 elif self.yvel > 0:
    #                     # self.yvel = t.rect.top - self.hitbox.top
    #                     self.yvel = 0
                        
    #         elif t.t_type == "snowy_grass":
                # if t.rect.colliderect(self.hitbox):
                #     self.footprint_timer += 1
                #     if self.footprint_timer >= 15:
                #         self.footprint_timer = 0
                #         self.create_s_footprint(f_group)#, camera)
                        
    #         elif t.t_type == "mud":
                # if t.rect.colliderect(self.hitbox):
                #     self.footprint_timer += 1
                #     if self.footprint_timer >= 15:
                #         self.footprint_timer = 0
                #         self.create_m_footprint(f_group)#, camera)
                        
    #         elif t.t_type == "portal" and moves[7] and self.energyval >= 10:#t.timer == 90:
                # if t.rect_1.colliderect(self.hitbox):
                #     self.pos = t.pos_2 + (tile_scale/2, tile_scale/2)
                #     self.energyval -= self.portal_cost
                #     #t.timer = 0
                # elif t.rect_2.colliderect(self.hitbox):
                #     self.pos = t.pos_1 + (tile_scale/2, tile_scale/2)
                #     self.energyval -= self.portal_cost
                #     #t.timer = 0
                    
            # elif t.t_type == "b_portal" and moves[7]:
            #     if t.rect.colliderect(self.hitbox):
            #         self.change_lvl = True
            #         self.level += 1
            #         self.prev_score = self.score
            #         self.prev_kills = self.kills
            #         self.prev_bullets = self.bullets
            #         self.prev_cash = self.cash
            #         self.pos.x = self.pos.y = 200
            
    #         #collision of slowing tiles
    #         if t.speed_mult != 1:
    #             if t.rect.collidepoint(self.pos):
    #                 self.xvel = self.xvel * t.speed_mult
    #                 self.yvel = self.yvel * t.speed_mult
                    
    # def tile_collisions(self, tiles):#this adds all of them to list and sorts them, then checks if collidable until it is
    #     for data in self.path:
    #         if tiles[data[0]][data[1]].t_type in self.collidable_tiles:#or tiles[data[2]][data[3]].t_type in self.collidable_tiles:and *= data[4]
    #             # print(tiles[data[0]][data[1]].t_type)
    #             self.xvel *= data[2]
    #             self.yvel *= data[3]
    #             # print(f"Hitting tile {data[0]} {data[1]}")
    #             break
            
    # def tile_collisions(self, tiles):
    #     for pos in range(len(self.path)):
    #         if tiles[self.path[pos][0]][self.path[pos][1]].t_type in self.collidable_tiles:
    #             self.xvel *= self.path[pos][2]
    #             self.yvel *= self.path[pos][3]
    #             # try:
    #             #     if self.path[pos][4] == self.path[pos+1][4]:
    #             #         self.yvel *= self.path[pos][4]
    #             # except:
    #             #     pass
    #             break
    
    # def tile_collisions(self, r, c, ratio, tiles):#maybe add r2 and c2 #checks all if collidable, if it is then adds to list and sorts
    #     if tiles[r][c].t_type in self.collidable_tiles:#or tiles[r2][c2].t_type in self.collidable_tiles:
    #         self.path.append(ratio)
    
    # def x_tile_collisions(self, tiles):
    #     for data in self.path:
    #         if tiles[data[0]][data[1]].t_type in self.collidable_tiles:
    #             self.xvel *= data[2]
    #             break
                
    # def y_tile_collisions(self, tiles):
    #     for data in self.path:
    #         if tiles[data[0]][data[1]].t_type in self.collidable_tiles:
    #             self.yvel *= data[2]
    #             break
    
    # def x_tile_collisions(self, r, c, ratio, tiles):
    #     if tiles[r][c].t_type in self.collidable_tiles:
    #         self.xvel *= ratio
    #         # break
            
    # def y_tile_collision(self, r, c, ratio, tiles):
    #     if tiles[r][c].t_type in self.collidable_tiles:
    #         self.yvel *= ratio

    def door_collisions(self, i_group):
        for d in i_group:
            #collision of doors
            if d.type == "door":
                #x axis collisions
                if d.rect.colliderect(self.hitbox.topleft[0] + (self.xvel * sprite_scale * 1.1), self.hitbox.topleft[1], self.hitbox.topright[0]-self.hitbox.topleft[0], self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                    if self.xvel > 0:
                        self.xvel = d.rect.left - self.hitbox.left
                        self.xvel = 0
                    elif self.xvel < 0:
                        self.xvel = self.hitbox.right - d.rect.right
                        self.xvel = 0
                #y axis collisions
                if d.rect.colliderect(self.hitbox.topleft[0], self.hitbox.topleft[1] + (self.yvel * sprite_scale * 1.1), self.hitbox.topright[0]-self.hitbox.topleft[0], self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                    if self.yvel < 0:
                        self.yvel = self.hitbox.bottom - d.rect.bottom
                        self.yvel = 0
                    elif self.yvel > 0:
                        self.yvel = d.rect.top - self.hitbox.top
                        self.yvel = 0

    def move(self, moves, tiles, f_group, i_group, portals, infobox):#, camera):#this should be moved after all speed changes if speed is set to a specific value by something
        # if moves[0] and not moves[1]:
        #     self.yvel = -self.vel
        # elif moves[1] and not moves[0]:
        #     self.yvel = self.vel
        # elif moves[0] and moves[1]:
        #     self.yvel = 0
        # else:
        #     self.yvel = 0
            
        # if moves[2] and not moves[3]:
        #     self.xvel = -self.vel
        # elif moves[3] and not moves[2]:
        #     self.xvel = self.vel
        # elif moves[2] and moves[3]:
        #     self.xvel = 0
        # else:
        #     self.xvel = 0
        
        self.yvel = 0#this should change if I have ice tiles
        if moves[0]:
            self.yvel -= self.vel
        if moves[1]:
            self.yvel += self.vel
            
        self.xvel = 0
        if moves[2]:
            self.xvel -= self.vel
        if moves[3]:
            self.xvel += self.vel
            
        if abs(self.xvel) == abs(self.yvel) and self.xvel != 0:#just do if self.xvel != 0 and self.yvel != 0
            abs_vel = (self.vel/root_2)
            self.xvel = (self.xvel/self.vel) * abs_vel
            self.yvel = (self.yvel/self.vel) * abs_vel
        # self.xvel = 4
        # self.yvel = -4

        # self.collisions(tiles)

        self.sprint(moves)
        self.tile_collisions(portals, moves, infobox, tiles, f_group)
        # self.tile_collisions(tiles, moves, f_group, camera)
        # self.collisions(tiles)
        self.calc_path_better(tiles)
        # self.collisions(tiles)
        self.door_collisions(i_group)

        self.sync()
        
    # def collisions(self, tiles):
    #     # if self.xvel != 0 and self.yvel != 0:
    #     self.calc_path()
            
    #     self.tile_collisions(tiles)
    
    #calculates the matrix position for tiles that will be collided and puts them in a list, in order of dist to the tile
    # def calc_path(self):#might be able to just use pos instead of rect sides if vel is always bigger than half the hitbox width
    #     self.path.clear()
        
    #     if self.xvel > 0:
    #         #first column crossing on path
    #         current_c = int(self.hitbox.right / tile_scale)#could also just do from left // tile_scale + 1 or do (self.hitbox.right - 1) // tile_scale + 1
    #         if self.hitbox.right / tile_scale == current_c:#if right of hitbox is on a column (only needed if I set the position to be touching the tile)
    #             first_c = current_c
    #         else:
    #             first_c = current_c + 1
                
    #         #calculates tile matrix pos for column crossing on path
    #         for x in range(first_c * tile_scale, int(self.hitbox.right + self.xvel)+1, tile_scale):
    #                 # print()
    #                 ratio = (x - self.hitbox.right) / self.xvel
    #                 top_r = int(((ratio * self.yvel) + self.hitbox.top) / tile_scale)#+1 on middle if 48 vel doesn't work
    #                 num = ((ratio * self.yvel) + self.hitbox.bottom) / tile_scale#could just do (height/tile_scale) + top_r if not int?
    #                 bottom_r = int(num)
    #                 if num != bottom_r:
    #                     bottom_r += 1
    #                 c = int(x / tile_scale)
    #                 for r in range(top_r, bottom_r):#maybe instead do from top_r to int(height / tile_scale + 1)
    #                     self.path.append((r, c, ratio, 1, ratio))
                    
    #         #moving right and up (+x, -y)
    #         if self.yvel < 0:#last row crossing on path
    #             last_r = int((self.hitbox.top + self.yvel) / tile_scale + 1)#maybe do no +1 and \/
                
    #             #if it doesn't work do this and do * tile_scale above and do if does work
    #             # if first_c > self.hitbox.right + self.xvel:
                
    #             #if does work maybe do and/or do * tile_scale above
    #             # ratio = (first_c-self.hitbox.right)/self.xvel
    #             # self.path.append(((self.hitbox.top - (ratio * self.yvel)) // tile_scale, first_c, ratio))
                
    #             #calculates tile matrix pos for column crossing on path
    #             # for x in range(first_c * tile_scale, int(self.hitbox.right + self.xvel)+1, tile_scale):#+1 on middle if 48 vel doesn't work
    #             #     ratio = (x - self.hitbox.right) / self.xvel
    #             #     top_r = int((self.hitbox.top + (ratio * self.yvel)) / tile_scale)
    #             #     num = (self.hitbox.bottom + (ratio * self.yvel)) / tile_scale#could just do (height/tile_scale) + top_r if not int?
    #             #     bottom_r = int(num)
    #             #     if num != bottom_r:
    #             #         bottom_r += 1
    #             #     c = int(x / tile_scale)
    #             #     for r in range(top_r, bottom_r):#maybe instead do from top_r to int(height / tile_scale + 1)
    #             #         self.path.append((r, c, ratio, 1, ratio))
                    
                
    #             #calculates tile matrix pos for row crossing on path
    #             for y in range(last_r * tile_scale, int(self.hitbox.top)+1, tile_scale):#maybe check for if top is already touching ,+1 on middle if 48+ vel doesn't work or do from bottom
    #                 ratio = (y - self.hitbox.top) / self.yvel
    #                 r = int((y / tile_scale) - 1)#and maybe do no -1
    #                 left_c = int(((ratio * self.xvel) + self.hitbox.left) / tile_scale)
    #                 num = ((ratio * self.xvel) + self.hitbox.right) / tile_scale
    #                 right_c = int(num)
    #                 if num != right_c:
    #                     right_c += 1
    #                 for c in range(left_c, right_c):#this should then be width // tile_scale + 1
    #                     self.path.append((r, c, 1, ratio, ratio))
        
    #         #moving right and down (+x, +y)
    #         elif self.yvel > 0:
    #             #first row crossing on path
    #             current_r = int(self.hitbox.bottom / tile_scale)
    #             if self.hitbox.bottom / tile_scale == current_r:
    #                 first_r = current_r
    #             else:
    #                 first_r = current_r + 1
    #             # print(first_r)
    #             #calculates tile matrix pos for column crossing on path
    #             # for x in range(first_c * tile_scale, int(self.hitbox.right + self.xvel)+1, tile_scale):
    #             #     # print()
    #             #     ratio = (x - self.hitbox.right) / self.xvel
    #             #     top_r = int(((ratio * self.yvel) + self.hitbox.top) / tile_scale)
    #             #     num = ((ratio * self.yvel) + self.hitbox.bottom) / tile_scale
    #             #     bottom_r = int(num)
    #             #     if num != bottom_r:
    #             #         bottom_r += 1
    #             #     c = int(x / tile_scale)
    #             #     for r in range(top_r, bottom_r):
    #             #         self.path.append((r, c, ratio, 1, ratio))
                
    #             #calculates tile matrix pos for row crossing on path
    #             for y in range(first_r * tile_scale, int(self.hitbox.bottom + self.yvel)+1, tile_scale):
    #                 ratio = (y - self.hitbox.bottom) / self.yvel
    #                 r = int(y / tile_scale)
    #                 left_c = int(((ratio * self.xvel) + self.hitbox.left) / tile_scale)
    #                 num = ((ratio * self.xvel) + self.hitbox.right) / tile_scale
    #                 right_c = int(num)
    #                 if num != right_c:
    #                     right_c += 1
    #                 for c in range(left_c, right_c):
    #                     # for pos in range(len(self.path)):
    #                     #     if ratio == self.path[pos][2]:
    #                     #         self.path[pos][3] = ratio
    #                     #     else:
    #                     self.path.append((r, c, 1, ratio, ratio))
                 
    #         #moving right (+x, 0)   
    #         else:
    #             #top row crossing path
    #             top_r = int(self.hitbox.top / tile_scale)
                
    #             #bottom row crossing path
    #             num = self.hitbox.bottom / tile_scale
    #             bottom_r = int(num)
    #             if num != bottom_r:
    #                 bottom_r += 1
                    
    #             #calculates tile matrix pos for column crossing on path
    #             for x in range(first_c * tile_scale, int(self.hitbox.right + self.xvel)+1, tile_scale):
    #                 ratio = (x - self.hitbox.right) / self.xvel
    #                 c = int(x / tile_scale)
    #                 # print(c)
    #                 for r in range(top_r, bottom_r):
    #                     self.path.append((r, c, ratio, 1, ratio))
                    
    #         self.path.sort(key=lambda data: data[4])
        
    #     elif self.xvel < 0:
    #         #last column crossing on path
    #         last_c = int((self.hitbox.left + self.xvel) / tile_scale + 1)
                
    #         #moving left and up (-x, -y)
    #         if self.yvel < 0:
    #             #last row crossing on path
    #             last_r = int((self.hitbox.top + self.yvel) / tile_scale + 1)
                
    #             #calculates tile matrix pos for column crossing on path
    #             for x in range(last_c * tile_scale, int(self.hitbox.left)+1, tile_scale):
    #                 ratio = (x - self.hitbox.left) / self.xvel
    #                 top_r = int((self.hitbox.top + (ratio * self.yvel)) / tile_scale)
    #                 num = (self.hitbox.bottom + (ratio * self.yvel)) / tile_scale
    #                 bottom_r = int(num)
    #                 if num != bottom_r:
    #                     bottom_r += 1
    #                 c = int((x / tile_scale) - 1)
    #                 for r in range(top_r, bottom_r):
    #                     self.path.append((r, c, ratio, 1, ratio))
                    
    #             #calculates tile matrix pos for row crossing on path
    #             for y in range(last_r * tile_scale, int(self.hitbox.top)+1, tile_scale):
    #                 ratio = (y - self.hitbox.top) / self.yvel
    #                 r = int((y / tile_scale) - 1)
    #                 left_c = int((self.hitbox.left + (ratio * self.xvel)) / tile_scale)
    #                 num = (self.hitbox.right + (ratio * self.xvel)) / tile_scale
    #                 right_c = int(num)
    #                 if num != right_c:
    #                     right_c += 1
    #                 for c in range(left_c, right_c):
    #                     self.path.append((r, c, 1, ratio, ratio))
        
    #         #moving left and down (-x, +y)
    #         elif self.yvel > 0:
    #             #first row crossing on path
    #             current_r = int(self.hitbox.bottom / tile_scale)
    #             if self.hitbox.bottom / tile_scale == current_r:#if already on a grid line include current x in path
    #                 first_r = current_r
    #             else:
    #                 first_r = current_r + 1
                    
    #             #calculates tile matrix pos for column crossing on path
    #             for x in range(last_c * tile_scale, int(self.hitbox.left)+1, tile_scale):
    #                 ratio = (x - self.hitbox.left) / self.xvel
    #                 top_r = int(((ratio * self.yvel) + self.hitbox.top) / tile_scale)
    #                 num = ((ratio * self.yvel) + self.hitbox.bottom) / tile_scale
    #                 bottom_r = int(num)
    #                 if num != bottom_r:
    #                     bottom_r += 1
    #                 c = int((x / tile_scale) - 1)
    #                 for r in range(top_r, bottom_r):
    #                     self.path.append((r, c, ratio, 1, ratio))
                    
    #             #calculates tile matrix pos for row crossing on path
    #             for y in range(first_r * tile_scale, int(self.hitbox.bottom + self.yvel)+1, tile_scale):
    #                 ratio = (y - self.hitbox.bottom) / self.yvel
    #                 r = int(y / tile_scale)
    #                 left_c = int((self.hitbox.left + (ratio * self.xvel)) / tile_scale)
    #                 num = (self.hitbox.right + (ratio * self.xvel)) / tile_scale
    #                 right_c = int(num)
    #                 if num != right_c:
    #                     right_c += 1
    #                 for c in range(left_c, right_c):
    #                     self.path.append((r, c, 1, ratio, ratio))
                    
    #         #moving left (-x, 0)
    #         else:
    #             #top row crossing path
    #             top_r = int(self.hitbox.top / tile_scale)
                
    #             #bottom row crossing path
    #             num = self.hitbox.bottom / tile_scale
    #             bottom_r = int(num)
    #             if num != bottom_r:
    #                 bottom_r += 1
                
    #             #calculates tile matrix pos for column crossing on path
    #             for x in range(last_c * tile_scale, int(self.hitbox.left)+1, tile_scale):
    #                 ratio = (x - self.hitbox.left) / self.xvel
    #                 # print(ratio)
    #                 c = int((x / tile_scale) - 1)
    #                 for r in range(top_r, bottom_r):
    #                     self.path.append((r, c, ratio, 1, ratio))
                
    #         self.path.sort(key=lambda data: data[4])
            
    #     else:
    #         #left column crossing path
    #         left_c = int(self.hitbox.left / tile_scale)
            
    #         #right column crossing path
    #         num = self.hitbox.right / tile_scale
    #         right_c = int(num)
    #         if num != right_c:
    #             right_c += 1
                
    #         if self.yvel < 0:#moving up (0, -y)
    #             #last row crossing on path
    #             last_r = int((self.hitbox.top + self.yvel) / tile_scale + 1)
                
    #             #calculates tile matrix pos for row crossing on path
    #             for y in range(last_r * tile_scale, int(self.hitbox.top)+1, tile_scale):
    #                 ratio = (y - self.hitbox.top) / self.yvel
    #                 # print(ratio)
    #                 r = int((y / tile_scale) - 1)
    #                 for c in range(left_c, right_c):
    #                     self.path.append((r, c, 1, ratio, ratio))
                    
    #         elif self.yvel > 0:#moving down (0, +y)
    #             #first row crossing on path
    #             current_r = int(self.hitbox.bottom / tile_scale)
    #             if self.hitbox.bottom / tile_scale == current_r:
    #                 first_r = current_r
    #             else:
    #                 first_r = current_r + 1
                
    #             #calculates tile matrix pos for row crossing on path
    #             for y in range(first_r * tile_scale, int(self.hitbox.bottom + self.yvel)+1, tile_scale):
    #                 ratio = (y - self.hitbox.bottom) / self.yvel
                    
    #                 r = int(y / tile_scale)
    #                 for c in range(left_c, right_c):
    #                     self.path.append((r, c, 1, ratio, ratio))
                    
    #         self.path.sort(key=lambda data: data[4])
    
    def calc_path_better(self, tiles):
        # tile_pos = self.pos//tile_scale
        # current_tile = tiles[int(tile_pos.y)][int(tile_pos.x)]
        
        current_right_column = self.hitbox.right//tile_scale
        current_left_column = self.hitbox.left//tile_scale
        current_top_row = self.hitbox.top//tile_scale
        current_bottom_row = self.hitbox.bottom//tile_scale
        
        if self.xvel > 0:
            # current_column = self.hitbox.right//tile_scale
            for n in range(1, int(self.xvel//tile_scale)+2):
                # print(n)
                next_x = self.hitbox.right + self.xvel * n
                next_column = int(next_x/tile_scale)
                next_top_row = int((self.hitbox.top + self.yvel)/tile_scale)
                next_bottom_row = int((self.hitbox.bottom + self.yvel)/tile_scale)
                print(current_top_row, next_top_row)
                # print(current_right_column, next_column)
                if next_column != current_right_column:
                    next_top_tile = tiles[next_top_row][next_column]#having only two(top and bottom) works for player being smaller than a tile but not bigger, would need a loop
                    next_bottom_tile = tiles[next_bottom_row][next_column]
                    if next_top_tile.t_type in self.collidable_tiles or next_bottom_tile.t_type in self.collidable_tiles:
                        ratio = (next_top_tile.rect.left - self.hitbox.right)/(self.hitbox.right + self.xvel)
                        print(ratio)
                        self.xvel *= ratio
                        
        elif self.xvel < 0:
            for n in range(int(self.xvel//tile_scale)+1):
                next_x = self.hitbox.left + self.xvel * n
                next_column = next_x//tile_scale
                if next_column != current_left_column:
                    next_top_tile = tiles[current_top_row][next_column]
                    next_bottom_tile = tiles[current_bottom_row][next_column]
                    if next_top_tile.t_type in self.collidable_tiles or next_bottom_tile.t_type in self.collidable_tiles:
                        self.xvel *= (self.hitbox.left - next_top_tile.right)/(self.hitbox.left + self.xvel)
                        
        if self.yvel > 0:
            for n in range(int(self.yvel//tile_scale)+1):
                next_y = self.hitbox.bottom + self.yvel * n
                next_row = next_y//tile_scale
                if next_row != current_bottom_row:
                    next_left_tile = tiles[current_left_column][next_row]
                    next_right_tile = tiles[current_right_column][next_row]
                    if next_left_tile.t_type in self.collidable_tiles or next_right_tile.t_type in self.collidable_tiles:
                        self.yvel *= (next_left_tile.top - self.hitbox.bottom)/(self.hitbox.bottom + self.yvel)
                        
        elif self.yvel < 0:
            for n in range(int(self.yvel//tile_scale)+1):
                next_y = self.hitbox.top + self.yvel * n
                next_row = next_y//tile_scale
                if next_row != current_top_row:
                    next_left_tile = tiles[current_left_column][next_row]
                    next_right_tile = tiles[current_right_column][next_row]
                    if next_left_tile.t_type in self.collidable_tiles or next_right_tile.t_type in self.collidable_tiles:
                        self.yvel *= (self.hitbox.top - next_left_tile.bottom)/(self.hitbox.top + self.yvel)
                        
    def calc_path_better(self, tiles):
        current_right_column = int((self.hitbox.right-1)/tile_scale)
        current_left_column = int(self.hitbox.left/tile_scale)
        current_top_row = int(self.hitbox.top/tile_scale)
        current_bottom_row = int((self.hitbox.bottom-1)/tile_scale)
        # print(current_left_column, current_right_column)
        # ns = []
        possible_col = []
        possible_row = []
        # self.xvel = 50
        # for x in range(1, int((self.pos.x + self.xvel + (self.hitbox.width/2))/tile_scale)+2):
            # next_x = self.pos.x + self.xvel + (self.hitbox.width/2)
            # possible_x.append(next_x)
            
        if self.xvel > 0:
            for n in range(current_left_column, int((self.hitbox.left + self.xvel)/tile_scale)+1):
                possible_col.append(n)
                
            for n in range(current_right_column, int((self.hitbox.right + self.xvel)/tile_scale)+1):
                possible_col.append(n)
        
        elif self.xvel < 0:
            for n in range(int((self.hitbox.left + self.xvel)/tile_scale), current_left_column+1):
                possible_col.append(n)
                
            for n in range(int((self.hitbox.right + self.xvel)/tile_scale), current_right_column+1):
                possible_col.append(n)
                
            # possible_col.reverse()
            
        else:
            possible_col.append(current_left_column)
            possible_col.append(current_right_column)
                
        if self.yvel > 0:
            for n in range(current_top_row, int((self.hitbox.top + self.yvel)/tile_scale)+1):
                possible_row.append(n)
                
            for n in range(current_bottom_row, int((self.hitbox.bottom + self.yvel)/tile_scale)+1):
                possible_row.append(n)
                
        elif self.yvel < 0:
            for n in range(int((self.hitbox.top + self.yvel)/tile_scale), current_top_row+1):
                possible_row.append(n)
                
            for n in range(int((self.hitbox.bottom + self.yvel)/tile_scale), current_bottom_row+1):
                possible_row.append(n)
                
            # possible_row.reverse()
            
        else:
            possible_row.append(current_top_row)
            possible_row.append(current_bottom_row)
        
        possible_tiles = []
        for c in possible_col:
            for r in possible_row:
                possible_tiles.append(tiles[r][c])
                
        # tiless = []
        # for n in range(len(possible_tiles)):
        #     tiless.append(possible_tiles[n].t_type + str(possible_tiles[n].pos))
        # print(tiless)

        # tested_tiles = []
        # for tile in sorted(possible_tiles, key = lambda tile: tile.pos.distance_to(self.pos)):
        #     # tested_tiles.append(tile.t_type)
        #     if tile.t_type in self.collidable_tiles:
        #         if self.xvel > 0:
        #             self.xvel *= (tile.rect.left - self.hitbox.right)/self.xvel
                    
        #         elif self.xvel < 0:
        #             self.xvel *= (tile.rect.right - self.hitbox.left)/self.xvel
                    
        #         if self.yvel > 0:
        #             self.yvel *= (tile.rect.top - self.hitbox.bottom)/self.yvel
                    
        #         elif self.yvel < 0:
        #             self.yvel *= (tile.rect.bottom - self.hitbox.top)/self.yvel
                    
        #         break
            
        possible_tiles.sort(key = lambda tile: tile.pos.distance_to(self.pos))
        for tile in possible_tiles:
            if tile.t_type in self.collidable_tiles:
                if tile.rect.left >= self.hitbox.right and self.xvel > 0:
                    ratio = (tile.rect.left - self.hitbox.right)/self.xvel
                    self.xvel *= ratio
                
                elif tile.rect.right <= self.hitbox.left and self.xvel < 0:
                    ratio = (tile.rect.right - self.hitbox.left)/self.xvel
                    self.xvel *= ratio
                    
                # elif tile.rect.top >= self.hitbox.bottom and self.yvel > 0:
                #     ratio = (tile.rect.top - self.hitbox.bottom)/self.yvel
                #     self.yvel *= ratio
                    
                # elif tile.rect.bottom <= self.hitbox.top and self.yvel < 0:
                #     ratio = (tile.rect.bottom - self.hitbox.top)/self.yvel
                #     self.yvel *= ratio
                    
                break
            
        for tile in possible_tiles:
            if tile.t_type in self.collidable_tiles:
                if tile.rect.top >= self.hitbox.bottom and self.yvel > 0:
                    ratio = (tile.rect.top - self.hitbox.bottom)/self.yvel
                    self.yvel *= ratio
                    
                elif tile.rect.bottom <= self.hitbox.top and self.yvel < 0:
                    ratio = (tile.rect.bottom - self.hitbox.top)/self.yvel
                    self.yvel *= ratio
                    
                break
                        
            
        # print(tested_tiles)
            
    def calc_path(self, tiles):#new
        # self.calc_path_better(tiles)
        # print(self.xvel//tile_scale)
        # self.path.clear()
        # print(str(self.hitbox.left) + " " + str(self.hitbox.bottom))
        #moving right
        if self.xvel > 0:
            #first column crossing on path
            current_c = int(self.hitbox.right / tile_scale)#could also just do from left // tile_scale + 1 or do (self.hitbox.right - 1) // tile_scale + 1
            if self.hitbox.right / tile_scale == current_c:#if right of hitbox is on a column (only needed if I set the position to be touching the tile)
                first_c = current_c
            else:
                first_c = current_c + 1
                
            #calculates tile matrix pos for column crossing on path (possible tile collisions)
            for x in range(first_c * tile_scale, int(self.hitbox.right + self.xvel)+1, tile_scale):
                # print()
                ratio = (x - self.hitbox.right) / self.xvel
                top_r = int(((ratio * self.yvel) + self.hitbox.top) / tile_scale)
                bottom_num = ((ratio * self.yvel) + self.hitbox.bottom) / tile_scale
                bottom_r = int(bottom_num)
                if bottom_num != bottom_r:
                    bottom_r += 1
                c = int(x / tile_scale)
                for r in range(top_r, bottom_r):
                    # self.path.append((r, c, ratio, 1, ratio))
                    # self.x_tile_collisions(r, c, ratio, tiles)
                    if tiles[r][c].t_type in self.collidable_tiles:
                        self.xvel *= ratio
                        # self.hitbox.left = x
                        # self.pos.x = x - (9 * sprite_scale)
                        # self.xvel = 0
                        break
        
        #moving left 
        elif self.xvel < 0:
            #last column crossing on path
            last_c = int((self.hitbox.left + self.xvel) / tile_scale + 1)
            
            #calculates tile matrix pos for column crossing on path
            for x in range(last_c * tile_scale, int(self.hitbox.left)+1, tile_scale):
                ratio = (x - self.hitbox.left) / self.xvel
                # print("x (" + str(x) + " " + str(self.hitbox.bottom + (self.yvel * ratio)) + ")")
                # print(ratio)
                # print()
                top_num = ((ratio * self.yvel) + self.hitbox.top) / tile_scale
                top_r = int(top_num)
                # if top_num == top_r:
                #     top_r 
                bottom_num = ((ratio * self.yvel) + self.hitbox.bottom) / tile_scale
                bottom_r = int(bottom_num)
                if bottom_num != bottom_r:
                    bottom_r += 1
                c = int((x / tile_scale) - 1)
                for r in range(top_r, bottom_r):
                    # self.path.append((r, c, ratio, 1, ratio))
                    # self.x_tile_collisions(r, c, ratio, tiles)
                    if tiles[r][c].t_type in self.collidable_tiles:
                        self.xvel *= ratio
                        # self.pos.x = x + (9 * sprite_scale)
                        # self.xvel = 0
                        break
            
        #no horizontal movement
        # else:
        #     #left column crossing path
        #     left_c = int(self.hitbox.left / tile_scale)
            
        #     #right column crossing path
        #     num = self.hitbox.right / tile_scale
        #     right_c = int(num)
        #     if num != right_c:
        #         right_c += 1
                
        #     if self.yvel < 0:#moving up
        #         #last row crossing on path
        #         last_r = int((self.hitbox.top + self.yvel) / tile_scale + 1)
                
        #         #calculates tile matrix pos for row crossing on path
        #         for y in range(last_r * tile_scale, int(self.hitbox.top)+1, tile_scale):
        #             ratio = (y - self.hitbox.top) / self.yvel
        #             # print(ratio)
        #             r = int((y / tile_scale) - 1)
        #             for c in range(left_c, right_c):
        #                 self.path.append((r, c, 1, ratio, ratio))
                    
        #     elif self.yvel > 0:#moving down (0, +y)
        #         #first row crossing on path
        #         current_r = int(self.hitbox.bottom / tile_scale)
        #         if self.hitbox.bottom / tile_scale == current_r:
        #             first_r = current_r
        #         else:
        #             first_r = current_r + 1
                
        #         #calculates tile matrix pos for row crossing on path
        #         for y in range(first_r * tile_scale, int(self.hitbox.bottom + self.yvel)+1, tile_scale):
        #             ratio = (y - self.hitbox.bottom) / self.yvel
                    
        #             r = int(y / tile_scale)
        #             for c in range(left_c, right_c):
        #                 self.path.append((r, c, 1, ratio, ratio))
                        
        # self.path.sort(key=lambda data: data[4])
        
        
        #moving up
        if self.yvel < 0:
            #last row crossing on path
            last_r = int((self.hitbox.top + self.yvel) / tile_scale + 1)
            
            #calculates tile matrix pos for row crossing on path
            for y in range(last_r * tile_scale, int(self.hitbox.top)+1, tile_scale):
                ratio = (y - self.hitbox.top) / self.yvel
                r = int((y / tile_scale) - 1)
                left_c = int((self.hitbox.left + (ratio * self.xvel)) / tile_scale)
                right_num = (self.hitbox.right + (ratio * self.xvel)) / tile_scale
                right_c = int(right_num)
                if right_num != right_c:
                    right_c += 1
                for c in range(left_c, right_c):
                    # self.path.append((r, c, 1, ratio, ratio))
                    if tiles[r][c].t_type in self.collidable_tiles:
                        self.yvel *= ratio
                        # self.pos.y = y + (9 * sprite_scale)
                        # self.yvel = 0
                        break
        
        #moving down
        elif self.yvel > 0:
            #first row crossing on path
            current_r = int(self.hitbox.bottom / tile_scale)
            if self.hitbox.bottom / tile_scale == current_r:#if already on a grid line include current x in path
                first_r = current_r
            else:
                first_r = current_r + 1
                    
            # print(str(self.hitbox.bottom//tile_scale) + " " + str(self.hitbox.left//tile_scale) + tiles[int(self.hitbox.bottom//tile_scale)][int(self.hitbox.left//tile_scale)].t_type)
            #calculates tile matrix pos for row crossing on path
            for y in range(first_r * tile_scale, int(self.hitbox.bottom + self.yvel+1), tile_scale):
                ratio = (y - self.hitbox.bottom) / self.yvel
                # print("y (" + str(self.hitbox.left + (self.xvel * ratio)) + " " + str(y) + ")")
                # print(ratio)
                # print()
                r = int(y / tile_scale)
                left_c = int((self.hitbox.left + (ratio * self.xvel)) / tile_scale)
                right_num = (self.hitbox.right + (ratio * self.xvel)) / tile_scale
                right_c = int(right_num)
                if right_num != right_c:
                    right_c += 1
                for c in range(left_c, right_c):
                    # self.path.append((r, c, 1, ratio, ratio))
                    if tiles[r][c].t_type in self.collidable_tiles:
                        self.yvel *= ratio
                        # self.pos.y = y - (9 * sprite_scale)
                        # self.yvel = 0
                        break
            
        # #no vertical movement   
        # else:
        #     #top row crossing path
        #     top_r = int(self.hitbox.top / tile_scale)
            
        #     #bottom row crossing path
        #     num = self.hitbox.bottom / tile_scale
        #     bottom_r = int(num)
        #     if num != bottom_r:
        #         bottom_r += 1
                
        #     if self.xvel > 0:
        #         #first column crossing on path
        #         current_c = int(self.hitbox.right / tile_scale)#could also just do from left // tile_scale + 1 or do (self.hitbox.right - 1) // tile_scale + 1
        #         if self.hitbox.right / tile_scale == current_c:#if right of hitbox is on a column (only needed if I set the position to be touching the tile)
        #             first_c = current_c
        #         else:
        #             first_c = current_c + 1
                
        #         #calculates tile matrix pos for column crossing on path
        #         for x in range(first_c * tile_scale, int(self.hitbox.right + self.xvel)+1, tile_scale):
        #             ratio = (x - self.hitbox.right) / self.xvel
        #             c = int(x / tile_scale)
        #             # print(c)
        #             for r in range(top_r, bottom_r):
        #                 self.path.append((r, c, ratio, 1, ratio))
                
        #     elif self.xvel < 0:
        #         #last column crossing on path
        #         last_c = int((self.hitbox.left + self.xvel) / tile_scale + 1)
            
        #         #calculates tile matrix pos for column crossing on path
        #         for x in range(last_c * tile_scale, int(self.hitbox.left)+1, tile_scale):
        #             ratio = (x - self.hitbox.left) / self.xvel
        #             # print(ratio)
        #             c = int((x / tile_scale) - 1)
        #             for r in range(top_r, bottom_r):
        #                 self.path.append((r, c, ratio, 1, ratio))
                        
        # self.path.sort(key=lambda data: data[4])
        
    # def check_tile_collision(self):#probably not needed
    #     if self.xvel != 0:
    #         if self.xvel > 0 and self.hitbox.right + self.xvel > (self.hitbox.right // tile_scale + 1) * tile_scale:
    #             x_collision = 0
                
    #         elif self.xvel < 0 and self.hitbox.left + self.xvel < (self.hitbox.left // tile_scale) * tile_scale:
    #             x_collision = 1
                
    #         # if self.xvel > 0 and self.hitbox.collidepoint()
        
    #     if self.yvel != 0:
    #         if self.yvel > 0 and self.hitbox.bottom + self.yvel > (self.hitbox.bottom // tile_scale + 1) * tile_scale:
    #             y_collision = 0
                
    #         elif self.yvel < 0 and self.hitbox.top + self.yvel < (self.hitbox.top // tile_scale) * tile_scale:
    #             y_collision = 1
                
    #         else:
    #             y_collision = 0
            
    #     return x_collision, y_collision

    def rotatehead(self):
        self.rot_image = pygame.transform.rotate(self.scal_image, self.angle)
        self.rect = self.rot_image.get_rect(center = self.rect.center)

    def rotatearms(self):
        self.rot_arm = pygame.transform.rotate(self.scal_arm, self.angle)
        self.arm_rect = self.rot_arm.get_rect(center = self.arm_rect.center)

    def rotate(self):
        self.rotatehead()
        self.rotatearms()

    def rotate_to_mouse(self, m_pos):
        dx, dy = (d_width / 2) - m_pos[0], (d_height / 2) - m_pos[1]
        self.angle = math.degrees(math.atan2(dx, dy))
        self.rotate()

    def render_text(self):
        self.ep_textbox.draw_r(str(round(self.energyval, 1)) + ' ')
        self.ep_textbox.draw_c("/")
        self.ep_textbox.draw_l(' ' + str(self.energymax))
        
        self.hp_textbox.draw_r(str(round(self.health, 1)) + ' ')
        self.hp_textbox.draw_c("/")
        self.hp_textbox.draw_l(' ' + str(self.healthmax))

    def render_bars(self):
        #progress of each bar
        self.healthbar.width = d_width*0.6*(self.health/self.healthmax)
        self.energybar.width = d_width*0.6*(self.energyval/self.energymax)
        
        #energy bar
        pygame.draw.rect(self.display, dark_blue, self.energybarborder)#pygame.Rect(energybar_b_left, energybar_b_top, energybar_b_width, energybar_b_height))
        pygame.draw.rect(self.display, blue, self.energybar)#pygame.Rect(energybar_p_left, energybar_p_top, energybar_p_width, energybar_p_height))

        #hp bar
        pygame.draw.rect(self.display, dark_green, self.healthbarborder)#pygame.Rect(hpbar_b_left, hpbar_b_top, hpbar_b_width, hpbar_b_height))
        pygame.draw.rect(self.display, green, self.healthbar)#pygame.Rect(hpbar_p_left, hpbar_p_top, hpbar_p_width, hpbar_p_height))

    def render_hearts(self):
        for i in range(0, len(self.hrt_rects)):
            self.display.blit(hrt, self.hrt_rects[i])

    def render_weapon_show(self):
        rect = fist_show.get_rect(topleft = (round(d_width-140), round(d_height-140)))
        self.display.blit(w_show[self.weapon], rect)
    
    # def sprint(self, moves):#original
    #     self.wait += 1
    #     if self.wait >= 30:
    #         self.energyval += self.energyregen
    #         if self.energyval >= self.energymax:
    #             self.energyval = self.energymax
    #             self.wait = 0
    #     if moves[4] and self.energyval > 0 and (self.xvel != 0 or self.yvel != 0) and not self.regen_energy:
    #         self.wait = 0
    #         self.energyval -= 0.5
    #         self.xvel = self.sprintvelmult * self.xvel
    #         self.yvel = self.sprintvelmult * self.yvel
    #         if self.energyval <= 0:
    #             self.energyval = 0
    #     self.energyval = round(self.energyval, 1)
        
    def sprint(self, moves):#new
        if self.regen_energy:
            self.energyval += self.energyregen
            if self.energyval >= self.energymax:
                self.energyval = self.energymax
                # self.regen_energy = False
            if moves[4] and self.is_new_press and (self.xvel != 0 or self.yvel != 0):
                self.regen_energy = False
                self.is_new_press = False
            # elif self.xvel == 0 and self.yvel == 0:
            #     self.regen_energy = False
                # self.is_new_press = True
                
        elif moves[4] and (self.xvel != 0 or self.yvel != 0):
            self.energyval -= 0.5
            self.xvel *= self.sprintvelmult
            self.yvel *= self.sprintvelmult
            if self.energyval <= 0:
                self.energyval = 0
                self.regen_energy = True
                
        elif moves[4]:
            self.regen_energy = True
            self.is_new_press = True
                
        elif not moves[4]:
            self.regen_energy = True
            
        # elif self.xvel != 0 or self.yvel != 0:
        #     self.regen_energy = True
        #     self.is_new_press = True
                
        # self.energyval = round(self.energyval, 1)
        
    # def sprint(self, moves):#test might use?
    #     if moves[4]:
    #         if self.regen_energy:
    #             self.energyval += self.energyregen
    #             if self.energyval >= self.energymax:
    #                 self.energyval = self.energymax
    #                 self.regen_energy = False
                    
    #         elif (self.xvel != 0 or self.yvel != 0):
    #             self.energyval -= 0.5
    #             self.xvel = self.sprintvelmult * self.xvel
    #             self.yvel = self.sprintvelmult * self.yvel
    #             if self.energyval <= 0:
    #                 self.energyval = 0
    #                 self.regen_energy = True
                    
    #     else:
    #         if self.regen_energy:
    #             self.energyval += self.energyregen
    #             if self.energyval >= self.energymax:
    #                 self.energyval = self.energymax
    #                 self.regen_energy = False
                    
    #     self.energyval = round(self.energyval, 1)
    
    def change_weapon(self):
        if self.weapon ==  0:
            self.weapon = 1
        elif self.weapon == 1:
            self.weapon = 0
        else:
            pass

    def attack(self, m_pos, b_group, e_group, s_group):#, camera):#needs improving, click and hold rotates player back and forth
        if self.weapon == 0:
            if self.attack_timer >= 15:
                self.angle += 20
                for e in e_group.sprites():
                    if self.weapon_hitbox.colliderect(e.hitbox.topleft[0]-5, e.hitbox.topright[1]-5, (e.hitbox.topright[0]-e.hitbox.topleft[0]+10), (e.hitbox.bottomleft[1]-e.hitbox.topleft[1]+10)):
                        if e.solid == True:
                            e.health -= self.damage
                for s in s_group.sprites():
                    if self.weapon_hitbox.colliderect(s.hitbox.topleft[0]-5, s.hitbox.topright[1]-5, (s.hitbox.topright[0]-s.hitbox.topleft[0]+10), (s.hitbox.bottomleft[1]-s.hitbox.topleft[1]+10)):
                        s.health -= self.damage
            
                self.rotate()
                self.attack_timer = 0
            #self.attack = True
        #bullet spawn has longer delay and max shoot before reload(just max bullets now)
        if self.weapon == 1:
            if self.bullets > 0:
                if self.bullet_delay >= 7:
                    self.bullets -= 1
                    self.create_bullet(b_group)#, camera)
                    self.bullet_delay = 0

    def create_s_footprint(self, f_group):#, camera):
        footprint = Snow_Footprint(self.pos.x, self.pos.y, self.angle)
        f_group.add(footprint)
        # camera.add(footprint)

    def create_m_footprint(self, f_group):#, camera):
        footprint = Mud_Footprint(self.pos.x, self.pos.y, self.angle)
        f_group.add(footprint)
        # camera.add(footprint)

    def create_bullet(self, b_group):#, camera):
        bullet = Bullet(self.pos.x, self.pos.y, angle = self.angle)
        b_group.add(bullet)
        # camera.add(bullet)

    def render(self, arm_offset_pos, img_offset_pos):
        self.display.blit(self.rot_arm, arm_offset_pos)#order matters as arms look weird if drawn over head
        self.display.blit(self.rot_image, img_offset_pos)
        self.render_bars()
        self.render_text()
        self.render_hearts()
        self.render_weapon_show()
        
    def sync(self):
        super().sync()

class Bullet(Object):
    def __init__(self, x, y, angle = 0, b_type = "player", display = display, image = blt):
        super().__init__(x, y, display, image)
        self.scal_image = pygame.transform.scale(self.image, (sprite_scale*4, sprite_scale*4))
        self.rot_image = self.scal_image
        self.rect = self.rot_image.get_rect(center = (round(self.pos.x), round(self.pos.y)))
        self.hitbox = self.scal_image.get_rect(center = (round(self.pos.x), round(self.pos.y)))
        self.angle = math.radians(angle) + math.pi
        self.vel = 10
        self.xvel = (self.vel * math.sin(self.angle)) + random.randint(0, 1) - 0.5
        self.yvel = (self.vel * math.cos(self.angle)) + random.randint(0, 1) - 0.5
        self.damage = 2
        self.t = 0
        self.z = 1
        self.type = "bullet"
        self.b_type = b_type

    def update(self, tiles, player, enemies, spawners, i_group):
        self.move(tiles, player, enemies, spawners, i_group)
        self.stop()
        #self.render()

    def move(self, tiles, player, enemies, spawners, i_group):

        self.tile_collisions(tiles)

        self.entity_collisions(player, enemies, spawners)

        self.door_collisions(i_group)
        
        self.sync()

    def stop(self):
        self.t += 1
        if self.t >= 60:
            self.kill()

    def tile_collisions(self, tiles):
        for t in tiles:
            #collision of impassible tiles
            if t.t_type == "wall" or t.t_type == "tree" or t.t_type == "door":
                if t.rect.colliderect(self.hitbox.topleft[0] + (self.xvel * sprite_scale), self.hitbox.topleft[1] + (self.yvel * sprite_scale), self.hitbox.topright[0]-self.hitbox.topleft[0], self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                    self.kill()

    def door_collisions(self, i_group):
        for d in i_group:
            #collision of impassible tiles
            if d.type == "door":
                if d.rect.colliderect(self.hitbox.topleft[0] + (self.xvel * sprite_scale), self.hitbox.topleft[1] + (self.yvel * sprite_scale), self.hitbox.topright[0]-self.hitbox.topleft[0], self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                    self.kill()

    def enemy_collisions(self, enemies, spawners):
        for e in enemies:
            #collision of enemy hitbox
            if e.solid and e.hitbox.colliderect(self.hitbox.topleft[0] + (self.xvel * sprite_scale), self.hitbox.topleft[1] + (self.yvel * sprite_scale), self.hitbox.topright[0]-self.hitbox.topleft[0], self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                self.deal_damage(e)
                self.kill()
        for s in spawners:
            #collision of spawner hitbox
            if s.solid and s.hitbox.colliderect(self.hitbox.topleft[0] + (self.xvel * sprite_scale), self.hitbox.topleft[1] + (self.yvel * sprite_scale), self.hitbox.topright[0]-self.hitbox.topleft[0], self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
                self.deal_damage(s)
                self.kill()

    def player_collision(self, player):
        if player.hitbox.colliderect(self.hitbox.topleft[0] + (self.xvel * sprite_scale), self.hitbox.topleft[1] + (self.yvel * sprite_scale), self.hitbox.topright[0]-self.hitbox.topleft[0], self.hitbox.bottomleft[1]-self.hitbox.topleft[1]):
            self.deal_damage(player)
            self.kill()

    def entity_collisions(self, player, enemies, spawners):
        if self.b_type == "player":
            self.enemy_collisions(enemies, spawners)
        else:
            self.player_collision(player)

    def deal_damage(self, entity):
        entity.health -= self.damage

    def sync(self):
        super().sync()

    def rotate(self):
        self.rot_image = pygame.transform.rotate(self.scal_image, self.angle)
        self.rect = self.rot_image.get_rect(center = self.rect.center)

    def render(self):
        self.display.blit(self.rot_image, self.rect)

class Footprint(Object):
    def __init__(self, x, y, angle, display, image):
        super().__init__(x, y, display, image)
        self.type = "particle"
        self.scal_image = pygame.transform.scale(self.image, (sprite_scale*18, sprite_scale*18))
        self.rot_image = pygame.transform.rotate(self.scal_image, angle)
        self.rect = self.rot_image.get_rect(center = (round(self.pos.x), round(self.pos.y)))
        self.t = 0
        self.xvel = 0
        self.yvel = 0
        self.angle = angle
        self.z = 1

    def update(self):
        # self.rotate()
        self.fade()
        #self.render()

    def fade(self):
        self.t += 1
        if self.t >= 600:
            self.t = 0
            self.kill()

    # def rotate(self):
    #     self.rot_image = pygame.transform.rotate(self.scal_image, self.angle)
    #     self.rect = self.rot_image.get_rect(center = self.rect.center)

    def render(self):
        self.display.blit(self.rot_image, self.rect)
        
class Snow_Footprint(Footprint):
    def __init__(self, x, y, angle, display = display, image = snow_footprints):
        super().__init__(x, y, angle, display, image)
        
    def update(self):
        super().update()
        
class Mud_Footprint(Footprint):
    def __init__(self, x, y, angle, display = display, image = mud_footprints):
        super().__init__(x, y, angle, display, image)
        
    def update(self):
        super().update()

class Collectable(Object):
    def __init__(self, x, y, display, image, value):
        super().__init__(x, y, display, image)
        self.type = "collectable"
        self.value = value
        self.fade_timer = 0
        self.pushed = False

    def fade(self):
        self.fade_timer += 1
        if self.fade_timer >= self.fade_limit:
            self.kill()
            
    # def tile_collisions(self, p, tiles):#move away from tile center continuously
    #     for t in tiles:
    #         if t.t_type in p.collidable_tiles:
    #             if t.rect.colliderect(self.hitbox):
    #                 if self.pos.x >= t.rect.center.x:
    #                     self.pos.x += 1
    #                 else:
    #                     self.pos.x -= 1
                        
    #                 if self.pos.y >= t.rect.center.x:
    #                     self.pos.y += 1
    #                 else:
    #                     self.pos.y -= 1
    
    def tile_collisions(self, p, tiles, i_group):#move towards player continuously - could try to do it by finding a good location once and moving there
        if not self.pushed:
            self.pushed = True
            for t in tiles:
                if t.t_type in p.collidable_tiles:
                    if t.rect.colliderect(self.hitbox):
                        self.pushed = False
                        
                        if self.pos.x < p.pos.x:
                            self.pos.x += 1
                        else:
                            self.pos.x -= 1
                        
                        if self.pos.y < p.pos.y:
                            self.pos.y += 1
                        else:
                            self.pos.y -= 1
                            
            for d in i_group:
                if d.type == "door":
                    if d.rect.colliderect(self.hitbox):
                        self.pushed = False
                        
                        if self.pos.x < p.pos.x:
                            self.pos.x += 1
                        else:
                            self.pos.x -= 1
                        
                        if self.pos.y < p.pos.y:
                            self.pos.y += 1
                        else:
                            self.pos.y -= 1
                            
                            
            self.rect.center = self.pos
            self.hitbox.center = self.pos
            
    # def door_collisions(self, p, i_group):
        

    #pushes them out of walls and portals
    #def push(self, tiles):
    #    pass

class Ammo(Collectable):
    def __init__(self, x, y, display = display, image = amo, value = 30):
        super().__init__(x, y, display, image, value)
        self.fade_limit = random.randint(1250, 1500)
        self.scal_image = pygame.transform.scale(self.image, (sprite_scale*32, sprite_scale*32))
        self.rot_image = self.scal_image

    def update(self, p, tiles, i_group):
        super().tile_collisions(p, tiles, i_group)
        self.collect(p)
        self.fade()

    def collect(self, p):
        if p.hitbox.colliderect(self.hitbox):
            p.bullets += self.value
            self.kill()

    def fade(self):
        super().fade()

class Coin(Collectable):
    def __init__(self, x, y, display = display, image = cn, value = 1):
        super().__init__(x, y, display, image, value)
        self.fade_limit = random.randint(850, 950)

    def update(self, p, tiles, i_group):
        super().tile_collisions(p, tiles, i_group)
        self.collect(p)
        self.fade()

    def collect(self, p):
        if p.hitbox.colliderect(self.hitbox):
            p.cash += self.value
            self.kill()

    def fade(self):
        super().fade()

class Menu_Player(Entity):
    def __init__(self, x, y, display = display, image = plrhd, arm = plrrm):
        super().__init__(x, y, display, image, arm)
        self.energyval = 50
        self.energyregen = 0.2
        self.energymax = 50
        self.sprintvelmult = 2
        self.wait = 0
        self.vel = 4
        self.name = "bob"

    def update(self, moves, m_pos, m_p_rect, play_group, quit_group, ctrl_group):
        self.rotate(m_pos)
        self.move(moves, play_group, quit_group, ctrl_group)
        # self.render()
        self.die(m_p_rect)

    def move(self, moves, play_group, quit_group, ctrl_group):
        # if moves[0] and not moves[1]:
        #     self.yvel = -self.vel
        # elif moves[1] and not moves[0]:
        #     self.yvel = self.vel
        # elif moves[0] and moves[1]:
        #     self.yvel = 0
        # else:
        #     self.yvel = 0
            
        # if moves[2] and not moves[3]:
        #     self.xvel = -self.vel
        # elif moves[3] and not moves[2]:
        #     self.xvel = self.vel
        # elif moves[2] and moves[3]:
        #     self.xvel = 0
        # else:
        #     self.xvel = 0
        
        self.yvel = 0
        if moves[0]:
            self.yvel -= self.vel
        if moves[1]:
            self.yvel += self.vel
            
        self.xvel = 0
        if moves[2]:
            self.xvel -= self.vel
        if moves[3]:
            self.xvel += self.vel
            
        if abs(self.xvel) == abs(self.yvel) and self.xvel != 0:#this should be moved after all speed changes if speed is set to a specific value by something
            abs_vel = (self.vel/root_2)
            self.xvel = (self.xvel/self.vel) * abs_vel
            self.yvel = (self.yvel/self.vel) * abs_vel

        self.sprint(moves)

        self.border_collision()

        self.button_collision(play_group)
        self.button_collision(quit_group)
        self.button_collision(ctrl_group)

        self.sync()

    def die(self, m_p_rect):
        if self.hitbox.colliderect(m_p_rect):
            self.dirty = 0
            self.kill()
        else:
            self.dirty = 1

    def border_collision(self):
        if self.pos.x <= ((9 * sprite_scale) - self.xvel):
            self.xvel = 0
        elif self.pos.x >= ((d_width - (9 * sprite_scale)) - self.xvel):
            self.xvel = 0
        if self.pos.y <= ((9 * sprite_scale) - self.yvel):
            self.yvel = 0
        elif self.pos.y >= ((d_height - (9 * sprite_scale)) - self.yvel):
            self.yvel = 0

    def button_collision(self, group):
        if group[1] == group[2]:
            if self.hitbox.colliderect((group[0].topleft[0] - self.xvel), group[0].topleft[1], 1, (group[0].bottomleft[1] - group[0].topleft[1])):
                if self.xvel > 0:
                    self.xvel = 0
            elif self.hitbox.colliderect((group[0].topright[0] - 1), group[0].topright[1], (1 - self.xvel), (group[0].bottomright[1] - group[0].topright[1])):
                if self.xvel < 0:
                    self.xvel = 0
            if self.hitbox.colliderect(group[0].topleft[0], (group[0].topleft[1] - self.yvel), (group[0].topright[0] - group[0].topleft[0]), 1):
                if self.yvel > 0:
                    self.yvel = 0
            elif self.hitbox.colliderect(group[0].bottomleft[0], (group[0].bottomleft[1] - 1), (group[0].topright[0] - group[0].topleft[0]), (1 - self.yvel)):
                if self.yvel < 0:
                    self.yvel = 0
            elif self.hitbox.colliderect(group[0].bottomleft[0], group[0].bottomleft[1]-16+(9*sprite_scale), (group[0].bottomright[0]-group[0].bottomleft[0]), 2):
                self.pos.y = group[0].bottomleft[1] + (9*sprite_scale)
            # elif pygame.Rect(group[0].bottomleft[0], group[0].bottomleft[1]-16+(9*sprite_scale), (group[0].bottomright[0]-group[0].bottomleft[0]), 2).collidepoint(self.pos):
            #     self.pos.y = group[0].bottomleft[1] + (9*sprite_scale)

    def sprint(self, moves):
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
        self.energyval = round(self.energyval, 1)
        
    def rotatehead(self):
        self.rot_image = pygame.transform.rotate(self.scal_image, self.angle)
        self.rect = self.rot_image.get_rect(center = self.rect.center)

    def rotatearms(self):
        self.rot_arm = pygame.transform.rotate(self.scal_arm, self.angle)
        self.arm_rect = self.rot_arm.get_rect(center = self.arm_rect.center)

    def rotate(self, m_pos):
        dx, dy = self.pos.x - m_pos.x, self.pos.y - m_pos.y
        self.angle = math.degrees(math.atan2(dx, dy))
        self.rotatehead()
        self.rotatearms()

    def render_bar(self, play_rect, play_img):
        x = play_rect.topleft[0] + 8
        if play_img == play_u:
            y = play_rect.topleft[1] + 8
        elif play_img == play_d:
            y = play_rect.topleft[1] + 24
        w = (play_rect.topright[0] - play_rect.topleft[0] - 16) * (self.energyval/self.energymax)
        h = play_rect.bottomleft[1] - play_rect.topleft[1] - 32

        pygame.draw.rect(self.display, blue, pygame.Rect(x, y, w, h))
        
    def render(self):
        self.display.blit(self.rot_image, self.rect)
        self.display.blit(self.rot_arm, self.arm_rect)
        
    def sync(self):
        super().sync()

class Interactable(pygame.sprite.DirtySprite):
    def __init__(self, x, y, state, images, display = display):
        super().__init__()
        pygame.sprite.DirtySprite.__init__(self)
        self.pos = pygame.math.Vector2((x, y))
        self.display = display
        self.images = images
        self.image = images[state]
        # self.image1 = image1
        # self.image2 = image2
        # self.image = self.image1
        # rect1 = images[1].get_rect(bottomleft = (round(x), round(y)))
        # rect2 = images[2].get_rect(bottomleft = (round(x), round(y)))
        # self.rects = [rect1, rect2]
        self.rects = []
        for i in images:
            self.rects.append(i.get_rect(bottomleft = (round(x), round(y))))
        self.rect = self.rects[state]
        # self.rect = self.rect1
        self.state = state
        # self.image = locals()['self.image' + str(self.state)]
        # self.rect = locals()['self.rect' + str(self.state)]
        # exec('self.image = self.image' + str(self.state) + '\nself.rect = self.rect' + str(self.state))
        self.hitbox = pygame.Rect(x-10, y-58, 68, 68)
        self.once = False
        # self.type = "interactable"
        self.z = 2
        self.dirty = 1
        self.needs_key = False
        # self.info_textbox = textbox(d_width/2, d_height*0.88, 20, white, display)
        # self.info_text = Text(d_width/2, d_height*0.88, 20, white, display, 'Right click to interact', has_bg=True)
        
    def render_text(self, textbox):
        textbox.draw_c("Right click to interact")
        # self.info_text.draw_l()

    #def render(self):
    #    self.display.blit(self.image, self.rect)

class Chest(Interactable):
    def __init__(self, x, y, state, images = [wood_closed, wood_open], c_type = 1):
        super().__init__(x, y, state, images)
        self.once = True
        self.c_type = c_type
        self.type = "chest"
        # self.open = state
        # self.check_image = True

    def update(self, moves, player, c_group, textbox):#, camera):
        # if self.check_image:
        #     self.set_image()
        #     self.check_image = False
        self.change_state(moves, player, c_group, textbox)#, camera)
        #self.render()

    # def change_state(self, moves, player, c_group):
    #     if moves[7] and player.hitbox.colliderect(self.hitbox):
    #         if self.image == self.image1:
    #             self.image = self.image2
    #             self.rect = self.rect2
    #             self.action(c_group)
    #         elif self.image == self.image2 and self.once == False:
    #             self.image = self.image1
    #             self.rect = self.rect1
    #         else:
    #             pass
            
    # def change_state(self, moves, player, c_group):
    #     if player.hitbox.colliderect(self.hitbox):
    #         self.render_text()
    #         if moves[7]:
    #             if self.image == self.image1:
    #                 self.image = self.image2
    #                 self.rect = self.rect2
    #                 self.action(c_group)
    #             elif self.image == self.image2 and self.once == False:
    #                 self.image = self.image1
    #                 self.rect = self.rect1
    #             else:
    #                 pass
                
    # def change_state(self, moves, player, c_group, camera):
    #     if self.once == True:
    #         if player.hitbox.colliderect(self.hitbox):
    #             if self.image == self.image1:
    #                 self.render_text()
    #                 if moves[7]:
    #                     self.image = self.image2
    #                     self.rect = self.rect2
    #                     self.open = True
    #                     self.action(c_group, camera)
    #     else:
    #         if player.hitbox.colliderect(self.hitbox):
    #             self.render_text()
    #             if moves[7]:
    #                 if self.image == self.image1:
    #                     self.image = self.image2
    #                     self.rect = self.rect2
    #                     self.open = True
    #                     self.action(c_group, camera)
    #                 else:
    #                     self.image = self.image1
    #                     self.rect = self.rect1
    #                     self.open = False
                        
    # def change_state(self, moves, player, c_group, camera):
    #     if self.once:
    #         if not self.open:
    #             if player.hitbox.colliderect(self.hitbox):
    #                 self.render_text()
    #                 if moves[7]:
    #                     self.open = True
    #                     self.set_image()
    #                     self.action(c_group, camera)
    #     else:
    #         if player.hitbox.colliderect(self.hitbox):
    #                 self.render_text()
    #                 if moves[7]:
    #                     self.open != self.open
    #                     self.set_image()
    #                     self.action(c_group, camera)
                        
    def change_state(self, moves, player, c_group, textbox):#, camera):
        if self.once:
            if self.state == 0:
                if player.hitbox.colliderect(self.hitbox):
                    self.render_text(textbox)
                    if moves[7]:
                        self.state = 1
                        self.image = self.images[self.state]
                        self.rect = self.rects[self.state]
                        self.action(c_group)#, camera)
                        
        else:
            if player.hitbox.colliderect(self.hitbox):
                self.render_text(textbox)
                if moves[7]:
                    if self.state == 0:
                        self.state = 1
                    else:
                        self.state = 0
                    self.image = self.images[self.state]
                    self.rect = self.rects[self.state]
                    self.action(c_group)#, camera)
                
    # def set_image(self):
    #     if self.open:
    #         self.image = self.image2
    #         self.rect = self.rect2
    #     else:
    #         self.image = self.image1
    #         self.rect = self.rect1
                        
    # def player_collision(self, player):
    #     if player.hitbox.colliderect(self.hitbox):
    #         self.colliding = True
    #     else:
    #         self.colliding = False
                                    
    # def show_text(self):
    #     if self.colliding:
            

    def action(self, c_group):#, camera):
        for n in range (0, self.c_type*5):
            x = (self.hitbox.topleft[0] + random.randint(0, (self.hitbox.topright[0]-self.hitbox.topleft[0])))
            y = (self.hitbox.topleft[1] + random.randint(0, (self.hitbox.bottomleft[1]-self.hitbox.topleft[1])))
            num = random.randint(0, 30)
            if num == 30:
                self.create_ammo(x, y, c_group)#, camera)
            else:
                self.create_coin(x, y, c_group)#, camera)

    def create_coin(self, x, y, c_group):#, camera):
        coin = Coin(x, y)
        c_group.add(coin)
        # camera.add(coin)

    def create_ammo(self, x, y, c_group):#, camera):
        ammo = Ammo(x, y)
        c_group.add(ammo)
        # camera.add(ammo)
        
    def render_text(self, infobox):
        super().render_text(infobox)

    #def render(self):
    #    super().render()
    
class Iron_Chest(Chest):
    def __init__(self, x, y, state, images = [iron_closed, iron_open], c_type = 2):
        super().__init__(x, y, state, images = images, c_type = c_type)
        
    def update(self, moves, player, c_group, infobox):#, camera):
        super().update(moves, player, c_group, infobox)#, camera)
        
class Gold_Chest(Chest):
    def __init__(self, x, y, state, images = [gold_closed, gold_open], c_type = 3):
        super().__init__(x, y, state, images = images, c_type = c_type)
        
    def update(self, moves, player, c_group, infobox):#, camera):
        super().update(moves, player, c_group, infobox)#, camera)

class Door(pygame.sprite.DirtySprite):#Interactable):
    def __init__(self, x, y, state, d_type = 'tr', image = wood_door, display = display):
        # super().__init__(x, y, display, image1 = image1, image2 = image2)
        super().__init__()
        if d_type == 'tr':
            image1 = image
            image2 = pygame.transform.flip(pygame.transform.rotate(image, 90), True, False)
            # images = [image1, image2]
            rect1 = image1.get_rect(bottomleft = (round(x), round(y)))
            rect2 = image2.get_rect(bottomleft = (round(x), round(y)))
            # rects = [rect1, rect2]
        elif d_type == 'tl':
            image1 = pygame.transform.flip(image, True, False)
            image2 = pygame.transform.rotate(image, 90)
            # images = [image1, image2]
            rect1 = image1.get_rect(bottomright = (round(x), round(y)))
            rect2 = image2.get_rect(bottomright = (round(x), round(y)))
        elif d_type == 'br':
            image1 = pygame.transform.flip(image, False, True)
            image2 = pygame.transform.rotate(image, 270)
            # images = [image1, image2]
            rect1 = image1.get_rect(topleft = (round(x), round(y)))
            rect2 = image2.get_rect(topleft = (round(x), round(y)))
        elif d_type == 'bl':
            image1 = pygame.transform.flip(image, True, True)
            image2 = pygame.transform.flip(pygame.transform.rotate(image, 90), False, True)
            # images = [image1, image2]
            rect1 = image1.get_rect(topright = (round(x), round(y)))
            rect2 = image2.get_rect(topright = (round(x), round(y)))
        # self.rect = self.rect1
        # self.hitbox = pygame.Rect(self.rect.topleft[0]-10, self.rect.topleft[1]-10, self.rect.topright[0]-self.rect.topleft[0]+20, self.rect.bottomleft[1]-self.rect.topleft[1]+20)
        self.images = [image1, image2]
        self.image = self.images[state]
        self.rects = [rect1, rect2]
        self.rect = self.rects[state]
        self.d_type = d_type
        self.type = "door"
        self.pos = pygame.math.Vector2((x, y))
        self.display = display
        self.state = state#0 is vertical and 1 is horizontal
        self.hitbox = pygame.Rect(x-10, y-58, 68, 68)
        self.once = False
        self.z = 2
        self.dirty = 1
        self.needs_key = False
        # self.info_textbox = textbox(d_width/2, d_height*0.88, 20, white, display)
        # self.push_dist = self.rects[0].centerx - self.rects[0].left + 0.1
        # super().__init__(x, y, state, images)
 
    def update(self, moves, player, e_group, c_group, textbox):
        self.change_state(moves, player, e_group, c_group, textbox)
        self.hitbox = pygame.Rect(self.rect.topleft[0]-10, self.rect.topleft[1]-10, self.rect.topright[0]-self.rect.topleft[0]+20, self.rect.bottomleft[1]-self.rect.topleft[1]+20)

    # def change_state(self, moves, player):
    #     if moves[7] and player.hitbox.colliderect(self.hitbox):
    #         if self.image == self.image1:
    #             self.image = self.image2
    #             self.rect = self.rect2
    #         elif self.image == self.image2 and self.once == False:
    #             self.image = self.image1
    #             self.rect = self.rect1
    #         else:
    #             pass
            
    # def change_state(self, moves, player, c_group):
    #     if self.once == True:
    #         if player.hitbox.colliderect(self.hitbox):
    #             if self.image == self.image1:
    #                 self.render_text()
    #                 if moves[7]:
    #                     self.image = self.image2
    #                     self.rect = self.rect2
    #                     self.action(c_group)
    #     else:
    #         if player.hitbox.colliderect(self.hitbox):
    #             self.render_text()
    #             if moves[7]:
    #                 if self.image == self.image1:
    #                     self.image = self.image2
    #                     self.rect = self.rect2
    #                     self.action(c_group)
    #                 else:
    #                     self.image = self.image1
    #                     self.rect = self.rect1
                        
    def change_state(self, moves, player, e_group, c_group, textbox):
        if self.once:
            if self.state == 0:
                if player.hitbox.colliderect(self.hitbox):
                    self.render_text()
                    if moves[7]:
                        self.state = 1
                        self.push_y(player, e_group, c_group)
                        
        else:
            if player.hitbox.colliderect(self.hitbox):
                self.render_text(textbox)
                if moves[7]:
                    if self.state == 0:
                        self.state = 1
                        self.push_y(player, e_group, c_group)
                    else:
                        self.state = 0
                        self.push_x(player, e_group, c_group)
                    
    def push_x(self, player, e_group, c_group):#maybe change to what the rect is before for more dynamic pushing
        self.image = self.images[self.state]
        self.rect = self.rects[self.state]
        
        if self.rect.colliderect(player.hitbox):
            if player.pos.x >= self.rect.centerx:
                player.pos.x = self.rect.right + (player.pos.x - player.hitbox.left) + 0.1
            else:
                player.pos.x = self.rect.left - (player.pos.x - player.hitbox.left) - 0.1
                
        for e in e_group:
            if e.solid:
                if self.rect.colliderect(e.hitbox):
                    if e.pos.x >= self.rect.centerx:
                        e.pos.x = self.rect.right + (e.pos.x - e.hitbox.left) + 0.1
                    else:
                        e.pos.x = self.rect.left - (e.pos.x - e.hitbox.left) - 0.1
                        
        for c in c_group:
            if self.rect.colliderect(e.hitbox):
                if c.pos.x >= self.rect.centerx:
                    c.pos.x = self.rect.right + (c.pos.x - c.hitbox.left) + 0.1
                else:
                    c.pos.x = self.rect.left - (c.pos.x - c.hitbox.left) - 0.1
        
    def push_y(self, player, e_group, c_group):
        self.image = self.images[self.state]
        self.rect = self.rects[self.state]
        
        if self.rect.colliderect(player.hitbox):
            if player.pos.y >= self.rect.centery:
                player.pos.y = self.rect.bottom + (player.pos.y - player.hitbox.top) + 0.1
            else:
                player.pos.y = self.rect.top - (player.pos.y - player.hitbox.top) - 0.1
                
        for e in e_group:
            if e.solid:
                if self.rect.colliderect(e.hitbox):
                    if e.pos.y >= self.rect.centery:
                        e.pos.y = self.rect.bottom + (e.pos.y - e.hitbox.top) + 0.1
                    else:
                        e.pos.y = self.rect.top - (e.pos.y - e.hitbox.top) - 0.1
                        
        for c in c_group:
            if self.rect.colliderect(e.hitbox):
                if c.pos.y >= self.rect.centery:
                    c.pos.y = self.rect.bottom + (c.pos.y - c.hitbox.top) + 0.1
                else:
                    c.pos.y = self.rect.top - (c.pos.y - c.hitbox.top) - 0.1
                    
    def render_text(self, textbox):
        textbox.draw_c("Right click to interact")
    # def action(self, x):
    #     pass