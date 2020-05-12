#*********************************************************************************
#playSnakeGame.py
#Author: Craig Haber
#5/9/2020
#This program allows the user to play the Snake Game. Maybe you will do better than
#the AI! You can find out how well the AI preforms by running testTrainedAgents.py.
#*********************************************************************************
#Instructions: 
#Use the arrow keys to move up, down, left, or right.
#The goal is to get the snake as long as possible by eating fruit (the red squares)
#You will die and then automatically restart the game if:
#	1. The snake hits a wall.
#	2. The snake hits its own body.
#*********************************************************************************
#Dependecies: 
#
#To run this module, you must have the module pygame installed.
#Type pip install pygame in the command prompt or terminal to install it.
#If necessary, more specific instructions for installing pygame are here:
#https://www.pygame.org/wiki/GettingStarted 
#
#Also, a Python version of 3.7 or higher is required.
#*********************************************************************************

import pygame
from helpers.snakeGame import *

def main():
	"""Function to play the Snake Game."""

	fps = 8
	game = SnakeGame(fps)
	pygame.font.init()

	while game.play:
		#Lock the game at a set fps
		game.clock.tick(game.fps)
		
		game.move_snake()
		game.check_collisions()

		if game.restart == True:
			game.restart = False
			continue
		
		game.redraw_window()
		game.event_handler()

		
if __name__ == "__main__":
	main()