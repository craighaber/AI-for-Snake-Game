from enum import Enum


# https://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
class Directions(Enum):
    UP = "Directions.UP",
    DOWN = "Directions.DOWN",
    LEFT = "Directions.LEFT",
    RIGHT = "Directions.RIGHT",
    NONE = "Directions.NONE",
