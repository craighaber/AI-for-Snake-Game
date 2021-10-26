import os, subprocess, time, signal
import gym
from gym import error, spaces, utils
from gym.utils import seeding
# from gym_snake.envs.snake import Controller, Discrete
import pygame
from gym_snake.envs.snakeGameGym import *


try:
    import matplotlib.pyplot as plt
    import matplotlib
except ImportError as e:
    raise error.DependencyNotInstalled("{}. (HINT: see matplotlib documentation for installation https://matplotlib.org/faq/installing_faq.html#installation".format(e))

class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, grid_size=[15,15], unit_size=10, unit_gap=1, snake_size=3, n_snakes=1, n_foods=1, random_init=True):
        fps = 3000
        self.game = SnakeGameGym(fps)

        self.action_space = spaces.Discrete(4)
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

        info = None
        return observation, rewards, done, info

    def reset(self):
        observation = self.game.get_board()
        self.game.game_over()
        return observation
        


    def render(self, mode='human', close=False, frame_speed=.1):
        pass

    def seed(self, x):
        pass
