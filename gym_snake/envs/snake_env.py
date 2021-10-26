import os, subprocess, time, signal
import gym
from gym import error, spaces, utils
from gym.utils import seeding
# from gym_snake.envs.snake import Controller, Discrete
import pygame
from gym_snake.envs.snakeGame import *


try:
    import matplotlib.pyplot as plt
    import matplotlib
except ImportError as e:
    raise error.DependencyNotInstalled("{}. (HINT: see matplotlib documentation for installation https://matplotlib.org/faq/installing_faq.html#installation".format(e))

class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, grid_size=[15,15], unit_size=10, unit_gap=1, snake_size=3, n_snakes=1, n_foods=1, random_init=True):
        fps = 3000
        self.game = SnakeGame(fps)
        pygame.font.init()        

    def step(self, action):
        self.game.clock.tick(self.game.fps)
        
        self.game.move_snake()
        self.game.check_collisions()

        if self.game.restart == True:
            self.game.restart = False
            # continue FIXME: this was within a loop originally
        
        self.game.redraw_window()
        self.game.event_handler()  # TODO: maybe remove this since we aren't handling events?        
        return self.last_obs, rewards, done, info  # TODO: fill this in

    def reset(self):
        # self.controller = Controller(self.grid_size, self.unit_size, self.unit_gap, self.snake_size, self.n_snakes, self.n_foods, random_init=self.random_init)
        #  self.last_obs = self.controller.grid.grid.copy()
        # return self.last_obs
        return None

    def render(self, mode='human', close=False, frame_speed=.1):
        if self.viewer is None:
            self.fig = plt.figure()
            self.viewer = self.fig.add_subplot(111)
            plt.ion()
            self.fig.show()
        else:
            self.viewer.clear()
            self.viewer.imshow(self.last_obs)
            plt.pause(frame_speed)
        self.fig.canvas.draw()

    def seed(self, x):
        pass
