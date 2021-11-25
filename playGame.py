import time

import keyboard  # using module keyboard
import pygame

from game.Board import Directions
from game.GUI import GUI
from game.SnakeGame import SnakeGame


# Uses keyboard (python module) to directly query for key presses, without relying on the console inputs.
def play_game():
    game = SnakeGame()
    view = GUI()
    pygame.font.init()
    view.redraw_window(game)

    sleep_time = 0.2

    # Reference:
    # https://stackoverflow.com/questions/24072790/how-to-detect-key-presses
    while not game.is_game_over():  # making a loop
        if keyboard.is_pressed('w'):  # if key 'q' is pressed
            game.move_snake(Directions.UP)
            time.sleep(sleep_time)
        if keyboard.is_pressed('s'):
            game.move_snake(Directions.DOWN)
            time.sleep(sleep_time)
        if keyboard.is_pressed('a'):
            game.move_snake(Directions.LEFT)
            time.sleep(sleep_time)
        if keyboard.is_pressed('d'):
            game.move_snake(Directions.RIGHT)
            time.sleep(sleep_time)

        game.check_collisions()
        view.redraw_window(game)
        view.event_handler()

    print(f'Game Over. You Scored: {game.get_score()}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    play_game()
