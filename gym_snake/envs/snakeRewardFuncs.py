"""
This file is used to store reward functions which we define that follow the basic pattern

inputs:
    did_consume_fruit: boolean representing whether a snake consumed a fruit in the last move
    did_collide_wall: boolean representing whether a snake collided with itself in the last move
    did_collide_body: boolean representing whether a snake collided with a wall in the last move

output: 
    an integer representing a reward assigned to the snake agent based on the inputs provided
"""

def basic_reward_func(
    did_consume_fruit: bool,
    did_collide_wall: bool,
    did_collide_body: bool) -> int:
    """
    Basic reward function that rewards the snake for consuming a fruit, 
    punishes it for colliding with itself or a wall, and rewards nothing otherwise.
    """
    if did_consume_fruit:
        return 1
    elif did_collide_wall or did_collide_body:
        return -1
    else: 
        return 0