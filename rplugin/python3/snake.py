class Snake(object):
    directions = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1),
    }

    def __init__(self, y, x):
        self.body = [(y, x)]
        self.direction = "left"

    def step(self, ate_fruit):
        head = self.body[-1]
        new_head = (head[0] + Snake.directions[self.direction][0], head[1] + Snake.directions[self.direction][1])
        if new_head in self.body:
            return (False, None)
        else:
            self.body.append(new_head)
            if ate_fruit:
                return (True, None)
            else:
                return (True, self.body.pop(0))
