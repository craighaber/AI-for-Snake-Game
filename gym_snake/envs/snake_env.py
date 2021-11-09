import gym
import pygame
from typing import Union
from typing import Callable
from gym import spaces
from numpy import ndarray
from gym_snake.envs.snakeGameGym import *
from gym_snake.envs.snakeRewardFuncs import basic_reward_func


class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, 
        use_pygame: bool = True, 
        reward_func: Callable[..., float] = basic_reward_func):
        """
        Function that initializes the snake environment.

        use_pygame: a boolean flage representing whether or not to render the game with pygame
        reward_func: a function that takes any inputs (representing important game states) and returns an 
                     int output representing a reward for the snake agent based on the inputs. 
                     Defaults to snakeRewardFunc.basic_reward_func()
        """
        fps = 3000
        self.viewer = None

        if use_pygame:
            pygame.font.init()
        self.game = SnakeGameGym(fps, use_pygame=use_pygame)

        self.reward_func = reward_func
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=3, shape=(self.game.cols, self.game.rows), dtype=int)
           


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

        # check collisions after move
        did_consume_fruit = self.game.check_fruit_collision()
        did_collide_wall = self.game.check_wall_collision()
        did_collide_body = self.game.check_body_collision()

        # Get observation after move
        observation = self.game.get_board()

        # Get rewards based on collision status
        reward_dict = {
            "did_consume_fruit":did_consume_fruit,
            "did_collide_wall": did_collide_wall,
            "did_collide_body": did_collide_body,
        }
        rewards = self.reward_func(reward_dict)

        # Game is over if wall collision or body collision occurred. TODO: add end done for time limit
        done = did_collide_wall or did_collide_body

        # FIXME: Figure out what to do with info. stable_baseline3 seems to require episode object
        info = {"episode": None}  

        # If there was a fruit collision during last frame, move the fruit.
        if did_consume_fruit:
            self.game.respond_to_fruit_consumption()
        
        if self.game.use_pygame:
            self.game.clock.tick(self.game.fps)
            self.game.redraw_window()

        return observation, rewards, done, info

    def reset(self) -> ndarray:
        """
        Function that collects the game board observation, ends the game,
        and returns the observation.
        """
        observation = self.game.get_board()
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
        observation = self.game.get_board()

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
