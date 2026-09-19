import pygame
import sys
import random

#初始化Pygame
pygame.init()

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

#方向
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


#蛇类
class Snake:
    def __init__(self):
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2  
        self.head = (start_x, start_y)
        self.body = [(start_x - i, start_y) for i in range(0, 3)]  # 初始身体长度为3
        self.direction = RIGHT
        #self.next_direction = RIGHT 使用单格缓冲会出现卡连招丢键的情况
        self.pending = [] #通过队列原理，控制长度最大为2保证连招存在，手感丝滑
        self.grow_flag = False

    def move(self):
        self.direction = self.pending.pop(0) if self.pending else self.direction
        old_head = self.head
        new_head = (old_head[0] + self.direction[0], old_head[1] + self.direction[1])

        #判断是否撞墙
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            return False  # 撞墙，游戏结束
        #判断是否撞到自己
        if self.grow_flag:
             body_to_check = self.body[1:]
        else:
             body_to_check = self.body[1:-1]
        if new_head in body_to_check:  # 排除头部
            return False  # 撞到自己，游戏结束

        #更新身体
        self.head = new_head
        self.body.insert(0, new_head)  #将新头部插入身体列表的开头
        if not self.grow_flag:
            self.body.pop()  #移除尾部
        else:
            self.grow_flag = False  #重置增长标志

        return True  # 移动成功

    def grow(self):
        self.grow_flag = True

    def change_direction(self, new_direction):
        last = self.pending[-1] if self.pending else self.direction

        if (new_direction[0] * -1, new_direction[1] * -1) != last and new_direction != last :  #防止180度转向
            if len(self.pending) < 2:
                 
                self.pending.append(new_direction)

#食物类
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

def load_font(size,bold=False):
    path = "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"
    try:

        return pygame.font.Font(path, size)

    except (FileNotFoundError, pygame.error):

        return pygame.font.Font(None, size)
#游戏类
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        #
        self.font = load_font(24)
        self.big_font = load_font(48)
        self.reset()

    def reset(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False

        #确保食物不会生成在蛇身上
        while self.food.position in self.snake.body:
             self.food.randomize_position()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_SPACE:
                        self.reset()
                else:        
                    if event.key == pygame.K_UP:
                            self.snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                            self.snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                            self.snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                            self.snake.change_direction(RIGHT)

    def update(self):
        if self.game_over:
             return

        if not self.snake.move():
             self.game_over = True
             return

        if self.food.position == self.snake.head:
             self.snake.grow()
             self.score += 10
             self.food.randomize_position()
             while self.food.position in self.snake.body:
                  self.food.randomize_position()
             #return

    
    #游戏界面的绘制渲染
    def draw_grid(self):
         for x in range(0,WINDOW_WIDTH,GRID_SIZE):
              pygame.draw.line(self.screen,WHITE,(x,0),(x,WINDOW_HEIGHT))
         for y in range(0,WINDOW_HEIGHT,GRID_SIZE):
              pygame.draw.line(self.screen,WHITE,(0,y),(WINDOW_WIDTH,y))

    def draw(self):
        #窗口图架绘制
        self.screen.fill(BLACK)
        self.draw_grid()


        #绘制食物
        food_rect = pygame.Rect(self.food.position[0] * GRID_SIZE + 2,self.food.position[1] * GRID_SIZE + 2,GRID_SIZE - 4,GRID_SIZE - 4)
        pygame.draw.rect(self.screen, RED, food_rect, border_radius=6)


        #绘制蛇
        for i,body_node in enumerate(self.snake.body):
                body_rect = pygame.Rect(
                    body_node[0] * GRID_SIZE + 1,
                    body_node[1] * GRID_SIZE + 1,
                    GRID_SIZE - 2,
                    GRID_SIZE - 2)
                color = GREEN if i != 0 else DARK_GREEN

                pygame.draw.rect(self.screen,color,body_rect,border_radius=5)
                #绘制蛇的眼睛
                if i == 0:
                     x,y = body_node
                                    
                     cx = x * GRID_SIZE + GRID_SIZE // 2
                     cy = y * GRID_SIZE + GRID_SIZE // 2 
                     dx,dy = self.snake.direction
                                    
                     #考虑蛇的运动方向
                     offset = 4
                     eye_radius = 2
                                    
                     #左右方向
                     if dx:
                        eye1 = (cx + dx * offset,cy - 4)
                        eye2 = (cx + dx * offset,cy + 4)
                     else:
                        eye1 = (cx - 4, cy + dy * offset)
                        eye2 = (cx + 4, cy + dy * offset)                                    
                        dx,dy = self.snake.direction
                             

                     pygame.draw.circle(self.screen,RED,eye1,eye_radius)
                     pygame.draw.circle(self.screen,RED,eye2,eye_radius) 
        #绘制分数

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)

        self.screen.blit(score_text, (10, 10))     
        #绘制游戏结束界面
        if self.game_over:
             overlad = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT))
             overlad.set_alpha(200)
             overlad.fill(BLACK)
             self.screen.blit(overlad,(0,0))

             game_over_text = self.big_font.render("GAME OVER",True,RED)
             text_rect = game_over_text.get_rect(center=(
                  WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40
             ))
             self.screen.blit(game_over_text,text_rect)

             score_text = self.font.render(f"Final score:{self.score}",True,WHITE)
             score_rect = score_text.get_rect(center=
                (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
             self.screen.blit(score_text,score_rect)

             tip_text = self.font.render("Press SPACE to Restart, ESC to Quit",True,WHITE)
             tip_rect = tip_text.get_rect(center=
                (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
             self.screen.blit(tip_text,tip_rect)   

        pygame.display.flip()

                  
              

    #游戏运行
    def run(self):
        frame = 0
        while True:
            self.handle_events()
            if frame % 6 == 0:
                self.update()
            self.draw()
            self.clock.tick(60)
            frame += 1  
        


if __name__ == "__main__":
    game = Game()
    game.run()
    