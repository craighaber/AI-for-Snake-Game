"""
This file is used to store reward functions to be used in snake_env.py
"""

def basic_reward_func(reward_dict) -> float:
    """
    Basic reward function that rewards the snake for consuming a fruit, 
    punishes it for colliding with itself or a wall, and rewards nothing otherwise.

    reward_dict:
        did_consume_fruit: boolean representing whether a snake consumed a fruit in the last move
        did_collide_wall: boolean representing whether a snake collided with itself in the last move
        did_collide_body: boolean representing whether a snake collided with a wall in the last move

    output: 
        an integer representing a reward assigned to the snake agent based on the inputs provided
    """
    if reward_dict["did_consume_fruit"]:
        return 1
    elif reward_dict["did_collide_wall"] or reward_dict["did_collide_body"]:
        return -1
    else: 
        return 0

def reward_closer_to_fruit(reward_dict) -> float:
    if reward_dict["did_consume_fruit"]:
        return 10**10
    elif reward_dict["did_move_closer_to_fruit"]:
        return 1
    elif reward_dict["did_collide_wall"] or reward_dict["did_collide_body"]:
        return -1
    else: 
        return 0
