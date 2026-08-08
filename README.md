# Portal-Dungeon-python
A small top-down 2D dungeon crawler game made in python with pygame.

## Changes
Removed mx and my from bullet class

Added speed multipliers to tiles instead of doing it manually for each different tile

Changed collision with mud and snow to collide point

Adjusted positions of a few functions in some classes

Combined idle_move functions into one in the entity class
- square_move was created to allow different patterns in future

Added random move for idling

Made collidable_tiles list for each mob in tile_collision

Added a set velocity to each class:
- Removed idle_xvel and idle_yvel with idle_vel and sets xvel and yvel to idle_vel
- Allows one sync function (move part)

Removed some unnecessary comments

Made absolute value calcs better

Added info(bottom) text for doors and chests

Made the player hp and ep textbox only create when player is created not every frame

Made the player hearts rectangles only create when player is created

Recreated spawners class with creation function of enemies

Made the inputs faster by making them elif instead of lots of if

Removed display being passed in to the Button init func

Started testing having each game_state as a class:
- Just started with Main_Menu class
