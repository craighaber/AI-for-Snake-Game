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
        return 1.0
    elif reward_dict["did_collide_wall"] or reward_dict["did_collide_body"]:
        return -1.0
    else: 
        return 0.0

def reward_2x_for_fruit(reward_dict) -> float:
    """
    Same as basic reward function except reward for fruit is twice as high.

    reward_dict:
        did_consume_fruit: boolean representing whether a snake consumed a fruit in the last move
        did_collide_wall: boolean representing whether a snake collided with itself in the last move
        did_collide_body: boolean representing whether a snake collided with a wall in the last move

    output: 
        an integer representing a reward assigned to the snake agent based on the inputs provided
    """
    if reward_dict["did_consume_fruit"]:
        return 2.0
    elif reward_dict["did_collide_wall"] or reward_dict["did_collide_body"]:
        return -1.0
    else: 
        return 0.0

def reward_10x_for_fruit(reward_dict) -> float:
    """
    Same as basic reward function except reward for fruit is 10x as high.

    reward_dict:
        did_consume_fruit: boolean representing whether a snake consumed a fruit in the last move
        did_collide_wall: boolean representing whether a snake collided with itself in the last move
        did_collide_body: boolean representing whether a snake collided with a wall in the last move

    output: 
        an integer representing a reward assigned to the snake agent based on the inputs provided
    """
    if reward_dict["did_consume_fruit"]:
        return 10.0
    elif reward_dict["did_collide_wall"] or reward_dict["did_collide_body"]:
        return -1.0
    else: 
        return 0.0

def punish_equally_for_inactivity(reward_dict) -> float:
    """
    Similar to basic reward function except punishes -1 for not doing anything.

    reward_dict:
        did_consume_fruit: boolean representing whether a snake consumed a fruit in the last move
        did_collide_wall: boolean representing whether a snake collided with itself in the last move
        did_collide_body: boolean representing whether a snake collided with a wall in the last move

    output: 
        an integer representing a reward assigned to the snake agent based on the inputs provided
    """
    if reward_dict["did_consume_fruit"]:
        return 1.0
    elif reward_dict["did_collide_wall"] or reward_dict["did_collide_body"]:
        return -1.0
    else: 
        return -1.0

def punish_half_for_inactivity(reward_dict) -> float:
    """
    Similar to basic reward function except punishes -0.5 for not doing anything.


    reward_dict:
        did_consume_fruit: boolean representing whether a snake consumed a fruit in the last move
        did_collide_wall: boolean representing whether a snake collided with itself in the last move
        did_collide_body: boolean representing whether a snake collided with a wall in the last move

    output: 
        an integer representing a reward assigned to the snake agent based on the inputs provided
    """
    if reward_dict["did_consume_fruit"]:
        return 1.0
    elif reward_dict["did_collide_wall"] or reward_dict["did_collide_body"]:
        return -1.0
    else: 
        return -0.5

def punish_tenth_for_inactivity(reward_dict) -> float:
    """
    Similar to basic reward function except punishes -0.1 for not doing anything.


    reward_dict:
        did_consume_fruit: boolean representing whether a snake consumed a fruit in the last move
        did_collide_wall: boolean representing whether a snake collided with itself in the last move
        did_collide_body: boolean representing whether a snake collided with a wall in the last move

    output: 
        an integer representing a reward assigned to the snake agent based on the inputs provided
    """
    if reward_dict["did_consume_fruit"]:
        return 1.0
    elif reward_dict["did_collide_wall"] or reward_dict["did_collide_body"]:
        return -1.0
    else: 
        return -0.1

def basic_reward_func_with_move_ceiling(reward_dict) -> float:
    """
    Basic reward function that rewards the snake for consuming a fruit, 
    punishes it for colliding with itself or a wall, punishes it for running
    out of moves after not consuming a fruit, and rewards nothing otherwise.

    reward_dict:
        did_consume_fruit: boolean representing whether a snake consumed a fruit in the last move
        did_collide_wall: boolean representing whether a snake collided with itself in the last move
        did_collide_body: boolean representing whether a snake collided with a wall in the last move
        did_exceed_max_moves_no_fruit: boolean representing whether a snake has exceeded the number of allowable 
                                           moves without consuming a fruit

    output: 
        a float representing a reward assigned to the snake agent based on the inputs provided
    """
    if reward_dict["did_consume_fruit"]:
        return 1.0
    elif reward_dict["did_collide_wall"] or reward_dict["did_collide_body"]:
        return -1.0
    elif reward_dict["did_exceed_max_moves_no_fruit"]:
        return -1.0
    else: 
        return 0.0

def punish_half_for_move_ceiling(reward_dict) -> float:
    """
    Similar to basic reward function w/move ceiling except punishes -0.5 for not crossing the move ceiling.

    Basic reward function that rewards the snake for consuming a fruit, 
    punishes it for colliding with itself or a wall, punishes it for running
    out of moves after not consuming a fruit, and rewards nothing otherwise.

    reward_dict:
        did_consume_fruit: boolean representing whether a snake consumed a fruit in the last move
        did_collide_wall: boolean representing whether a snake collided with itself in the last move
        did_collide_body: boolean representing whether a snake collided with a wall in the last move
        did_exceed_max_moves_no_fruit: boolean representing whether a snake has exceeded the number of allowable 
                                           moves without consuming a fruit

    output: 
        a float representing a reward assigned to the snake agent based on the inputs provided
    """
    if reward_dict["did_consume_fruit"]:
        return 1.0
    elif reward_dict["did_collide_wall"] or reward_dict["did_collide_body"]:
        return -1.0
    elif reward_dict["did_exceed_max_moves_no_fruit"]:
        return -0.5
    else: 
        return 0.0

def punish_tenth_for_move_ceiling(reward_dict) -> float:
    """
    Similar to basic reward function w/move ceiling except punishes -0.1 for not crossing the move ceiling.

    Basic reward function that rewards the snake for consuming a fruit, 
    punishes it for colliding with itself or a wall, punishes it for running
    out of moves after not consuming a fruit, and rewards nothing otherwise.

    reward_dict:
        did_consume_fruit: boolean representing whether a snake consumed a fruit in the last move
        did_collide_wall: boolean representing whether a snake collided with itself in the last move
        did_collide_body: boolean representing whether a snake collided with a wall in the last move
        did_exceed_max_moves_no_fruit: boolean representing whether a snake has exceeded the number of allowable 
                                           moves without consuming a fruit

    output: 
        a float representing a reward assigned to the snake agent based on the inputs provided
    """
    if reward_dict["did_consume_fruit"]:
        return 1.0
    elif reward_dict["did_collide_wall"] or reward_dict["did_collide_body"]:
        return -1.0
    elif reward_dict["did_exceed_max_moves_no_fruit"]:
        return -0.1
    else: 
        return 0.0
    
def reward_closer_to_fruit(reward_dict) -> float:
    """
    Reward function that rewards the snake for consuming a fruit and getting closer to fruit,
    punishes it for colliding with itself or a wall, and rewards nothing otherwise.

    reward_dict:
        did_consume_fruit: boolean representing whether a snake consumed a fruit in the last move
        did_move_closer_to_fruit: boolean representing whether a snake moved closer to the fruit
        did_collide_wall: boolean representing whether a snake collided with itself in the last move
        did_collide_body: boolean representing whether a snake collided with a wall in the last move

    output: 
        an integer representing a reward assigned to the snake agent based on the inputs provided
    """
    if reward_dict["did_consume_fruit"]:
        return 1.0
    elif reward_dict["did_move_closer_to_fruit"]:
        return 1.0
    elif reward_dict["did_collide_wall"] or reward_dict["did_collide_body"]:
        return -1.0
    else: 
        return 0.0

def reward_2x_closer_to_fruit(reward_dict) -> float:
    """
    Similar to basic reward closer to fruit except rewards 2 for not crossing the move ceiling.

    Reward function that rewards the snake for consuming a fruit and getting closer to fruit,
    punishes it for colliding with itself or a wall, and rewards nothing otherwise.

    reward_dict:
        did_consume_fruit: boolean representing whether a snake consumed a fruit in the last move
        did_move_closer_to_fruit: boolean representing whether a snake moved closer to the fruit
        did_collide_wall: boolean representing whether a snake collided with itself in the last move
        did_collide_body: boolean representing whether a snake collided with a wall in the last move

    output: 
        an integer representing a reward assigned to the snake agent based on the inputs provided
    """
    if reward_dict["did_consume_fruit"]:
        return 1.0
    elif reward_dict["did_move_closer_to_fruit"]:
        return 2.0
    elif reward_dict["did_collide_wall"] or reward_dict["did_collide_body"]:
        return -1.0
    else: 
        return 0.0

def reward_10x_closer_to_fruit(reward_dict) -> float:
    """
    Similar to basic reward closer to fruit except rewards 10 for not crossing the move ceiling.

    Reward function that rewards the snake for consuming a fruit and getting closer to fruit,
    punishes it for colliding with itself or a wall, and rewards nothing otherwise.

    reward_dict:
        did_consume_fruit: boolean representing whether a snake consumed a fruit in the last move
        did_move_closer_to_fruit: boolean representing whether a snake moved closer to the fruit
        did_collide_wall: boolean representing whether a snake collided with itself in the last move
        did_collide_body: boolean representing whether a snake collided with a wall in the last move

    output: 
        an integer representing a reward assigned to the snake agent based on the inputs provided
    """
    if reward_dict["did_consume_fruit"]:
        return 1.0
    elif reward_dict["did_move_closer_to_fruit"]:
        return 10.0
    elif reward_dict["did_collide_wall"] or reward_dict["did_collide_body"]:
        return -1.0
    else: 
        return 0.0
