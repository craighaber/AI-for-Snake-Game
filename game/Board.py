from enum import Enum
from game.Directions import Directions


class States(Enum):
    NONE = "States.NONE",
    SNAKE_BODY = "States.SNAKE_BODY",
    SNAKE_HEAD = "States.SNAKE_HEAD",
    FOOD = "States.FOOD",


class BoardState:
    def __init__(self, state: States, direction: Directions):
        self.state: States = state
        self.direction = direction

    def __str__(self):
        return self.state.name + " " + self.direction.name

    def __repr__(self):
        return "<BoardState: %s>" % self


class Board:
    def __init__(self, rows: int, cols: int):
        self.rows: int = rows
        self.cols: int = cols

        self.board = [[BoardState(States.NONE, Directions.NONE) for x in range(cols)] for y in range(rows)]

    def __str__(self):
        output = ""
        for row_index in range(self.rows):
            for col_index in range(self.cols):
                if self.board[row_index][col_index].state == States.FOOD:
                    output = output + " F "
                elif self.board[row_index][col_index].state == States.SNAKE_HEAD:
                    output = output + " O "
                elif self.board[row_index][col_index].state == States.SNAKE_BODY:
                    print(self.board[row_index][col_index].direction)
                    if self.board[row_index][col_index].direction == Directions.UP or self.board[row_index][
                        col_index].direction == Directions.DOWN:
                        output = output + " | "
                    else:
                        output = output + "---"
                else:
                    output = output + "   "
            output = output + "\n"
        return output

    def get_state_at(self, row: int, col: int):
        return self.board[row][col]

    def set_state_at(self, row: int, col: int, state: States, direction: Directions):
        self.board[row][col].state = state
        self.board[row][col].direction = direction
