# **************************************************************************************
# Adapted from the work of [Craig Haber](https://github.com/craighaber) with the
# original work available at https://github.com/craighaber/AI-for-Snake-Game
# *************************************************************************************
import pygame

from game.Board import Directions
from game.SnakeGame import SnakeGame


class GUI:
    def __init__(self):
        self.width = 750
        self.height = 750
        self.grid_start_y = 30
        self.win = pygame.display.set_mode((self.width, self.height))

    def redraw_window(self, game: SnakeGame):
        """Function to update the pygame window every frame, called from playSnakeGame.py."""

        self.win.fill(pygame.Color(10, 49, 245))
        self.draw_data_window(game)
        self.draw_grid(game)
        self.draw_grid_updates(game)
        pygame.display.update()

    def draw_data_window(self, game: SnakeGame):
        """Function to draw the segment of the pygame window with the score and high score."""

        pygame.draw.rect(self.win, pygame.Color(20, 20, 20), (0, 0, self.width, self.grid_start_y))

        # Add the score and high score
        font = pygame.font.SysFont('calibri', 20)
        score_text = font.render('Score: ' + str(game.get_score()), 1, (255, 255, 255))
        self.win.blit(score_text, (10, 5))

    def draw_grid(self, game: SnakeGame):
        """Function to draw the grid in the pygame window where the game is played."""

        space_col = self.width // game.cols
        space_row = (self.height - self.grid_start_y) // game.rows

        for i in range(game.rows):
            # draw horizontal line
            pygame.draw.line(self.win, pygame.Color(100, 100, 100), (0, space_row * i + self.grid_start_y),
                             (self.width, space_row * i + self.grid_start_y))

        for i in range(game.cols):
            # draw vertical line
            pygame.draw.line(self.win, pygame.Color(100, 100, 100), (space_col * i, self.grid_start_y),
                             (space_col * i, self.height))

        # draw last lines so they are not cut off
        pygame.draw.line(self.win, pygame.Color(100, 100, 100), (space_col * game.rows - 2, self.grid_start_y),
                         (space_col * game.rows - 2, self.height))
        pygame.draw.line(self.win, pygame.Color(100, 100, 100), (0, self.height - 2), (self.width, self.height - 2))

    def draw_grid_updates(self, game: SnakeGame):
        """Function called from redraw_window() to update the grid area of the window."""

        space_col = self.width // game.cols
        space_row = (self.height - self.grid_start_y) // game.rows

        # Draw the fruit
        fruit_y = game.fruit_pos.x_coord
        fruit_x = game.fruit_pos.y_coord
        pygame.draw.rect(self.win, pygame.Color(250, 30, 30), (
            space_col * fruit_x + 1, self.grid_start_y + space_row * fruit_y + 1, space_col - 1, space_row - 1))

        # Draw the updated snake since last movement
        for pos in game.snake.body:
            pos_y = pos.x_coord
            pos_x = pos.y_coord

            pygame.draw.rect(self.win, pygame.Color(31, 240, 12), (
                space_col * pos_x + 1, self.grid_start_y + space_row * pos_y + 1, space_col - 1, space_row - 1))

        head = game.snake.body[0]
        head_y = head.x_coord
        head_x = head.y_coord
        try:
            head_dir = game.snake.directions[0]
        except IndexError:
            head_dir = Directions.DOWN

        # Draw eyes on the head of the snake, determining which direction they should face

        # if head facing left
        if head_dir == Directions.LEFT:
            # draw left eye
            pygame.draw.circle(self.win, pygame.Color(100, 100, 100), (
                space_col * head_x + space_col // 10, self.grid_start_y + space_row * head_y + (space_row * 4) // 5), 2)
            # draw right eye
            pygame.draw.circle(self.win, pygame.Color(100, 100, 100), (
                space_col * head_x + space_col // 10, self.grid_start_y + space_row * head_y + space_row // 5), 2)
        # if head facing up
        elif head_dir == Directions.UP:
            # draw left eye
            pygame.draw.circle(self.win, pygame.Color(100, 100, 100), (
                space_col * head_x + space_col // 5, self.grid_start_y + space_row * head_y + space_row // 10), 2)
            # draw right eye
            pygame.draw.circle(self.win, pygame.Color(100, 100, 100), (
                space_col * head_x + (space_col * 4) // 5, self.grid_start_y + space_row * head_y + space_row // 10), 2)
        # if head facing right
        elif head_dir == Directions.RIGHT:
            # draw left eye
            pygame.draw.circle(self.win, pygame.Color(100, 100, 100), (
                space_col * head_x + (space_col * 9) // 10, self.grid_start_y + space_row * head_y + space_row // 5), 2)
            # draw right eye
            pygame.draw.circle(self.win, pygame.Color(100, 100, 100), (
                space_col * head_x + (space_col * 9) // 10,
                self.grid_start_y + space_row * head_y + (space_row * 4) // 5),
                               2)
        # if head is facing down
        else:
            # draw left eye
            pygame.draw.circle(self.win, pygame.Color(100, 100, 100), (
                space_col * head_x + space_col // 5, self.grid_start_y + space_row * head_y + (space_row * 9) // 10), 2)
            # draw right eye
            pygame.draw.circle(self.win, pygame.Color(100, 100, 100), (
                space_col * head_x + (space_col * 4) // 5,
                self.grid_start_y + space_row * head_y + (space_row * 9) // 10),
                               2)

    def event_handler(self):
        """Function for cleanly handling the event of the user quitting."""

        for event in pygame.event.get():
            # Check if user has quit the game
            if event.type == pygame.QUIT:
                self.run = False
                pygame.quit()
                quit()
