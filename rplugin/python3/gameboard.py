class Board(object):
    # Box types
    no_box = "."
    snake_box = "X"
    fruit_box = "O"

    def __init__(self, height, width):
        self.board = ["." * width for _ in range(height)]
        self.height = height
        self.width = width

    def add(self, box_type, y, x):
        row = self.board[y]
        self.board[y] = row[:x] + box_type + row[(x + 1):]

