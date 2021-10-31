from gym.envs.registration import register

#Registers the 'snake-v0' OpenAI Gym env to the SnakeEnv class
register(
    id='snake-v0',
    entry_point='gym_snake.envs:SnakeEnv',
)
