# import pygame
from settings import *

class Camera():#tuple
    def __init__(self, sim_dist):
        super().__init__()
        #surface to draw everything to
        self.display_surface = pygame.display.get_surface()#display.get_rect()
        # print(self.display_surface.__sizeof__())
        
        #distance required to update sprites
        self.sim_dist = sim_dist
        
        #camera offset
        self.offset = pygame.math.Vector2()
        
        #midpoint of display
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2
        
        # self.groups = []
        
        # self.prev_size = 0

    def center_player_x(self, player):
        self.offset.x = player.rect.centerx - self.half_w#could be player.pos?

    def center_player_y(self, player):
        self.offset.y = player.rect.centery - self.half_h#could be player.pos?
        
    #for changing levels, player object should stay alive
    # def c_empty(self):
    #     for sprite in self.sprites():
    #         if sprite.type != "player":
    #             sprite.kill()
    
    def calc_screen_dims(self):
        self.display_surface = pygame.display.get_surface()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2
                
    def draw(self, player, moves, player_group, portals, level, level_matrix, tiles, m_pos, enemy_group, spawner_group, collectable_group, bullet_group, footprint_group, interactable_group, infobox):
        self.center_player_x(player)
        self.center_player_y(player)
        
        self.display_rect = self.display_surface.get_rect(center = player.pos)
        # self.display_rect = display.get_rect
        
        #corner tiles that are on the screen
        if self.offset.x >= 0:
            top_x = int(self.offset.x / tile_scale)
        else:
            top_x = 0
            
        if self.offset.y >= 0:
            top_y = int(self.offset.y / tile_scale)
        else:
            top_y = 0
            
        bottom_offset_x = player.rect.centerx + self.half_w
        bottom_offset_y = player.rect.centery + self.half_h
        
        max_c = len(level_matrix[level])
        max_r = len(level_matrix)
        
        if bottom_offset_x <= max_c:
            bottom_x = int(bottom_offset_x / tile_scale)
        else:
            bottom_x = max_c
            
        if bottom_offset_y <= max_r:
            bottom_y = int(bottom_offset_y / tile_scale)
        else:
            bottom_y = max_r
        
        # toplefttile = (top_x, top_y)
        # bottomrighttile = (bottom_x, bottom_y)#could be player.pos?
        # print(top_y)
        # print(bottom_x)
        #renders all tiles on the screen
        for r in range(top_y, bottom_y):#toplefttile[1], bottomrighttile[1]):
            # print(len(level_matrix[r]))
            for c in range(top_x, bottom_x):#toplefttile[0], bottomrighttile[0]):
                # print(str(r)+" "+str(c))
                # print(level)
                self.display_surface.blit(level_matrix[r][c].rot_image, level_matrix[r][c].pos - self.offset)
                
        # player_group = pygame.sprite.Group()
        groups = [footprint_group, spawner_group, interactable_group, collectable_group, bullet_group, enemy_group, player_group]        
        
        for p in portals:
            if self.display_rect.colliderect(p.rect_1):
                img_offset_pos = p.rect_1.topleft - self.offset
                self.display_surface.blit(p.scal_image, img_offset_pos)
            if self.display_rect.colliderect(p.rect_2):
                img_offset_pos = p.rect_2.topleft - self.offset
                self.display_surface.blit(p.scal_image, img_offset_pos)
        
        #rendering sprites
        for group in groups:
            # print(group)
            for sprite in group.sprites():
                if self.display_rect.colliderect(sprite.rect):
                    img_offset_pos = sprite.rect.topleft - self.offset
                    
                    if sprite.type == "collectable":
                        self.display_surface.blit(sprite.rot_image, img_offset_pos)
                        sprite.update(player, tiles, interactable_group)
                        
                    elif sprite.type == "particle":
                        self.display_surface.blit(sprite.rot_image, img_offset_pos)
                        sprite.update()
                        
                    elif sprite.type == "chest":
                        self.display_surface.blit(sprite.image, img_offset_pos)
                        sprite.update(moves, player, collectable_group, infobox)#, self)
                        
                    elif sprite.type == "door":
                        self.display_surface.blit(sprite.image, img_offset_pos)
                        sprite.update(moves, player, enemy_group, collectable_group, infobox)
                        
                    elif sprite.type == "bullet":
                        self.display_surface.blit(sprite.scal_image, img_offset_pos)
                        sprite.update(tiles, player, enemy_group, spawner_group, interactable_group)
                        
                    elif sprite.type == "spawner":
                        self.display_surface.blit(sprite.scal_image, img_offset_pos)
                        sprite.update(enemy_group, player, collectable_group, img_offset_pos)#, self)
                        
                    else:
                        arm_offset_pos = sprite.arm_rect.topleft - self.offset
                            
                        dist = player.pos.distance_to(sprite.pos)
                        
                        if sprite.type == "entity":
                            self.display_surface.blit(sprite.rot_arm, arm_offset_pos)
                            self.display_surface.blit(sprite.rot_image, img_offset_pos)
                            sprite.update(player, tiles, dist, collectable_group, spawner_group, bullet_group, enemy_group, img_offset_pos, interactable_group)#, self)
                        
                        elif sprite.type == "tailed_entity":
                            tail_offset_pos = sprite.tail_rect.topleft - self.offset
                            
                            self.display_surface.blit(sprite.rot_tail, tail_offset_pos)
                            self.display_surface.blit(sprite.rot_arm, arm_offset_pos)
                            self.display_surface.blit(sprite.rot_image, img_offset_pos)
                            sprite.update(player, tiles, dist, collectable_group, spawner_group, img_offset_pos)#, self)
                            
                        elif sprite.type == "player":
                            sprite.render(arm_offset_pos, img_offset_pos)
                            sprite.update(moves, level_matrix, m_pos, portals, bullet_group, footprint_group, enemy_group, spawner_group, interactable_group, infobox)#, self)
        