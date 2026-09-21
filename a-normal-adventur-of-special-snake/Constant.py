#环境配置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

#颜色定义
BLACK = (0, 0, 0)

WHITE = (255, 255, 255)

GREEN = (0, 255, 0)

DARK_GREEN = (0, 200, 0)
#绿色和深绿用于蛇图形

RED = (255, 0, 0)
#食物颜色

GRAY = (40, 40, 40)

#障碍物颜色
BLUE = (0, 0, 255)

#游戏首页颜色
PURPLE = (128, 0, 128)
#方向
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

#生成障碍物的数量
OBSTACLE_COUNT_LOW = 10
OBSTACLE_COUNT_HIGH = 30 #默认为简单模式

#食物被吃掉后急剧缩小消失的动画帧数（游戏逻辑每秒10帧，6帧约0.6秒）
FOOD_ANIM_FRAMES = 6

#根据游戏难度提供不同的游戏参数——障碍物的生成数量，贪吃蛇的移动速度
Easy_mode = {
    'OBSTACLE_COUNT_LOW':10,

    'OBSTACLE_COUNT_HIGH':30,
}

Normal_mode = {
    'OBSTACLE_COUNT_LOW':40,
    
    'OBSTACLE_COUNT_HIGH':60,
}

Hard_mode = {
    'OBSTACLE_COUNT_LOW':80,
    
    'OBSTACLE_COUNT_HIGH':100,
}

