import math, random
from typing import Type

import pygame.image

from textbox import *
from settings import *

# class Drop_Details():#for old method
#     def __init__(self, cls:Type[Collectable], probability:int, amount:int, value:int):
#         self.cls = cls
#         self.probability = probability#maybe should be rarity for now as its a chance of 1 in whatever the value is
#         self.amount = amount
#         self.value = value
        
class Drop_Details():#for new method
    def __init__(self, probability:int, amount:int, value:int, image:pygame.Surface):
        self.probability = probability
        self.amount = amount
        self.value = value
        self.image = image
        
# def drop_details(probability:int, amount:int, value:int, image:pygame.Surface):
#     return (probability, amount, value, image)

#objects (all sprites)
class Object(pygame.sprite.DirtySprite):
    def __init__(self, pos:pygame.Vector2, image:pygame.Surface):#I may not need image, arm, tail as args
        super().__init__()#remove this or
        pygame.sprite.DirtySprite.__init__(self)#or remove this
        
        self.pos = pos
        self.image = image
        
        self.type = "object"#might remove types for __name__
        
        #health is used as health or as a time for particle lifetime (might remove this second use)
        self.health = 10
        self.health_max = 10
        
        self.scal_image = pygame.transform.scale(self.image, (sprite_scale*18, sprite_scale*18))#change
        # self.rot_image = pygame.transform.rotate(self.scal_image, angle)#change
        self.rect = self.rot_image.get_rect(center = (round(self.pos.x), round(self.pos.y)))#maybe change by removing round
        
        self.hitbox = self.scal_image.get_rect(center = (round(self.pos.x), round(self.pos.y)))#maybe change by removing round
        
        self.current_tile_pos = (0, 0)
        self.current_tile = None
        
    def get_current_tile(self, level_matrix:list):
        self.current_tile_pos = (int(self.pos.x/tile_scale), int(self.pos.y/tile_scale))
        self.current_tile = level_matrix[self.current_tile_pos[1]][self.current_tile_pos[0]]

#entities (moving sprites)
class Entity(Object):
    def __init__(self, pos:pygame.Vector2, image:pygame.Surface, angle:float):
        super().__init__(pos, image)
        
        self.angle = angle
        
        self.type = "entity"
        
        self.rot_image = pygame.transform.rotate(self.scal_image, angle)#might just be scal_image
        
        self.base_speed = 0
        self.speed = 0
        self.dir = pygame.Vector2((0, 0))
        self.vel = pygame.Vector2((0, 0))
        self.acc = pygame.Vector2((0, 0))
        self.friction = 1
        
        self.idle_timer = 0
        self.idle_time = 150
        
        # self.tile_effects = {
        #     "mud":{
        #         "speed_mult":0.5,#"speed":-self.speed*0.5,
        #     },#[lambda: self.mult_speed(0.5)],
        #     "snow":{
        #         "speed_mult":0.66,#"speed":-self.speed*0.33,
        #     },#[lambda: self.mult_speed(0.66)],
        #     "ice":{
        #         "friction":0.5,#maybe just have this be a tile attribute
        #     },##[lambda: self.set_friction(0.5)],
        # }
        
        self.tile_effects = {
            "mud":{
                "speed":lambda: self.mult_speed(0.5),
            },
            "snow":{
                "speed":lambda: self.mult_speed(0.66),
            },
            "magma":{
                "speed":lambda: self.mult_speed(0.8),
                "health":lambda: self.change_health(2),
            },
        }
        
        self.collidable_tiles = ["wall", "tree"]
        
        self.hp_bar = pygame.Rect(0, 0, 30, 6)#pygame.Rect(self.hitbox.centerx - 15, self.hitbox.top - 15, 30, 6)
        self.hp_bar_back = pygame.Rect(0, 0, 34, 10)#pygame.Rect(self.hitbox.centerx - 17, self.hitbox.top - 17, 34, 10)
        
    def update(self):
        self.move()

    def move(self):
        # self.calc_vel()
        
        self.pos += self.vel
        
        self.move_rects()
        self.move_bars()
        
    def move_rects(self):
        self.rect.center = self.pos
        
        self.hitbox.center = self.pos
        
    def rotate(self):
        self.angle = self.dir.as_polar()[1]#maybe move if we have enemies moving in circles around the player
        
        self.rot_image = pygame.transform.rotate(self.scal_image, self.angle)
        self.rect = self.rot_image.get_rect(center = self.rect.center)
        
    def move_bars(self):
        self.hp_bar.centery = self.hp_bar_back.centery = self.hitbox.top - 15
        
    def calc_vel(self):
        self.acc = self.current_tile.friction * ((self.speed * self.dir) - self.vel)#move this if I ever decide to apply forces
        self.vel += self.acc
        
    # def apply_tile_effects(self):
    #     # self.tile_effects[self.current_tile.t_type]
    #     for attr, val in self.tile_effects.get(self.current_tile.t_type, {}).items():
    #         current = self.__getattribute__(attr)
    #         self.__setattr__(attr, current + val)
            
    def apply_tile_effects(self):#things that remove tile effects could add them to a different dict or just adjust every frame
        for attr, func in self.tile_effects.get(self.current_tile.t_type, {}).items():
            func()
            
    def tile_collisions(self):
        pass
    
    def reset_vals(self):
        # self.dir.x = self.dir.y = 0
        self.speed = self.base_speed
        # self.friction = 1
    
    def mult_speed(self, val:int|float):
        self.speed *= val
        
    def change_speed(self, val:int|float):
        self.speed += val
        
    def change_vel(self, val:int|float):
        self.vel += val
        
    def change_health(self, val:int|float):
        self.health += val
        
    def go_idle(self):# and put calc_dir after all the speed calcs
        if self.idle_timer == 0:
            self.dir = pygame.Vector2(random.randint(0, 200) - 100, random.randint(0, 200) - 100).normalize()
            self.idle_timer = self.idle_time
        else:
            self.idle_timer -= 1
            
    def go_to_player(self, p:Player):
        self.dir = (p.pos - self.pos).normalize()
        
class Particle(Object):
    def __init__(self, pos:pygame.Vector2, image:pygame.Surface):
        super().__init__(pos, image)
        
        self.type = "particle"
        
        self.speed = 0
        
        # self.die_funcs = (self.kill, self.fade)
        
    def update(self):
        self.fade()
    
    def fade(self):#might change to use system time
        self.health -= 1
        if self.health <= 0:
            self.kill()
            
    # def die(self):

    #     self.die_funcs[self.health]()
        
    # def fade(self):
    #     self.health -= 1

class Enemy(Entity):
    def __init__(self, pos:pygame.Vector2, image:pygame.Surface, angle:float):
        super().__init__(pos, image, angle)
        
        self.base_speed = 3
        self.speed = 0
        
        self.see_player_dist = 700
        
        self.damage = 10
        self.attack_dist = 25#might remove this and do it based on weapon
        
        # self.idle = False
        # self.idle_start_time = 0
        
        # self.drops = {#I think this is best but different method
        #     Money:[Drop_Details(1, (self.healthmax//2 - random.randint(0, self.healthmax//4)), 1)],
        #     Ammo:[Drop_Details(30, 1, 30)],
        # }
        # self.drops = {#this is bad for old method
        #     "money":[Drop_Details(Money, 1, (self.healthmax//2 - random.randint(0, self.healthmax//4)), 1)],
        #     "ammo":[Drop_Details(Ammo, 30, 1, 30)],
        # }
        # self.drops = [Drop_Details(Money, 1, (self.healthmax//2 - random.randint(0, self.healthmax//4)), 1), Drop_Details(Ammo, 30, 1, 30)]#this is for old methid
        
        # self.drops = {#for new method
        #     "money":[Drop_Details(1, (self.healthmax//2 - random.randint(0, self.healthmax//4)), 1, cn)],
        #     "ammo":[Drop_Details(30, 1, 30, amo)],
        # }
        
        self.pool_chances = {#pool method
            0.7:{
                "money":[Drop_Details(1, (self.healthmax//2 - random.randint(0, self.healthmax//4)), 1, cn)],
                "ammo":[Drop_Details(0.3, 1, 30, amo)],
            },
            0.2:{
                "ammo":[Drop_Details(1, 10, 50, amo)],
            },
            0.1:{
                None:[Drop_Details(0, 0, 0, None)],
            },
        }
        # self.pool_chances = [
        #     (1, {
        #         "money":[Drop_Details(1, 1, 1, cn)],
        #         "ammo":[Drop_Details(1, 1, 1, amo)],
        #         }
        #      )
        # ]
        
        self.pools = list(self.pool_chances.values())
        self.pool_weights = list(self.pool_chances.keys())
        
        # self.none_prob = 1#this was for if I didn't want to add and empty pool for enemies if they had a chance of dropping nothing (It ensures they are probabilities instead of weights)
        # for prob in self.pool_weights:
        #     self.none_prob -= prob
            
        # self.pools.append({0:[Drop_Details(0, 0, 0, None)]})
        # self.pool_weights.append(self.none_prob)
        
    def update(self):
        pass
        
    def die(self, p:Player, c_group:pygame.sprite.Group):
        if self.health <= 0:
            p.score += self.health_max
            p.kills += 1
            self.create_collectables(c_group)
            self.kill()
          
    # def create_collectables(self, c_group:pygame.sprite.Group):#for bad version of old method
    #     for _, data in self.drops.items():
    #         for details in data:
    #             num = random.randint(1, details.probability)
    #             if num == details.probability:
    #                 for _ in range(details.amount):
    #                     x = (self.hitbox.left + random.randint(0, (self.hitbox.width)))
    #                     y = (self.hitbox.top + random.randint(0, (self.hitbox.height)))
                        
    #                     collectable = details.cls(x, y, details.value)
    #                     c_group.add(collectable)
                        
    # def create_collectables(self, c_group:pygame.sprite.Group):#for good version of old method
    #     for details in self.drops:
    #         num = random.randint(1, details.probability)
    #         if num == details.probability:
    #             for _ in range(details.amount):
    #                 x = (self.hitbox.left + random.randint(0, (self.hitbox.width)))
    #                 y = (self.hitbox.top + random.randint(0, (self.hitbox.height)))
    
    #                 collectable = details.cls(x, y, details.value)
    #                 c_group.add(collectable)
                    
    # def create_collectables(self, c_group:pygame.sprite.Group):#for other method
    #     for cls, data in self.drops.items():
    #         for details in data:
                # num = random.randint(1, details.probability)
                # if num == details.probability:
    #                 for _ in range(details.amount):
                        # x = (self.hitbox.left + random.randint(0, (self.hitbox.width)))
                        # y = (self.hitbox.top + random.randint(0, (self.hitbox.height)))
                        
    #                     collectable = cls(x, y, details.value)
    #                     c_group.add(collectable)
    
    # def create_collectables(self, c_group:pygame.sprite.Group):#for new method
    #     for attr, drops in self.drops.items():
    #         for details in drops:
    #             num = random.randint(0, details.probability)
    #             if num == 0:
    #                 for _ in range(details.amount):
    #                     x = (self.hitbox.left + random.randint(0, (self.hitbox.width)))
    #                     y = (self.hitbox.top + random.randint(0, (self.hitbox.height)))
                        
    #                     collectable = Collectable(x, y, details.image, details.value, attr)
    #                     c_group.add(collectable)
                        
                        
    def create_collectables(self, c_group:pygame.sprite.Group):#pool method
        pool = random.choices(self.pools, self.pool_weights)[0]
        # collectables = random.choices(pool, weights, k=amount)
        num = random.random()
        for attr, drops in pool.items():
            for drop in drops:
                if num < drop.probability:
                    for _ in range(drop.amount):
                        x = (self.hitbox.left + random.randint(0, (self.hitbox.width)))
                        y = (self.hitbox.top + random.randint(0, (self.hitbox.height)))
                        
                        collectable = Collectable(x, y, drop.image, drop.value, attr)
                        c_group.add(collectable)
                    
                # collectable = random.choices(cls, prob, k=amount)
        
class Ghost(Enemy):
    def __init__(self, pos:pygame.Vector2, angle:float, image:pygame.Surface):
        super().__init__(pos, image, angle)
        
        self.base_speed = 2
        
        self.health = 15
        self.healthmax = 15
        
        self.see_player_dist = 800
        
        self.damage = 10
        self.attack_dist = 20
        # self.damage_tiles = {
        #     "portal":0.5,
        #     "level_portal":1,
        # }
        
        self.collidable_tiles = []
        
        # self.tile_effects = {
        #     "portal":{
        #         "health":-0.5,
        #     },
        #     "level_portal":{
        #         "health":-1,
        #     },
        # }
        
        self.tile_effects = {
            "portal":{
                "health":lambda: self.change_health(-0.5),
            },
            "level_portal":{
                "health":lambda: self.change_health(-1),
            },
        }
        
    def update(self, dist:int|float, p:Player, c_group:pygame.sprite.Group, level_matrix:list):
        self.die(p, c_group)#maybe move
        
        self.get_current_tile(level_matrix)
        
        self.calc_dir(dist, p)
        
        self.rotate()
        
        self.apply_tile_effects()
        
        self.calc_vel()
        
        self.tile_collisions()
        
        self.move()
            
    def calc_dir(self, dist:int|float, p:Player):
        if dist <= self.see_player_dist:
            self.go_to_player(p)
        else:
            self.go_idle()
            
    # def go_idle(self):
    #     if idle_timer == 0:
    #         self.target_pos = self.pos + (random.randint(0, 200) - 100, random.randint(0, 200) - 100)
        
    #         self.dir = (self.target_pos - self.pos).normalize()
            
    #         idle_timer = idle_time
            
    #     else:
    #         idle_timer -= 1
        
        # self.target_tile_pos = random.randint(0, 10) - 5 + self.current_tile_pos
        
    # def calc_vel(self):
    #     # if self.dir.magnitude() == 0:
    #     #     if self.vel.magnitude() == 0:
    #     #         self.acc = self.vel
    #     #         #self.vel -= self.vel
    #     #         #self.vel = self.dir
    #     #         #self.vel.x = self.vel.y = 0
    #     #         #pass
    #     #     else:
    #     #         if self.vel.magnitude() < self.friction * self.speed:
    #     #             self.acc = -self.vel
    #     #             #self.vel -= self.vel
    #     #             #self.vel = self.dir
    #     #             #self.vel.x = self.vel.y = 0
    #     #         else:
    #     #             self.acc = -self.friction * self.speed * self.vel.normalize()
    #     #             #self.vel -= self.friction * self.speed * self.vel.normalize()
    #     # else:
    #     #     if self.vel.magnitude() == self.speed:
    #     #         self.acc = 0
    #     #         #self.vel = 
    #     #     else:
    #     #         if self.speed - self.vel.magnitude() < self.friction * self.speed:
    #     #             self.acc = self.speed * self.dir - self.vel
    #     #         else:
    #     #             self.acc = self.friction * self.speed * self.dir
                    
    #     # self.acc = (self.friction * self.speed) * self.dir - self.friction * self.vel
    #     self.acc = self.friction * ((self.speed * self.dir) - self.vel)#move this if I ever decide to apply forces
    #     self.vel += self.acc
    #     # if self.acc.magnitude() == 0:
    #     #     self.vel -= self.acc
    
class Skeleton(Enemy):
    def __init__(self, pos:pygame.Vector2, image:pygame.Surface, angle:float):
        super().__init__(pos, image, angle)
        
        self.base_speed = 3
        self.base_reverse_speed = 2
        
        self.health = 10
        self.health_max = 10
        
        self.see_player_dist = 600
        self.damage = 5
        self.attack_dist = 300
        
    def update(self, dist:int|float, p:Player, c_group:pygame.sprite.Group, level_matrix:list):
        self.die(p, c_group)#maybe move
        
        self.get_current_tile(level_matrix)
        
        self.calc_dir(dist, p)#maybe put the speed calcs before dir
        
        self.rotate()
        
        self.apply_tile_effects()
        
        self.calc_vel()
        
        self.tile_collisions()
        
        self.move()
        
    def calc_dir(self, dist:int|float, p:Player):
        if dist < self.attack_dist:
            self.avoid_player(p)
        elif dist < self.see_player_dist:
            self.go_to_player(p)
        else:
            self.go_idle()
        
class Zombie(Enemy):
    def __init__(self, pos:pygame.Vector2, image:pygame.Surface, angle:float):
        super().__init__(pos, image, angle)
        
        self.base_speed = 3
        
        self.health = 10
        self.health_max = 10
        
        self.see_player_dist = 700
        self.damage = 5
        self.attack_dist = 25
        
    def update(self, dist:int|float, p:Player, c_group:pygame.sprite.Group, level_matrix:list):
        self.die(p, c_group)#maybe move
        
        self.get_current_tile(level_matrix)
        
        self.calc_dir(dist, p)#maybe put the speed calcs before dir
        
        self.rotate()
        
        self.apply_tile_effects()
        
        self.calc_vel()
        
        self.tile_collisions()
        
        self.move()
        
    def calc_dir(self, dist:int|float, p:Player):
        if dist <= self.see_player_dist:
            self.go_to_player(p)
        else:
            self.go_idle()
        
class Collectable(Particle):
    def __init__(self, pos:pygame.Vector2, image:pygame.Surface, value:int, attribute:str):
        super().__init__(pos, image)
        
        self.value = value
        self.attribute = attribute
        
        self.type = "collectable"
        
    def update(self, p:Player, level_matrix:list, i_group:pygame.sprite.Group):
        self.tile_collisions(p, level_matrix, i_group)
        self.collect(p)
        self.fade()
        
    def collect(self, p:Player):
        if p.hitbox.colliderect(self.hitbox):
            current = getattr(p, self.attribute)
            setattr(0, self.attribute, current + self.value)
            self.kill()
            
    def tile_collisions(self, p:Player, level_matrix:list, i_group:pygame.sprite.Group):#move towards player continuously - could try to do it by finding a good location once and moving there
        self.get_current_tile()#maybe move out into update func
        
        if level_matrix[self.current_tile[1]][self.current_tile[0]].t_type in p.collidable_tiles:
            self.pos += (p.pos - self.pos).normalize()
            
        for d in i_group:
            if d.type == "door":
                if d.rect.colliderect(self.hitbox):
                    self.pos += (p.pos - self.pos).normalize()
                    
        self.move_rects()
        
    def move_rects(self):
        self.rect.center = self.pos
        
        self.hitbox.center = self.pos
        
# class Collectable(Particle):
#     def __init__(self, x:int|float, y:int|float, image:pygame.Surface, value:int):
#         super().__init__(x, y, image)
        
#         self.value = value
        
#         self.type = "collectable"
        
#     def update(self, p:Player, level_matrix:list, i_group:pygame.sprite.Group):
#         self.tile_collisions(p, level_matrix, i_group)
#         self.collect(p)
#         self.fade()
    
#     def collect(self, p:Player):
#         if p.hitbox.colliderect(self.hitbox):
#             current = getattr(p, self.__class__.__name__)
#             # p.__setattr__(self.__class__.__name__, current + self.value)#might work
#             setattr(p, self.__class__.__name__, current + self.value)
#             self.kill()
            
#     def tile_collisions(self, p:Player, level_matrix:list, i_group:pygame.sprite.Group):#move towards player continuously - could try to do it by finding a good location once and moving there
#         self.get_current_tile()#maybe move out into update func
        
#         if level_matrix[self.current_tile[1]][self.current_tile[0]].t_type in p.collidable_tiles:
#             self.pos += (p.pos - self.pos).normalize()
            
#         for d in i_group:
#             if d.type == "door":
#                 if d.rect.colliderect(self.hitbox):
#                     self.pos += (p.pos - self.pos).normalize()
                    
#         self.rect.center = self.pos
        
#         self.hitbox.center = self.pos
        
# class Money(Collectable):
#     def __init__(self, x:int|float, y:int|float, image:pygame.Surface, value:int):
#         super().__init__(x, y, image, value)

class Factory(Object):
    pass

class Spawner(Object):
    def __init__(self, pos:pygame.Vector2, image:pygame.Surface, angle:float):
        super().__init__(pos, image)
        
        self.angle = angle
        
        self.spawn_time = 300
        self.e_count = 0
        self.e_count_max = 20
        
        self.spawn_chances = {
            Zombie:0.5,
            Skeleton:0.5,
        }
        
        self.enemy_classes = list(self.spawn_chances.keys())
        self.enemy_probs = list(self.spawn_chances.values())
    
    def create_enemy(self, e_group):
        self.spawn_time -= 1
        if self.spawn_time == 0 and self.e_count < self.e_count_max:
            enemy = random.choices(self.enemy_classes, self.enemy_probs)[0](self.pos.x, self.pos.y, self.angle)
            e_group.add(enemy)
            self.e_count += 1
            
class Player(Entity):
    def __init__(self, pos:pygame.Vector2, image:pygame.Surface, angle:float, lives:int=3):
        super().__init__(pos, image, angle)
        
        self.base_speed = 4
        
        self.health = 100
        self.health_max = 100
        self.health_regen = 0
        
        self.energy = 50
        self.energy_max = 50
        self.energy_regen = 0.2
        self.regen_energy = False
        
        self.sprint_mult = 2
        self.sprint_energy = 0.5
        
        self.portal_energy = 10
        
        self.score = 0
        self.kills = 0
        self.money = 0
        self.lives = lives
        self.deaths = 0
        
        self.damage = 5
        self.attack_dist = 25
        self.weapon = 0
        self.attack_timer = 0
        self.bullets = 50
        self.bullet_delay = 7
        
        self.weapon_hitbox = None
        
        self.wait = 0
        self.footprint_timer = 0
        
        self.is_new_press = True
        self.change_lvl = False
        
        self.respawn_protection = False
        self.respawn_protection_timer = 0
        
        self.prev_score = 0
        self.prev_kills = 0
        self.prev_bullets = self.bullets
        self.prev_cash = 0
        self.deaths = 0
        
        self.hrt_rects = []
        for i in range(self.lives):
            hrt_rect = hrt.get_rect(topleft = (round(d_width - 48 - (i*33)), 15))
            self.hrt_rects.append(hrt_rect)
            
        self.hp_bar_back = pygame.Rect(d_width*0.2 - 3, d_height*0.96 - 3, d_width*0.6 + 6, d_height*0.02 + 6)
        self.hp_bar = pygame.Rect(d_width*0.2, d_height*0.96, d_width*0.6, d_height*0.02)
        self.energy_bar_back = pygame.Rect(d_width*0.2 - 3, d_height*0.92 - 3, d_width*0.6 + 6, d_height*0.02 + 6)
        self.energy_bar = pygame.Rect(d_width*0.2, d_height*0.92, d_width*0.6, d_height*0.02)
        
        self.hp_textbox = textbox((d_width*0.5), (d_height * 0.96), int(d_height*0.02), white, display)
        self.ep_textbox = textbox((d_width*0.5), (d_height * 0.92), int(d_height*0.02), white, display)
        
    def update(self, level_matrix:list, moves:list):
        self.die()#maybe move
        
        self.get_current_tile(level_matrix)
        
        self.calc_dir(moves)#maybe put the speed calcs before dir
        
        self.rotate()
        
        self.apply_tile_effects()
        
        self.calc_vel()
        
        self.tile_collisions()
        
        self.move()
        
    def calc_dir(self, moves):
        self.dir.x = self.dir.y = 0#maybe remove for new input_detection
        self.speed = self.base_speed
        
        if moves[0]:
            self.dir.y -= 1
        if moves [1]:
            self.dir.y += 1
            
        if moves[2]:
            self.dir.x -= 1
        if moves[3]:
            self.dir.x += 1
            
        self.dir.normalize_ip()
        
    def angle_to_mouse(self, m_pos:pygame.Vector2):
        self.angle = (m_pos - (d_width/2, d_height/2)).as_polar()[1]
    
    def rotate(self, m_pos:pygame.Vector2):
        self.angle_to_mouse(m_pos)
        
        self.rot_image = pygame.transform.rotate(self.scal_image, self.angle)
        self.rect = self.rot_image.get_rect(center = self.rect.center)
        
    def move_rects(self):
        super().move_rects()
        
        # self.weapon_hitbox.center = None
        
    def move_bars(self):
        pass