import gym
import pygame
from typing import Union
from gym import error, spaces
from gym.utils import seeding
from numpy import ndarray
from numpy.lib.index_tricks import nd_grid
from gym_snake.envs.snakeGameGym import *

try:
    import matplotlib.pyplot as plt
except ImportError as e:
    raise error.DependencyNotInstalled("{}. (HINT: see matplotlib documentation for installation https://matplotlib.org/faq/installing_faq.html#installation".format(e))

class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        fps = 3000
        self.viewer = None
        self.game = SnakeGameGym(fps)

        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=3, shape=(self.game.cols, self.game.rows), dtype=int)
        pygame.font.init()   


    def step(self, action: spaces.Discrete(4)) -> tuple:
        # Check to make sure action is valid
        err_msg = "%r (%s) invalid" % (action, type(action))
        assert self.action_space.contains(action), err_msg

        # Get current Observation
        observation = self.game.get_board()

        self.game.clock.tick(self.game.fps)
        
        self.game.move_snake(action)
        rewards = self.game.check_collisions()
        
        done = self.game.restart

        if self.game.restart == True:
            #  FIXME: restart is used to indicate whether game was forced over during
            # self.game.check_collisions(). This seems to be a non-ideal way of achieving this.
            self.game.restart = False
            # continue FIXME: this was within a loop originally
        
        self.game.redraw_window()

        info = {"episode": None}  # FIXME: Figure out what to do with info. stable_baseline3 seems to require episode object

        return observation, rewards, done, info

    def reset(self) -> ndarray:
        """
        Function that collects the game board observation, ends the game,
        and returns the observation.
        """
        observation = self.game.get_board()
        self.game.game_over()

        return observation
        
    def render(self, mode='human') -> Union[ndarray, None]:
        """
        Function that renders the training process of the Gym env.

        Available modes offer graphical or non-graphical training
        """
        observation = self.game.get_board()

        #Non-graphical
        if mode == "array":
            return observation

        #Graphical
        elif mode == "human":
            if self.viewer is None:
                from gym.envs.classic_control import rendering

                self.viewer = rendering.SimpleImageViewer()

            # Create three channel array where each channel is same size as observation
            num_channels = 3
            observation_grey = np.zeros(((observation.shape[0], observation.shape[1], num_channels)))
            
            # For each channel, set pixel values based on scaled observation
            scaled_observation = observation / observation.max()
            for channel_i in range(num_channels):
                observation_grey[:, :, channel_i] = scaled_observation

            self.viewer.imshow(observation_grey)
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
