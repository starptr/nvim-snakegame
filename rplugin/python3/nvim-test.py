import pynvim
import time
from threading import Thread
#import gameboard as Board
#import snake as Snake
from gameboard import Board
from snake import Snake
import os
cwd = os.getcwd()

@pynvim.plugin
class TestPlugin(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self.board = Board(20, 20)
        self.snake = Snake(self.board.height // 2, self.board.width // 2)
        self.step_time = 100
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

    @pynvim.command('TestSnake', nargs='*', range='')
    def testcommand(self, args, _):
        self.nvim.out_write(cwd + '\n')
        # Initialize
        self.nvim.command("silent edit `='vim-game-snake'`")
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

    def update_board(self):
        valid_step, old_tail = self.snake.step(False)
        if valid_step:
            self.board.add(Board.snake_box, self.snake.body[-1][0], self.snake.body[-1][1])
            if old_tail:
                self.board.add(Board.no_box, old_tail[0], old_tail[1])
        else:
            self.is_gameover = True

    def draw_game(self):
        self.nvim.call("setline", 2, self.board)
        self.nvim.command("redraw")

    #@pynvim.autocmd('BufEnter', pattern='*.py', eval='expand("<afile>")', sync=True)
    #def on_bufenter(self, filename):
    #    self.nvim.out_write('testplugin is in ' + filename + '\n')
