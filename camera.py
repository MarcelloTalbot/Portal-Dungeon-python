# import pygame
from settings import *

class Camera(pygame.sprite.Group):
    def __init__(self, render_dist, sim_dist):
        super().__init__()
        #surface to draw everything to
        self.display_surface = pygame.display.get_surface()#display.get_rect()
        # print(self.display_surface.__sizeof__())
        #distance required to display images
        self.render_dist = render_dist
        #distance required to update sprites
        self.sim_dist = sim_dist
        #camera offset
        self.offset = pygame.math.Vector2()
        #midpoint of display
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2
        
        self.prev_size = 0

    def center_player_x(self, player):
        self.offset.x = player.rect.centerx - self.half_w#could be player.pos?

    def center_player_y(self, player):
        self.offset.y = player.rect.centery - self.half_h#could be player.pos?
        
    #for changing levels, player object should stay alive
    def c_empty(self):
        for sprite in self.sprites():
            if sprite.type != "player":
                sprite.kill()

    #       
    def c_draw(self, player, moves, tiles, m_pos, enemy_group, spawner_group, collectable_group, bullet_group, footprint_group, interactable_group, infobox):
        self.center_player_x(player)
        self.center_player_y(player)
        
        self.display_rect = self.display_surface.get_rect(center = player.pos)
        # self.display_rect = display.get_rect
        # self.__len__
        # toplefttile = (self.offset.x // tile_scale, self.offset.y // tile_scale)
        # bottomrighttile = ((player.rect.centerx + self.half_w) // tile_scale, (player.rect.centery + self.half_h) // tile_scale)#could be player.pos?
        # for r in range(toplefttile[1], bottomrighttile[1]):
        #     for c in range(toplefttile[0], bottomrighttile[0]):
        #         self.display_surface.blit(tiles[r][c].scal_image, tiles[r][c].pos - self.offset)
        
        #loops through sprites in ascending order of their z attributes
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.z):#should do self.sprites().sort(key = lambda sprite: sprite.z)
            
            if sprite.type == "portal":
                # dist_1 = player.pos.distance_to(sprite.pos_1)
                # dist_2 = player.pos.distance_to(sprite.pos_2)
                # if dist_1 <= self.render_dist or dist_2 <= self.render_dist:
                #     img_offset_pos_1 = sprite.rect_1.topleft - self.offset
                #     img_offset_pos_2 = sprite.rect_2.topleft - self.offset
                #     self.display_surface.blit(sprite.scal_image, img_offset_pos_1)
                #     self.display_surface.blit(sprite.scal_image, img_offset_pos_2)
                if self.display_rect.colliderect(sprite.rect_1) or self.display_rect.colliderect(sprite.rect_2):
                    img_offset_pos_1 = sprite.rect_1.topleft - self.offset
                    img_offset_pos_2 = sprite.rect_2.topleft - self.offset
                    self.display_surface.blit(sprite.scal_image, img_offset_pos_1)
                    self.display_surface.blit(sprite.scal_image, img_offset_pos_2)
                    
            else:
                # dist = player.pos.distance_to(sprite.pos)
            
                if self.display_rect.colliderect(sprite.rect):#dist <= self.render_dist:
                    img_offset_pos = sprite.rect.topleft - self.offset
                    
                    if sprite.type == "tile":
                        # self.display_surface.blit(sprite.rot_image, img_offset_pos)
                        display.blit(sprite.rot_image, img_offset_pos)
                        
                    elif sprite.type == "collectable":
                        self.display_surface.blit(sprite.rot_image, img_offset_pos)
                        sprite.update(player, tiles, interactable_group)
                        
                    elif sprite.type == "particle":
                        self.display_surface.blit(sprite.rot_image, img_offset_pos)
                        sprite.update()
                        
                    elif sprite.type == "chest":
                        self.display_surface.blit(sprite.image, img_offset_pos)
                        sprite.update(moves, player, collectable_group, self)
                        
                    elif sprite.type == "door":
                        self.display_surface.blit(sprite.image, img_offset_pos)
                        sprite.update(moves, player, enemy_group, collectable_group, infobox)
                        
                    elif sprite.type == "bullet":
                        self.display_surface.blit(sprite.scal_image, img_offset_pos)
                        sprite.update(tiles, player, enemy_group, spawner_group, interactable_group)
                        
                    elif sprite.type == "spawner":
                        self.display_surface.blit(sprite.scal_image, img_offset_pos)
                        sprite.update(enemy_group, player, collectable_group, img_offset_pos, self)
                    
                    else:
                        arm_offset_pos = sprite.arm_rect.topleft - self.offset
                        
                        dist = player.pos.distance_to(sprite.pos)
                        
                        if sprite.type == "entity":
                            self.display_surface.blit(sprite.rot_arm, arm_offset_pos)
                            self.display_surface.blit(sprite.rot_image, img_offset_pos)
                            sprite.update(player, tiles, dist, collectable_group, spawner_group, bullet_group, enemy_group, img_offset_pos, interactable_group, self)
                        
                        elif sprite.type == "tailed_entity":
                            tail_offset_pos = sprite.tail_rect.topleft - self.offset
                            self.display_surface.blit(sprite.rot_tail, tail_offset_pos)
                            self.display_surface.blit(sprite.rot_arm, arm_offset_pos)
                            self.display_surface.blit(sprite.rot_image, img_offset_pos)
                            sprite.update(player, tiles, dist, collectable_group, spawner_group, img_offset_pos, self)
                            
                        elif sprite.type == "player":
                            sprite.render(arm_offset_pos, img_offset_pos)
                            sprite.update(moves, tiles, m_pos, bullet_group, footprint_group, enemy_group, spawner_group, interactable_group, self)
    
    def calc_offset(self, player):
        self.center_player_x(player)
        self.center_player_y(player)
        
        #loops through sprites in ascending order of their z attributes
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.z):
            
            #offset from player
            try:#for all sprites with one rectangle - change to if maybe
                self.img_offset_pos = sprite.rect.topleft - self.offset
            except:#for portals as they have two rectangles
                self.img_offset_pos_1 = sprite.rect_1.topleft - self.offset
                self.img_offset_pos_2 = sprite.rect_2.topleft - self.offset
    
    def update(self, player, moves, tiles, m_pos, enemy_group, spawner_group, collectable_group, bullet_group, footprint_group, interactable_group):
        pass
        
    def render(self, player, moves, tiles, m_pos, enemy_group, spawner_group, collectable_group, bullet_group, footprint_group, interactable_group):
        pass
                    
            
            

        
