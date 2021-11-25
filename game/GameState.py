from enum import Enum


# https://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
class GameState(Enum):
    OVER = "GameState.OVER",
    INPROGRESS = "GameState.INPROGRESS",