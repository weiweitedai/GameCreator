import pygame
import Constant as c
import Snake
import Food
import sys
import Obstacle
import random
#初始化Pygame
pygame.init()

  
def load_font(size,bold=False):
    path = "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf" 
    try:

        return pygame.font.Font(path, size)

    except (FileNotFoundError, pygame.error):

        return pygame.font.Font(None, size)
#游戏类
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((c.WINDOW_WIDTH, c.WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = load_font(24)
        self.big_font = load_font(48)
        self.reset()

    def reset(self):
        self.snake = Snake.Snake()
        self.food = Food.Food()
        self.obstacles = [Obstacle.Obstacle() for _ in range(random.randint(c.OBSTACLE_COUNT_LOW, c.OBSTACLE_COUNT_HIGH))]
        print(f"当前障碍物范围: {c.OBSTACLE_COUNT_LOW} ~ {c.OBSTACLE_COUNT_HIGH}, 本次生成: {len(self.obstacles)} 个") #验证属性值是否被模式选择修改，调试完可删除
        self.score = 0
        self.game_over = False
        self.food_anim = None #吞食动画剩余帧数，None表示没有动画

        while True:
                occupied_positions = set(self.snake.body + [self.food.position] + [obs.position for obs in self.obstacles])
                if len(occupied_positions) == len(self.snake.body) + 1 + len(self.obstacles):
                    break
                self.food.randomize_position()
                for obs in self.obstacles:
                    obs.randomize_position()
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() #这段必须书写，是每个Pygame程序想要正常退出所必须的，关闭窗口需要操作系统发出请求，再由程序决定是否要响应，若没有则可能触发系统强制杀程序，留下僵尸进程，窗口无响应但程序继续跑这几种情况
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_SPACE:
                        self.reset()
                else:        
                    if event.key == pygame.K_UP:
                            self.snake.change_direction(c.UP)
                    elif event.key == pygame.K_DOWN:
                            self.snake.change_direction(c.DOWN)
                    elif event.key == pygame.K_LEFT:
                            self.snake.change_direction(c.LEFT)
                    elif event.key == pygame.K_RIGHT:
                            self.snake.change_direction(c.RIGHT)

    def update(self):
        if self.game_over:
             return

        if not self.snake.move():
             self.game_over = True
             return

        if self.snake.head in [obs.position for obs in self.obstacles]:
             self.game_over = True
             return

        #吞食动画进行中：只推进动画，不判吃也不生成新食物
        #（此时食物还停在旧格子上、蛇头也还压在上面，不跳过的话会被反复判吃）
        if self.food_anim is not None:
             self.food_anim -= 1
             if self.food_anim == 0:
                  self.food_anim = None
                  self.food.randomize_position()
                  while self.food.position in self.snake.body or self.food.position in [obs.position for obs in self.obstacles]:
                       self.food.randomize_position()
             return

        if self.food.position == self.snake.head:
             self.snake.grow()
             self.score += 10
             self.food_anim = c.FOOD_ANIM_FRAMES

    
    #游戏界面的绘制渲染
    def draw_grid(self):
         for x in range(0,c.WINDOW_WIDTH,c.GRID_SIZE):
              pygame.draw.line(self.screen,c.WHITE,(x,0),(x,c.WINDOW_HEIGHT))
         for y in range(0,c.WINDOW_HEIGHT,c.GRID_SIZE):
              pygame.draw.line(self.screen,c.WHITE,(0,y),(c.WINDOW_WIDTH,y))

    def draw(self,t=0):
        #窗口图架绘制
        self.screen.fill(c.BLACK)
        self.draw_grid()


        #绘制食物（被吃掉后急剧缩小直至消失：t是插值进度，让缩小过程和蛇身移动一样平滑）
        if self.food_anim is None:
             size = c.GRID_SIZE - 4
        else:
             size = max(1, int((c.GRID_SIZE - 4) * (self.food_anim - t) / c.FOOD_ANIM_FRAMES))
        offset = (c.GRID_SIZE - size) // 2 #向格子中心收缩
        food_rect = pygame.Rect(self.food.position[0] * c.GRID_SIZE + offset,self.food.position[1] * c.GRID_SIZE + offset,size,size)
        pygame.draw.rect(self.screen, c.RED, food_rect, border_radius=max(1, size * 3 // 8))


        #绘制蛇
        for i,body_node in enumerate(self.snake.body):
                prev = self.snake.prev_body[i] if self.snake.prev_body and i < len(self.snake.prev_body) else body_node
                dx = body_node[0] - prev[0]
                dy = body_node[1] - prev[1]
                if dx > 1:
                     dx -= c.GRID_WIDTH
                elif dx < -1:
                     dx += c.GRID_WIDTH
                if dy > 1:
                     dy -= c.GRID_HEIGHT
                elif dy < -1:
                     dy += c.GRID_HEIGHT
                px = ( prev[0] + dx * t ) * c.GRID_SIZE
                py = ( prev[1] + dy * t ) * c.GRID_SIZE
                body_rect = pygame.Rect(
                    px + 1,
                    py + 1,
                    c.GRID_SIZE - 2,
                    c.GRID_SIZE - 2)
                color = c.GREEN if i != 0 else c.DARK_GREEN

                pygame.draw.rect(self.screen,color,body_rect,border_radius=5)
                #绘制蛇的眼睛
                if i == 0:

                                    
                     cx = px + c.GRID_SIZE // 2
                     cy = py + c.GRID_SIZE // 2 
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
                             

                     pygame.draw.circle(self.screen,c.RED,eye1,eye_radius)
                     pygame.draw.circle(self.screen,c.RED,eye2,eye_radius) 
        #绘制分数

        score_text = self.font.render(f"Score: {self.score}", True, c.WHITE)

        self.screen.blit(score_text, (10, 10)) 

        #绘制障碍物
        for obs in self.obstacles:
             obs_rect = pygame.Rect(obs.position[0] * c.GRID_SIZE, obs.position[1] * c.GRID_SIZE, c.GRID_SIZE , c.GRID_SIZE)
             pygame.draw.rect(self.screen, c.BLUE, obs_rect, border_radius=4)    
        #绘制游戏结束界面
        if self.game_over:
             overlad = pygame.Surface((c.WINDOW_WIDTH,c.WINDOW_HEIGHT))
             overlad.set_alpha(200)
             overlad.fill(c.BLACK)
             self.screen.blit(overlad,(0,0))

             game_over_text = self.big_font.render("GAME OVER",True,c.RED)
             text_rect = game_over_text.get_rect(center=(
                  c.WINDOW_WIDTH // 2, c.WINDOW_HEIGHT // 2 - 40
             ))
             self.screen.blit(game_over_text,text_rect)

             score_text = self.font.render(f"Final score:{self.score}",True,c.WHITE)
             score_rect = score_text.get_rect(center=
                (c.WINDOW_WIDTH // 2, c.WINDOW_HEIGHT // 2 + 20))
             self.screen.blit(score_text,score_rect)

             tip_text = self.font.render("Press SPACE to Restart, ESC to Quit",True,c.WHITE)
             tip_rect = tip_text.get_rect(center=
                (c.WINDOW_WIDTH // 2, c.WINDOW_HEIGHT // 2 + 60))
             self.screen.blit(tip_text,tip_rect)   

        pygame.display.flip()

                  
              

    #游戏运行
    def run(self):
        frame = 0
        while True:
            self.handle_events()
            if frame % 6 == 0:
                self.update()
            self.draw((frame % 6) / 6)
            self.clock.tick(60)
            frame += 1  
        
