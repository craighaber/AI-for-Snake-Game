import gym
import pygame
from typing import Union
from typing import Callable
from gym import spaces
from numpy import ndarray
from gym_snake.envs.snakeGameGym import *
from gym_snake.envs.snakeRewardFuncs import *


class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, 
        board_height: int = 10, 
		board_width:int = 10,  
		max_moves_no_fruit: int = 0,
		use_pygame: bool = True, 
		fps: int = 3000,
        reward_func: Callable[..., float] = basic_reward_func,
        represent_border: bool = False):
        """
        Initializes the custom Snake gym environment.

		board_height: the number of rows on the game board. defaults to 10.
		board_width: the number of columns on the game board. defaults to 10.
        max_moves_no_fruit: number of allowed consecutive moves that do not result in fruit consumption. 
									   Non-positive values correspond to no limit.
		use_pygame: boolean flag for whether or not to visualize the environment with pygame. defaults to True.
		fps: sets the speed of the game in frames per second.
        reward_func: a function that takes any inputs (representing important game states) and returns an 
                     int output representing a reward for the snake agent based on the inputs. 
                     Defaults to snakeRewardFunc.basic_reward_func()
        represent_border: boolean flag for whether or not to represent the border in observation.
        """
        self.viewer = None

        if use_pygame:
            pygame.font.init()
            self.fps = fps
        self.game = SnakeGameGym(board_height, board_width, max_moves_no_fruit, use_pygame)

        self.reward_func = reward_func
        self.action_space = spaces.Discrete(4)

        # Create Observation Space
        # Border requires two additional rows and columns
        obs_rows = self.game.rows + int(represent_border) * 2
        obs_cols = self.game.cols + int(represent_border) * 2
        self.observation_space = spaces.Box(low=0, high=3, shape=(obs_cols, obs_rows), dtype=int)  # TODO: make sure (cols, rows) is correct order
        self.represent_border = represent_border
           


    def step(self, action: spaces.Discrete(4)) -> tuple:
        """
        Function that is called at every update in the game state (i.e., every move)

        action: a discrete set (0,1,2,3) that corresponds to a movement direction for the snake
        """
        # Check to make sure action is valid
        err_msg = "%r (%s) invalid" % (action, type(action))
        assert self.action_space.contains(action), err_msg
        
        # Play one frame of Snake Game
        self.game.move_snake(action)

        # Increment necessary game states
        self.game.increment_moves_since_fruit()

        # check collisions after move
        did_consume_fruit = self.game.check_fruit_collision()
        did_collide_wall = self.game.check_wall_collision()
        did_collide_body = self.game.check_body_collision()
        did_move_closer_to_fruit = self.game.check_closer_to_fruit()

        # Check if snake exceeded threshold of max moves without consuming fruit
        did_exceed_max_moves_no_fruit = self.game.check_exceeded_max_moves()

        # Get observation after move
        observation = self.game.get_board(self.represent_border)

        # Get rewards based on collision status
        reward_dict = {
            "did_consume_fruit":did_consume_fruit,
            "did_collide_wall": did_collide_wall,
            "did_collide_body": did_collide_body,
            "did_exceed_max_moves_no_fruit": did_exceed_max_moves_no_fruit,
            "did_move_closer_to_fruit": did_move_closer_to_fruit
        }
        rewards = self.reward_func(reward_dict)

        # Game is over if wall collision, body collision, or too many moves before consuming a fruit occurred.
        done = did_collide_wall or did_collide_body or did_exceed_max_moves_no_fruit

        # FIXME: Figure out what to do with info. stable_baseline3 seems to require episode object
        info = {"episode": None}  

        # If there was a fruit collision during last frame, move the fruit.
        if did_consume_fruit:
            self.game.respond_to_fruit_consumption()
            self.game.reset_moves_since_fruit()

        # If game over, reset moves taken since consuming fruit to 0
        if done:
            self.game.reset_moves_since_fruit()
        
        if self.game.use_pygame:
            self.game.clock.tick(self.fps)
            self.game.redraw_window()

        return observation, rewards, done, info

    def reset(self) -> ndarray:
        """
        Function that collects the game board observation, ends the game,
        and returns the observation.
        """
        observation = self.game.get_board(self.represent_border)
        self.game.game_over()

        # game_over sets restart to  true. It then needs to be reset to false. 
        # FIXME: doesn't seem like restart is necessary
        self.game.restart = False

        return observation
        
    def render(self, mode='human') -> Union[ndarray, None]:
        """
        Function that renders the training process of the Gym env.

        Available modes offer graphical or non-graphical training

        NOTE: As of now, this render function is NOT working. Evidently,
        SimpleImageViewer is not that simple
        """
        observation = self.game.get_board(self.represent_border)

        #Non-graphical
        if mode == "array":
            return observation

        #Graphical
        elif mode == "human":
            if self.viewer is None:
                from gym.envs.classic_control import rendering

                self.viewer = rendering.SimpleImageViewer()

            # Stretches array since this is not done by viewer https://stackoverflow.com/a/4227280/11892023
            im = np.repeat(np.repeat(observation,100, axis=0), 100, axis=1)
            
            # Create three channel array where each channel is same size as observation
            num_channels = 3
            im_grey = np.zeros(((im.shape[0], im.shape[1], num_channels)))
            
            # For each channel, set pixel values based on scaled observation
            for channel_i in range(num_channels):
                im_grey[:, :, channel_i] = (im / im.max())*255

            self.viewer.imshow(im_grey)
            return self.viewer.isopen

        else:
            # Will raise an appropriate exception
            return super().render(mode=mode)

    def close(self) -> None:
        if self.viewer is not None:
            self.viewer.close()
            self.viewer = None

    def seed(self, x):
        """
        FIXME: Read Gym docs on how seed should be used for custom envs and implement.
        """
        pass
