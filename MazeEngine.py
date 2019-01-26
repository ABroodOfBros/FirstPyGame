"""
Add some notes here
"""

from pygame.locals import *
import pygame

# Dimensions of image files used is 32x32
IMAGE_HEIGHT = 32
IMAGE_WIDTH  = 32

class Game:
	def __init__(self):
		pygame.init()

	def load(self,level):
		self.level  = level
		self.height = len(level)
		self.width  = len(level[0])

		self.screen = pygame.display.set_mode([self.width*IMAGE_WIDTH,self.height*IMAGE_HEIGHT])
		self.clock  = pygame.time.Clock()

		# load images needed to draw the screen
		self.player   = pygame.image.load('human.png').convert()
		self.brick    = pygame.image.load('brick.png').convert()
		self.ladder   = pygame.image.load('ladder.png').convert()
		self.treasure = pygame.image.load('treasure.png').convert()
		self.bomb     = pygame.image.load('bomb.png').convert()
		self.exit     = pygame.image.load('exit.png').convert()
		self.blank    = pygame.image.load('blank.png').convert()

		self.player_location = [0,0]
		self.player_died = False
		self.player_wins = False

	def render_player(self,x,y):
		location = [x*IMAGE_WIDTH, y*IMAGE_HEIGHT]

		self.screen.blit(self.player,location)

	def render_object(self,x,y):
		location = [x*IMAGE_WIDTH, y*IMAGE_HEIGHT]

		if self.level[y][x] == '#':
			self.screen.blit(self.brick,location)
		elif self.level[y][x] == '=':
			self.screen.blit(self.ladder,location)
		elif self.level[y][x] == '@':
			self.screen.blit(self.treasure,location)
		elif self.level[y][x] == '*':
			self.screen.blit(self.bomb,location)
		elif self.level[y][x] == 'X':
			self.screen.blit(self.exit,location)
		else:
			self.screen.blit(self.blank,location)

	def move_blocked(self,x,y):
		blocked = False
		if self.level[y][x] == '#':
			blocked = True
		return blocked

	def player_falling(self,x,y):
		falling = False
		# look at block under player, to see if something under him
		if self.level[y+1][x] == ' ':
			falling = True
		return falling

	def player_exited(self,x,y):
		blocked = False
		if self.level[y][x] == 'X':
			blocked = True
		return blocked

	def player_blowed_up(self,x,y):
		blowedup = False
		if self.level[y][x] == '*':
			blowedup = True
		return blowedup

	def player_found_treasure(self,x,y):
		treasure = False
		if self.level[y][x] == '@':
			treasure = True
			# FIXME: should only be able to get a treasure once
		return treasure

	def player_out_of_bounds(self,x,y):
		out_of_bounds = False
		if x < 0:
			out_of_bounds = True
		elif x >= self.width:
			out_of_bounds = True
		elif y < 0:
			out_of_bounds = True
		elif y >= self.height:
			out_of_bounds = True
		return out_of_bounds

	def play(self):
		# draw the screen
		for y in range(self.height):
			for x in range(self.width):
				# draw block in maze
				self.render_object(x,y)

				# if player, then remember his location
				if self.level[y][x] == 'P':
					self.player_location = [x,y]

		# limit allowable events to key presses only (supposed to make game faster ;)
		pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

		while not self.player_died:
			# read any new events that came in, e.g. key presses
			pygame.event.pump()

			# Check if player done with this level. There are a few ways to get out:
			# 1) player dies,
			# 2) player asks to quit, or
			# 3) player reaches the exit

			# check if player died (went out of bounds, got blown up, etc...)
			if self.player_out_of_bounds(self.player_location[0],self.player_location[1]):
				print ("You fell off the map!")
				player_died = True

			if self.player_blowed_up(self.player_location[0],self.player_location[1]):
				print ("BOOM! What a terrible wayt to die!")
				self.player_died = True

			# check if player asked to quit
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.player_died = True

			# check if player wins
			if self.player_exited(self.player_location[0],self.player_location[1]):
				print ("You reached the exit!")
				self.player_wins = True

			# check if player found treasure
			if self.player_found_treasure(self.player_location[0],self.player_location[1]):
				print ("You found treasure!")
			
			# if this level is done, then break out of the loop (returns back to caller)
			if self.player_wins or self.player_died:
				break

			# if nothing below the player, then they fall down a block
			if self.player_falling(self.player_location[0], self.player_location[1]):
				# redraw what was under the player so it shows up after they fall
				self.render_object(self.player_location[0], self.player_location[1])
				self.player_location[1] = self.player_location[1] + 1

			# figure out which way the player moved
			x_diff = 0
			y_diff = 0

			keys = pygame.key.get_pressed()
			if (keys[K_RIGHT]):
				x_diff = 1
			if (keys[K_LEFT]):
				x_diff = -1
			if (keys[K_DOWN]):
				y_diff = 1
			if (keys[K_UP]):
				y_diff = -1

			# if the player moved, make sure the path is not blocked by a wall
			if x_diff or y_diff:
				# figure out new player location, and check if it is valid
				new_x = self.player_location[0] + x_diff
				new_y = self.player_location[1] + y_diff
				if not self.move_blocked(new_x, new_y):
					# redraw what was under the player so it shows up after they move
					self.render_object(self.player_location[0], self.player_location[1])
					# move the player to the new location
					self.player_location[0] = new_x
					self.player_location[1] = new_y

			self.render_player(self.player_location[0], self.player_location[1])

			pygame.display.flip()
			self.clock.tick(20)

		return self.player_wins

	def cleanup(self):
		pygame.quit()

