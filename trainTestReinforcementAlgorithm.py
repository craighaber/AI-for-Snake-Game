# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import argparse
import time
from typing import Callable
import gym
import gym_snake
from stable_baselines3 import A2C
import numpy as np
from argparse import ArgumentParser
from datetime import datetime
import gym_snake.envs.snakeRewardFuncs as RewardFuncs


# %% [markdown]
# # Read This First
# This notebook is created to make it clear how we train and test the OpenAI Gym Snake. I used jupytext so that it can be run on the server as a python commandline script or as a jupyter notebook on your local machine. If you're not able to run the python file in a notebook, then you probably need to [install jupytext](https://jupytext.readthedocs.io/_/downloads/en/stable/pdf/):
# ```
# pip install jupytext
# # or
# conda install jupytext -c conda-forge 
# ```

# %% [markdown]
# ## Train

# %%
def trainRL(
    train_timesteps=1000, # Set amount of time for training. One step is one action for the snake.
    env_name='snake-v0', # Set gym environment name.
    board_height=10, # Set game board height.
    board_width=10, # Set game board width.
    max_moves_no_fruit=0, # Set number of allowed moves without fruit consumption before ending the game. Any non-poitive number corresponds to no limit.
    visualize_training=False, # We don't want to visualize the training process.
    visualization_fps=3000, # Default to a high value for training speed if training is visualized.
    reward_function=RewardFuncs.basic_reward_func # Set reward function to be used in training. Reward functions are defined in snakeRewardFuncs.py
):
    env = gym.make(
        env_name, 
        board_height=board_height,
        board_width=board_width,
        max_moves_no_fruit=max_moves_no_fruit,
        use_pygame=visualize_training,
        fps=visualization_fps, 
        reward_func=reward_function
    )  
    
    # Model is defined here. This is hard to parameterize so change this code to play with different models
    model = A2C('MlpPolicy', env, verbose=1)    
    
    t0 = time.time()
    model.learn(
        total_timesteps=train_timesteps  # Number of actions the model should take in learning
    )
    t1 = time.time()
    print("Finished training in " + str(round(t1-t0, 2)) + " seconds")
    
    return model


# %% [markdown]
# ## Test
# Test the model to see how well it is performing. Also have the option to visualize the result

# %%
def testRL(
    model,
    test_timesteps=100, # Set amount of time for testing. One step is one action for the snake.
    env_name='snake-v0', # Set gym environment name.
    board_height=10, # Set game board height.
    board_width=10, # Set game board width.
    max_moves_no_fruit=0, # Set number of allowed moves without fruit consumption before ending the game. Any non-poitive number corresponds to no limit.
    visualize_testing=True, # Set to true in order to see game moves in pygame. Should be false if run on server.
    visualization_fps=30, # Set frames per second of testing visualization.
    reward_function=RewardFuncs.basic_reward_func # Set reward function to be used in training. Reward functions are defined in snakeRewardFuncs.py
):
    # Setup
    env = gym.make(
        env_name, 
        board_height=board_height,
        board_width=board_width, 
        max_moves_no_fruit=max_moves_no_fruit,
        use_pygame=visualize_testing,
        fps=visualization_fps, 
        reward_func=reward_function
    )
    obs = env.reset()
    
    # Run
    scores = []
    for i in range(test_timesteps):
        action, _state = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        if done:
            scores.append(env.game.score)
            obs = env.reset()

    return scores


# %% [markdown]
# ## Analyze

# %%
def analyzeRL(
    scores,  # array of scores for each completed game
):
    s_arr = np.array(scores)
    print("Number of completed games: ", len(s_arr))

    if len(s_arr) > 0:
        print("High Score over all games: ", np.max(s_arr))
        print("Mean Score over all games: ", np.average(s_arr))
        print("Median Score over all games: ", np.median(s_arr))    


# %% [markdown]
# ## Save

# %%
def saveRL(
    model, 
    model_filename=""  # Filename to save model under. If empty, defaults to naming using datetime
):
    
    if len(model_filename) == 0:
        model_filename = "saved_models/"+str(datetime.now().strftime("[%Y-%m-%d %H:%M:%S%z]"))
    
    model.save(model_filename)  


# %% [markdown]
# ## Run in Notebook
# To run in the notebook, uncomment the following three lines:

# %%
# model = trainRL()
# scores = testRL(model)
# analyzeRL(scores)
# saveRL(model)

# %% [markdown]
# ## Run on commandline
# Note that it is expected that this does not work in the notebook

# %%
def main():
    # Get arguments
    aparser = ArgumentParser("Snnake Reinforcement Learning")
    aparser.add_argument("--env_name", type=str, default="snake-v0")

    aparser.add_argument("--train_timesteps", type=int, default=1000)
    aparser.add_argument("--test_timesteps", type=int, default=100)

    aparser.add_argument("--board_height", type=int, default=10)
    aparser.add_argument("--board_width", type=int, default=10)
    aparser.add_argument("--max_moves_no_fruit", type=int, default=0)
    aparser.add_argument("--visualize_training", type=bool, default=False)
    aparser.add_argument("--visualize_testing", type=bool, default=True)
    aparser.add_argument("--visualization_fps", type=int, default=30)

    # FIXME currently we are not able to pass an argument for selecting the reward function as a command line arg. 
    # We should figure this out, but until then, change the reward function on line 181.
    # aparser.add_argument("--reward_function", type=Callable[..., float], default=RewardFuncs.basic_reward_func, help="function to determine how a snake agent is rewarded/punished for certain actions during training. Available functions can be found in snakeRewardFuncs.py")
    
    aparser.add_argument("--print_analysis", type=bool, default=True, help="bool to determine whether or not analysis of test scores is done")    
    
    aparser.add_argument("--save_model", type=bool, default=False, help="bool to determine whether or not to save the trained model")        
    aparser.add_argument("--model_filename", type=str, default="", help="filename for model if it is saved. Should probably start with 'saved_models/' directory")        
    
    args = aparser.parse_args()

    reward_function = RewardFuncs.basic_reward_func
    
    # Training
    model = trainRL(
        args.train_timesteps, 
        args.env_name,
        args.board_height,
        args.board_width,
        args.max_moves_no_fruit,
        args.visualize_training,
        args.visualization_fps,
        reward_function
    )
    
    # Testing
    scores = testRL(
        model, 
        args.test_timesteps, 
        args.env_name,
        args.board_height,
        args.board_width,
        args.max_moves_no_fruit,
        args.visualize_testing,
        args.visualization_fps,
        reward_function)
    
    # Analysis
    if args.print_analysis:
        analyzeRL(scores)
        
    # Save
    if args.save_model:
        saveRL(model, args.model_filename)


# %%
if __name__ == "__main__":
    main()
