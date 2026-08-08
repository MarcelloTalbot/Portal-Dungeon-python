import pygame
from settings import *

class Camera(pygame.sprite.Group):
    def __init__(self,render_dist,sim_dist):
        super().__init__()
        #surface to draw everything to
        self.display_surface = pygame.display.get_surface()
        #distance required to display images
        self.render_dist = render_dist
        #distance required to update sprites
        self.sim_dist = sim_dist
        
        #camera offset
        self.offset = pygame.math.Vector2()
        #midpoint of display
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

    def center_player_x(self,player):
        self.offset.x = player.rect.centerx - self.half_w

    def center_player_y(self,player):
        self.offset.y = player.rect.centery - self.half_h
        
    #for changing levels, player object should stay alive
    def c_empty(self):
        for sprite in self.sprites():
            if sprite.type != "player":
                sprite.kill()

    def c_draw(self,player,moves,tiles,mx,my,enemy_group,spawner_group,collectable_group,bullet_group,footprint_group,interactable_group):
        
        self.center_player_x(player)
        self.center_player_y(player)
        
        #loops through sprites in ascending order of their z attributes
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.z):
            
            #offset from player
            try:#for all sprites with one rectangle
                img_offset_pos = sprite.rect.topleft - self.offset
            except:#for portals as they have two rectangles
                img_offset_pos_1 = sprite.rect_1.topleft - self.offset
                img_offset_pos_2 = sprite.rect_2.topleft - self.offset

            #different objects have different parameters for updating
            if sprite.type == "tile":
                self.display_surface.blit(sprite.rot_image,img_offset_pos)
            elif sprite.type == "portal":
                self.display_surface.blit(sprite.scal_image,img_offset_pos_1)
                self.display_surface.blit(sprite.scal_image,img_offset_pos_2)
                #sprite.update()
            elif sprite.type == "chest":
                self.display_surface.blit(sprite.image,img_offset_pos)
                sprite.update(moves,player,collectable_group)
            elif sprite.type == "door":
                self.display_surface.blit(sprite.image,img_offset_pos)
                sprite.update(moves,player)
            elif sprite.type == "player":
                arm_offset_pos = sprite.arm_rect.topleft - self.offset
                sprite.render(arm_offset_pos,img_offset_pos)
                #self.display_surface.blit(sprite.rot_arm,arm_offset_pos)
                #self.display_surface.blit(sprite.rot_image,img_offset_pos)
                #sprite.render_bars()
                #sprite.render_text()
                #sprite.render_hearts()
                #sprite.render_weapon_show()
                if sprite.update(moves,tiles,mx,my,bullet_group,footprint_group,enemy_group,spawner_group,interactable_group):
                    return True
            #tile,portal,player should always be rendered and updating
            else:
                #calculates distance from the sprite to the player
                dist = player.pos.distance_to(sprite.pos)
            
                if dist <= self.render_dist:
                    if sprite.type == "particle":
                        self.display_surface.blit(sprite.rot_image,img_offset_pos)
                        if dist <= self.sim_dist:
                            sprite.update()
                    elif sprite.type == "collectable":
                        self.display_surface.blit(sprite.rot_image,img_offset_pos)
                        if dist <= self.sim_dist:
                            sprite.update(player)
                    elif sprite.type == "bullet":
                        self.display_surface.blit(sprite.scal_image,img_offset_pos)
                        if dist <= self.sim_dist:
                            sprite.update(tiles,mx,my,player,enemy_group,spawner_group,interactable_group)
                    elif sprite.type == "spawner":
                        self.display_surface.blit(sprite.scal_image,img_offset_pos)
                        if dist <= self.sim_dist:
                            sprite.update(enemy_group,player,collectable_group,img_offset_pos)
                    elif sprite.type == "tailed_entity":
                        arm_offset_pos = sprite.arm_rect.topleft - self.offset
                        tail_offset_pos = sprite.tail_rect.topleft - self.offset
                        self.display_surface.blit(sprite.rot_tail,tail_offset_pos)
                        self.display_surface.blit(sprite.rot_arm,arm_offset_pos)
                        self.display_surface.blit(sprite.rot_image,img_offset_pos)
                        if dist <= self.sim_dist:
                            sprite.update(player,tiles,dist,collectable_group,spawner_group,img_offset_pos)
                    elif sprite.type == "entity":
                        arm_offset_pos = sprite.arm_rect.topleft - self.offset
                        self.display_surface.blit(sprite.rot_arm,arm_offset_pos)
                        self.display_surface.blit(sprite.rot_image,img_offset_pos)
                        if dist <= self.sim_dist:
                            sprite.update(player,tiles,dist,collectable_group,spawner_group,bullet_group,enemy_group,img_offset_pos,interactable_group)
                    
                    
            
            

        
