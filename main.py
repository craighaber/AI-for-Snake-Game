from game.SnakeGame import SnakeGame
from game.board import Directions


def main():
    game = SnakeGame()
    while not game.is_game_over():
        print(game.get_board())
        print(f'Score: {game.get_score()}')
        print(game.snake.directions)
        token = input("Move: ")
        match token:
            case "w":
                game.move_snake(Directions.UP)
            case "s":
                game.move_snake(Directions.DOWN)
            case "a":
                game.move_snake(Directions.LEFT)
            case "d":
                game.move_snake(Directions.RIGHT)
            case _:
                print("Invalid token use WSAD")

        game.check_collisions()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
