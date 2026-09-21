import pygame
import sys
import Game



#初始化pygame
pygame.init()

def draw(mode_page,Mode_text, Mode1_text, Mode2_text, Mode3_text):
    #界面绘制
        mode_page.fill(Game.c.GREEN)
        #文字渲染
        mode_page.blit(Mode_text, (Game.c.WINDOW_WIDTH // 2 - Mode_text.get_width() // 2, Game.c.WINDOW_HEIGHT // 2 - 150 - Mode_text.get_height() // 2))
    
        mode_page.blit(Mode1_text, (Game.c.WINDOW_WIDTH // 2 - Mode1_text.get_width() // 2, Game.c.WINDOW_HEIGHT // 2 - 50 - Mode1_text.get_height() // 2))
                
        mode_page.blit(Mode2_text, (Game.c.WINDOW_WIDTH // 2 - Mode2_text.get_width() // 2, Game.c.WINDOW_HEIGHT // 2 + 50 - Mode2_text.get_height() // 2))

        mode_page.blit(Mode3_text, (Game.c.WINDOW_WIDTH // 2 - Mode3_text.get_width() // 2, Game.c.WINDOW_HEIGHT // 2 + 150 - Mode3_text.get_height() // 2))
        
        pygame.display.flip()
    

def apply_mode(mode):
    #根据所选模式，修改Constant.py中的障碍物数量范围
    Game.c.OBSTACLE_COUNT_LOW = mode['OBSTACLE_COUNT_LOW']
    Game.c.OBSTACLE_COUNT_HIGH = mode['OBSTACLE_COUNT_HIGH']
    print(f"OBSTACLE_COUNT: {Game.c.OBSTACLE_COUNT_LOW} ~ {Game.c.OBSTACLE_COUNT_HIGH}")

def handle_events(rect_Mode1, rect_Mode2, rect_Mode3):
    #事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键点击
                mouse_pos = pygame.mouse.get_pos()
                mode = None
                if rect_Mode1.collidepoint(mouse_pos):
                    print("Easy Mode clicked!")
                    mode = Game.c.Easy_mode
                elif rect_Mode2.collidepoint(mouse_pos):
                    print("Normal Mode clicked!")
                    mode = Game.c.Normal_mode
                elif rect_Mode3.collidepoint(mouse_pos):
                    print("Hard Mode clicked!")
                    mode = Game.c.Hard_mode
                if mode is not None:
                    apply_mode(mode)


def run():
    mode_page = pygame.display.set_mode((Game.c.WINDOW_WIDTH, Game.c.WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game For Choosing Specific Mode")
    clock = pygame.time.Clock()
    
    #引入字体
    path = r"D:\Github\Sources\font_collections\MYuppy\myuppygb-medium.ttf"
    Mode_text = pygame.font.Font(path, 72).render("Mode Choose", True, Game.c.WHITE)
        
    Mode1_text = pygame.font.Font(None, 64).render("Easy Mode", True, Game.c.WHITE)
    rect_Mode1 = pygame.Rect(Game.c.WINDOW_WIDTH // 2 - Mode1_text.get_width() // 2, Game.c.WINDOW_HEIGHT // 2 - 50 - Mode1_text.get_height() // 2, Mode1_text.get_width(), Mode1_text.get_height())
    Mode2_text = pygame.font.Font(None, 64).render("Normal Mode", True, Game.c.WHITE)
    rect_Mode2 = pygame.Rect(Game.c.WINDOW_WIDTH // 2 - Mode2_text.get_width() // 2, Game.c.WINDOW_HEIGHT // 2 + 50 - Mode2_text.get_height() // 2, Mode2_text.get_width(), Mode2_text.get_height())
    Mode3_text = pygame.font.Font(None, 64).render("Hard Mode", True, Game.c.WHITE)
    rect_Mode3 = pygame.Rect(Game.c.WINDOW_WIDTH // 2 - Mode3_text.get_width() // 2, Game.c.WINDOW_HEIGHT // 2 + 150 - Mode3_text.get_height() // 2, Mode3_text.get_width(), Mode3_text.get_height())
    
    
    #事件处理
    while True:
        handle_events(rect_Mode1, rect_Mode2, rect_Mode3)
        draw(mode_page, Mode_text, Mode1_text, Mode2_text, Mode3_text)
        clock.tick(60)  # 控制帧率为60FPS