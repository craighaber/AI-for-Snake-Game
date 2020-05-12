This was a project to develop agents that are very good at playing the classic Snake Game. In summary,
the agents use a deep neural network to make a decision about which direction to move every frame, and
the weights for this network were learned through a genetic algorithm.

Check out the following website for a more detailed description of the project and demos:
https://craighaber.github.io/AI-for-Snake-Game/

There are 3 programs to check out in this project:
	
	playSnakeGame.py
		Try out the Snake Game yourself using the arrow keys!
	testTrainedAgents.py
		Observe some of the best Snake Game agents trained with the genetic algorithm!
	trainGeneticAlgorithm.py
		Observe how the process of training Snake Game agents functions from scratch!


***Dependecies***:
   1. Python version of 3.7 or higher.
   2. The Python library pygame.
        Type "pip install pygame" in the command prompt or terminal to install it.
        If necessary, more specific instructions for installing pygame are here:
        https://www.pygame.org/wiki/GettingStarted 


Now, for some more detailed instructions for each program if necessary:

	playSnakeGame.py

		Use the arrow keys to move up, down, left, or right.
		The goal is to get the snake as long as possible by eating fruit (the red squares)
		You will die and then automatically restart the game if:
			1. The snake hits a wall.
			2. The snake hits its own body.

	testTrainedAgents.py

		Follow the menu prompts in the command prompt/terminal to select which snake 
		you would like to observe, and then watch as the agent plays the game
		in a new window.

	trainGeneticAlgorithm.py

		Simply run the module to observe how the genetic algorithm was trained in action,
		starting from randomized chromosomes. 
		Specific information about each population is saved in Gadata.txt in the same 
		folder as this program, and the file will be created if it does not already exist
		after the first generation.
		Also, for every 10 populations, the population is saved in a file 
		in the populations directory.









