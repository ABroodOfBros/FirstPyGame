"""
Maze game

Player moves through each level trying to reach the exit. They can pick
up treasures if they wish. As long as the player is standing on something
they will not fall. If player falls to the bottom of the screen, they die.

The maze is made of multiple levels, like floors in a building. As the
player successfully reaches the exit in one level they move to the next.
when all levels have been completed they win!!!

Note: there must always be one and only one player.

   Key:
     P   player
     #   brick wall
     =   ladder
     @   treasure
     *   bomb
     X   exit
"""

# Include the game implementation
import MazeEngine

# Define the maze, which can have one or more levels.
Maze = [

# Level 0
# This is the first level so it is easiest. All the player has to do is make it
# to the top right corner to exit. If they wish, there are several treasures to
# acquire.

[ "#########################################################",
  "#                           #                           X",
  "#                           #                #####=######",
  "#                 @         #                     =     #",
  "# ########=##################                     =     #",
  "#         =                                       =     #",
  "#         =                                 =######     #",
  "#         =                                 =           #",
  "#         =                                 =           #",
  "#         #########=####################### =######     #",
  "#             #    =                        =           #",
  "#             #    =                        =           #",
  "#          @  #    =                        =           #",
  "#  ############    =                        =           #",
  "#                  =#############=###       =           #",
  "#                  =         #   =          =           #",
  "#                  =         #   =          =           #",
  "#                  =         #   =          =           #",
  "#                  =    ##########################      #",
  "#                  =                       #            #",
  "# #######=#############                    #            #",
  "#        =                                 #  @         #",
  "#        =                                 ###########  #",
  "#        =                                              #",
  "# P      =                                              #",
  "#########################################################" ],

# Level 1
# The first level took us up, so let's try going down this time.

[ "#########################################################",
  "#                           P                           #",
  "#                                                       #",
  "#      =################                                #",
  "#      =                                                #",
  "#      =                   ###                          #",
  "#      =                 #######                        #",
  "#      =               ###########                      #",
  "#      =             ###############                    #",
  "#      =           ###################                  #",
  "#      =           #                 #                  #",
  "#      =           #     #    @#     #                  #",
  "#      =           #     ###=###     #                  #",
  "#      =           #        =        #                  #",
  "#      =           #        =        #                  #",
  "#      =           #        =        #                  #",
  "#      =         *          =                           #",
  "#      =         #######################                #",
  "#      =                                                #",
  "#      =  #######                       #########       #",
  "#      =  #                                             #",
  "#      =  #                                             #",
  "#      ####                                          X  #",
  "#                                                ########",
  "#                                                       #",
  "#                                                       #" ],
]

if __name__ == "__main__":
	game = MazeEngine.Game()

	# present the player with each level, one at a time, until
	# they lose or complete all the levels!

	winner = True
	completed = 0
	for level in range(len(Maze)):
		game.load(Maze[level])
		if game.play():
			# player completed a level
			completed = completed + 1
		else:
			# sadly, the player failed at this level
			winner = False
			break;

	game.cleanup()

	if winner:
		print ("Contratulations, you are a winner!")
	elif completed > 0:
		print ("Nice work, you completed", completed, "levels.")
	else:
		print ("Did you even try? I think not!")

