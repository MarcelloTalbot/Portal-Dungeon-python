# Portal-Dungeon-python
A small top-down 2D dungeon crawler game made in python 3.11 with pygame.

## Controls
Movement: W, A, S, D
Sprint: Left Shift
Attack: Left Click, Space
Change weapon: Scroll Wheel, Q
Interact: Right Click
Pause/Quit/go back: Escape

## Run
Download all the items into the same directory and run the main.py file.

## Changes
Finished creating new tile matrix, calc_path (and almost tile_collisions)

Not done - Changed up, down, left and right _pressed into 2 x_dir and y_dir

Made improved on display text classes

Fixed sprint against walls by making calc path be before it

Moved it back because I should add righted, lefted, upped, and downed for stuff maybe (if this done remove "ratio *" from the calc_path func for top_r and bottom_num

Added portals back in and fixed changing levels

Started a new Tile classes

Changed portal image to be transparent instead of have grass as background

Removed render distance

Cleaned up the image directories

Added text to show you can interact with chests, doors and portals

Made an improved enemy movement so they can go directly to the player

Improved player bar rendering and bar text

Improved central text drawing

Improved tile_collisions to use tile_matrix and made mud and snow slow you down again with footprints

Tried to make more calc_path functions to test improvements

Moved level back into Playing class out of Player class

Made the player spawn where the 'P' is in the level file

## Bugs
Going perfectly diagonal on collidable tiles corners allows you to go through them (with calc_path no _better)

Going diagonal whilst touching a line of walls make you pause in some directions at boundaries (with calc_path_better)

When enemies are near edge of screen they move weirdly

## Planned
Reduce size of entity file by reducing copied code

Fix collisions

Push entities out of doors

Make a better controls menu

Better energy system

Add heal

More and better levels - tower layout (only up or down after a certain level)

More enemies

More collectables

Items

More weapons

Classes and/or upgrades

More chests

Coin combining

Shop

Dungeons

Buildings - wood walls

Better brick walls

Water

Damaging tiles

Effects - fire, poison, etc

Other tiles - sand, dirt, deep snow + (add stairs back :D)

Fix aspect ratio for everything - no + or - when positioning

Bottom screen text for event input - portals - energy cost

Continue button in main menu for when the game is paused and they go back to main instead of play button

Fix lag - max sprite amount - max sprites from spawners

Multiple saves

Leaderboard

Application as in an app (noun)

Re-order methods in the classes

Add (useful) comments (in code)

Remove useless stuff

Global timer so only one timer for all instances of entities

Put interactables (doors, chests and portal) in a new txt file for loading or portals into the entities file:
- Make portals as interactables

The prev_ variables in the game loop can be removed if the player entity and other player values are separated or player entity doesn't actually die when it dies (maybe)

Actually use delta time (dt)

Make it so the images aren't passed into the init function of classes

Different Difficulties

Move the part of the sync functions into the move function that should be there

Add object pooling (bullets don't die and have to recreate them just move back to thing that shot it or stop rendering and updating)

Render function in classes and run in camera instead of all the blits

Change bullet inheritance to entity instead of object

Change render dist and sim dist to be separate in camera

Make the info text as part of the player and have a list of interactables

Make interactable action parameters as one so inheritance can be done for change_state

Change , remove or use s_num and s_spawn

Move bullet velocity calc into create bullet

Change mx and my with m_pos

Move mouse_hover func in Button class to menu_player class as buttons in other game_state don't need to check for collisions

See if I can remove the self.group in the buttons class

Add each button type

Use dirty sprites properly or change to layered sprites?

Use Vector2 properly

Add restart and continue when a save is made

Change textbox code to use pygame.freetype

When checking for mouse clicks use event.pos instead of getting the mouse pos and using it later

Merge portal creation code in load_level

Calculate max bullets on screen for each sprite and initialise that many when the sprite is initialised (object pooling)

## Possible
Make doors be tiles that just change colour

Make all entity collision detection happen outside of each entity class

Maybe remove .z as it is not used in the new camera

Change respawn to be where the user died and not the beginning of the level

Make velocity have a set velocity - (self.vel, self.xvel, self.yvel) or using dir - allows for better inheritance

Make respawn protection cause invisibility (if respawn at same pos)

In-between level like in dead cells

Repeatable like dead cells - harder each time after boss (Unlockable difficulties kinda)

Different levels to go to from each one like in Gauntlet IV and dead cells - can go back(Gauntlet IV) - can't go back(dead cells)

Separate game loop into multiple loops separated by inputs and updates (if input take a cycle to affect anything)

Change from OOP to ECS?

Different game modes - campaign (as is), adventure and/or sandbox (Minecraft/Terraria) (with building and crafting?)

Paurak's mode - go up or down to heaven or hell with dragons and stuff

Make info text and interactions to be done at a set dist not a collide - Or interactions when facing them

Interactables with needing keys could have a list of sprites with the key

Is having return before super() better?

Give each button their own class if images are removed as parameters

Change the Quit_Menu game state to an are you sure game state with a variable outcome for different things

Make some of the game states pop-ups instead in a new class, basically a separate returning state that doesn't change the game.game_state

Have the Main_Menu class be what the Game class is now and have the different game_state appear inside it and each other:
- Main_Menu
  - Playing
    - Paused
      - Quit_Menu
      
	- Death_screen
      - Quit_Menu
      
	- Win_Screen
      - Quit_Menu
      
	- Game_over
      - Quit_Menu
  
  - Options/controls
    - different sub options
   
  - Quit_Menu

- This is can remove prev_state from game states
- Can copy the Game class update into each game state class each having their own sub game state
- Wouldn't need a global variables function or settings as they could be passed down the chain(maybe)

Use the pygame.RESIZABLE in the pygame.display.set_mode() and use pygame.VIDEORESIZE in the input detection:
- Might need to move the input detection outside of each game state class

Make sprinting be like mincrafts with just a press needed

Change game update() to use exec() instead of globals()

Use collidedict and set dictionaries of hitboxes for collisions

Make hitbox and rect the dame for sprites?

Reorder import maybe

Have a bar (yellow) underneath spawners showing when they'll next spawn an enemy or a visual way of showing it

When enemies die check if they could be spawned in later by a spawner (without a max_e_count?)

Initialise all spawners enemies at the level beginning

Move input detection to game

Don't do checks but change the used function maybe
