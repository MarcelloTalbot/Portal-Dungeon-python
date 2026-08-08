# Portal-Dungeon-python
A small top-down 2D dungeon crawler game made in python with pygame.

## Changes
Changed how the level is changed by moving parts into the player

Changed prev stats to be inside the player class

Changed spawning enemies to use the spawner class function instantly instead of creating its own and saving it

Almost got update_1_1 working in Game class

Improved camera c_draw a bit so less laggy:- Not separated into update and render
- Changed rendering to be if the sprite rect is colliding with the screen rect instead of a distance to the player

Added a stats save feature for pause, death, win and game over screens

Changed how sprinting works: - might change again or revert back
- Only on player for now (not menu player)

Made sure all next_state were correct

Fixed respawn, retry and continue buttons to no go back to prev state but playing:
- Might make a new prev_play_state to pass into them instead

Changed how escape works on a few game state

Moved pygame.init() into the main.py instead of settings.py

Added a push feature to collectables to move them out of tiles that the player can collide with and doors

Changed chest and doors again to be better and actually be in the game

Created top-down pistol image to be shown when it's equipped

Removed rotate function in footprints cos it was useless

Gave bullets a self.vel as well

Made bullets not need to pass angle into the init

Designed a new level_load to make level_group as a matrix storing the tiles t_type: im just too smart

Designed a new tile_collision to use new calc_path which gets the matrix position of tiles that the sprite will cross: im just too smart

Started creating the new designed functions (Finish next version cos its getting messy and don't want to remove stuff for some reason \o_o/)

# Bugs
When enemies are near edge of screen they move weirdly
