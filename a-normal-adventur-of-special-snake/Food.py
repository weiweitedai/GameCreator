import random
import Constant as c

#食物类
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, c.GRID_WIDTH - 1), random.randint(0, c.GRID_HEIGHT - 1))