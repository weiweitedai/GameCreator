import random
import Constant as c

num_low = c.OBSTACLE_COUNT_LOW
num_high = c.OBSTACLE_COUNT_HIGH

#障碍物类
class Obstacle:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, c.GRID_WIDTH - 1), random.randint(0, c.GRID_HEIGHT - 1))