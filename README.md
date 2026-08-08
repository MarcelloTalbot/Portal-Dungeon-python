# Portal-Dungeon-python
A small top-down 2D dungeon crawler game made in python with pygame.

## Changes
Moved button code into separate class

Changed portals to need a key press to teleport
- this allowed me to remove the update procedure for the portal

Changed sprint to just left shift so tile using (teleporting through portals) is now right mouse click

Made travelling through blue portals cost energy (may remove)

Added retry, main and quit buttons to the win and game over screens
- simplified the code for these two sections
- moved the first level loading into the playing code and added a code so that the level would reset
- Combined the game over and win state into the same if statement by changing the game state value to a string outputted (may change if differences are needed)

Reset the menu players position when the game is playing

Added a continue/resume button to the pause screen

Fixed the score going below zero

Added a quit verification screen
- changed what escape does on different screens
- added yes and no buttons
- added previous game state variables to go back when no or escape is pressed

Added a death screen
- added respawn button
- added lives textbox - in pause screen too

Fixed the spite creation procedure to set the to spawn at the center of tiles so they can now spawn next to walls

Added Interactables class which includes chests and doors
- bronze, iron and gold chests so far
- right mouse click to open chests and open/close doors
- Doors
- many different orientations

Improved textbox naming

Added respawn protection(maybe)
	
