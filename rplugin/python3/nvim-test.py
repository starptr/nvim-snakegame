import pynvim
import random
import time
from threading import Thread
#import gameboard as Board
#import snake as Snake
#from gameboard import Board
#from snake import Snake
import os
cwd = os.getcwd()

@pynvim.plugin
class SnakeGame(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self.board = Board(20, 20)
        self.snake = Snake(self.board.height, self.board.width)
        self.step_time = 50
        self.is_gameover = False

    @pynvim.function('SnakeMovement', sync=True)
    def movement(self, args):
        bp = args[0]
        if self.snake.direction == "left" or self.snake.direction == "right":
            if bp == "k":
                self.snake.direction = "up"
            elif bp == "j":
                self.snake.direction = "down"
        else:
            if bp == "l":
                self.snake.direction = "right"
            elif bp == "h":
                self.snake.direction = "left"

    @pynvim.command('SnakeGame', nargs='*', range='')
    def testcommand(self, args, _):
        self.nvim.out_write(cwd + '\n')
        # Initialize
        self.nvim.command("silent edit `='SnakeGame'`")
        self.nvim.command("setlocal nonumber")
        self.nvim.command("setlocal norelativenumber")
        self.nvim.command("setlocal nowrap")
        self.nvim.command("setlocal noswapfile")
        self.nvim.command("setlocal nocursorline")
        self.nvim.command("setlocal nocursorcolumn")
        self.nvim.command("setlocal nolist")
        self.nvim.command("setlocal buftype=nofile")
        self.nvim.command("setlocal bufhidden=hide")

        self.nvim.command("nnoremap l :call SnakeMovement('l')<CR>")
        self.nvim.command("nnoremap k :call SnakeMovement('k')<CR>")
        self.nvim.command("nnoremap j :call SnakeMovement('j')<CR>")
        self.nvim.command("nnoremap h :call SnakeMovement('h')<CR>")
        self.draw_game()

        Thread(target=self.game_loop).start()

    def game_loop(self):
        last_step = 0
        clock = 0
        while not self.is_gameover:
            self.nvim.async_call(self.draw_game)
            if clock - last_step >= self.step_time:
                last_step = clock
                self.nvim.async_call(self.update_board)
            time.sleep(0.01)
            clock += 1 # Centiseconds

        self.board.gameover(len(self.snake.body))
        self.nvim.async_call(self.draw_game)

    def update_board(self):
        valid_step, old_tail = self.snake.step(self.board.fruit)
        if valid_step:
            self.board.add(Board.snake_box, self.snake.body[-1][0], self.snake.body[-1][1])
            if old_tail:
                self.board.add(Board.no_box, old_tail[0], old_tail[1])
            else: # Fruit was eaten
                while True:
                    self.board.fruit = (random.randint(0, self.board.height - 1), random.randint(0, self.board.width - 1))
                    if not self.board.fruit in self.snake.body:
                        break
                self.board.add(Board.fruit_box, self.board.fruit[0], self.board.fruit[1])
                self.step_time *= 0.9
        else:
            self.is_gameover = True

    def draw_game(self):
        self.nvim.call("setline", 2, self.board.board_ds)
        self.nvim.command("redraw")

class Board(object):
    # Box types
    no_box = "."
    snake_box = "X"
    fruit_box = "O"

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.fruit = (height // 4, width // 4)
        self.board_ds = ["." * width for _ in range(height)]
        self.add(Board.fruit_box, self.fruit[0], self.fruit[1])

    def add(self, box_type, y, x):
        row = self.board_ds[y]
        self.board_ds[y] = row[:x] + box_type + row[(x + 1):]

    def gameover(self, score):
        self.board_ds.append("Game over :( Your score is: " + str(score))

class Snake(object):
    directions = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1),
    }

    def __init__(self, height, width):
        self.board_height = height
        self.board_width = width
        self.body = [(height // 2, width // 2)]
        self.direction = "left"

    def step(self, fruit):
        head = self.body[-1]
        new_head = (head[0] + Snake.directions[self.direction][0], head[1] + Snake.directions[self.direction][1])
        if new_head in self.body or new_head[0] < 0 or new_head[0] >= self.board_height or new_head[1] < 0 or new_head[1] >= self.board_width:
            return (False, None)
        else:
            self.body.append(new_head)
            if fruit == new_head:
                return (True, None)
            else:
                return (True, self.body.pop(0))
