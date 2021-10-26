import os, subprocess, time, signal
import gym
from gym import error, spaces, utils
from gym.utils import seeding
# from gym_snake.envs.snake import Controller, Discrete
import pygame
from gym_snake.envs.snakeGameGym import *
import matplotlib.pyplot as plt

try:
    import matplotlib.pyplot as plt
    import matplotlib
except ImportError as e:
    raise error.DependencyNotInstalled("{}. (HINT: see matplotlib documentation for installation https://matplotlib.org/faq/installing_faq.html#installation".format(e))

class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        fps = 3000
        self.game = SnakeGameGym(fps)

        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=3, shape=(self.game.cols, self.game.rows), dtype=int)
        pygame.font.init()   


    def step(self, action):
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

    def reset(self):
        observation = self.game.get_board()
        self.game.game_over()
        return observation
        


    def render(self, mode='human'):
        observation = self.game.get_board()

        if mode == "array":
            return observation

        elif mode == "human":
            p = plt.imshow(observation)

            return p.figure

        else:
            # Will raise an appropriate exception
            return super().render(mode=mode)

    def seed(self, x):
        pass
