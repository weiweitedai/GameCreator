import Game
import pygame
import sys
import os
import Music_play
import Game_mode
import ui #新增通用按钮控件
import Sound_effects #新增：UI音效

#图片目录:项目根下的 img_collections,基于脚本位置定位,不依赖运行目录
IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "img_collections")


'''
def draw_button(surface, text, font, color, rect,path=None):
    Text_text = pygame.font.Font(path, font).render(text, True, color)
    surface.blit(Text_text, (Game.c.WINDOW_WIDTH //2 - Text_text.get_width() // 2, Game.c.WINDOW_HEIGHT // 2 - Text_text.get_height() // 2))
'''



def draw(option_page,GameTopic_text,background,buttons):
        #界面绘制
        option_page.fill(Game.c.PURPLE)
        
        #UI界面绘制
        
        #背景图片添加
        option_page.blit(background,(0,0))
        
        #标题渲染
        option_page.blit(GameTopic_text, (Game.c.WINDOW_WIDTH // 2 - GameTopic_text.get_width() // 2, Game.c.WINDOW_HEIGHT // 2 - 150 - GameTopic_text.get_height() // 2))
                
        #按钮:先把光标重置为箭头,悬停中的按钮会自己把光标换成手型
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        for button in buttons:
            button.draw(option_page)
        '''
        #文字渲染
        option_page.blit(GameStart_button_text, (Game.c.WINDOW_WIDTH // 2 - GameStart_button_text.get_width() // 2, Game.c.WINDOW_HEIGHT // 2 - 50 - GameStart_button_text.get_height() // 2))
                
        option_page.blit(GameMode_button_text, (Game.c.WINDOW_WIDTH // 2 - GameMode_button_text.get_width() // 2, Game.c.WINDOW_HEIGHT // 2 + 50 - GameMode_button_text.get_height() // 2))

        option_page.blit(MusicPlay_button_text, (Game.c.WINDOW_WIDTH // 2 - MusicPlay_button_text.get_width() // 2, Game.c.WINDOW_HEIGHT // 2 + 150 - MusicPlay_button_text.get_height() // 2))
        '''
        pygame.display.flip()

def handle_events(buttons):
    #事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        for button in buttons:
            button.handle_event(event)
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键点击
                mouse_pos = pygame.mouse.get_pos()
                if rect_GameStart.collidepoint(mouse_pos):
                    print("Start Game button clicked!")
                    game = Game.Game()
                    game.run()
                elif rect_GameMode.collidepoint(mouse_pos):
                    print("Choose Game Mode button clicked!")
                    Game_mode.run()
                elif rect_MusicPlay.collidepoint(mouse_pos):
                    print("Play Music button clicked!")
                    Music_play.run()
        '''
if __name__ == "__main__":
    #制作贪吃蛇游戏首页

    #创建窗口
    pygame.init()
    
    Sound_effects.load() #预加载点击/悬停音效
    
    option_page = pygame.display.set_mode((Game.c.WINDOW_WIDTH, Game.c.WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game For Choosing Specific Mode")
    clock = pygame.time.Clock()
    
    #背景图
    img_source = os.path.join(IMG_DIR, "Steedy_snake(1).jpg")
    background = pygame.image.load(img_source)

    #标题字体创建
    FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..',"font_collections\\MYuppy")
    path = os.path.join(FONT_DIR,"myuppygb-medium.ttf")
    GameTopic_text = pygame.font.Font(path, 72).render("Snake Game", True, Game.c.GREEN)
    
    
    '''
    GameStart_button_text = pygame.font.Font(None, 64).render("Start Game", True, Game.c.DARK_GREEN)
    rect_GameStart = pygame.Rect(Game.c.WINDOW_WIDTH // 2 - GameStart_button_text.get_width() // 2, Game.c.WINDOW_HEIGHT // 2 - 50 - GameStart_button_text.get_height() // 2, GameStart_button_text.get_width(), GameStart_button_text.get_height())
    GameMode_button_text = pygame.font.Font(None, 64).render("Choose Game Mode", True, Game.c.DARK_GREEN)
    rect_GameMode = pygame.Rect(Game.c.WINDOW_WIDTH // 2 - GameMode_button_text.get_width() // 2, Game.c.WINDOW_HEIGHT // 2 + 50 - GameMode_button_text.get_height() // 2, GameMode_button_text.get_width(), GameMode_button_text.get_height())
    MusicPlay_button_text = pygame.font.Font(None, 64).render("Play Music", True, Game.c.DARK_GREEN)
    rect_MusicPlay = pygame.Rect(Game.c.WINDOW_WIDTH // 2 - MusicPlay_button_text.get_width() // 2, Game.c.WINDOW_HEIGHT // 2 + 150 - MusicPlay_button_text.get_height() // 2, MusicPlay_button_text.get_width(), MusicPlay_button_text.get_height())
    '''
    #三个按钮:中心坐标 + 文字 + 三种状态颜色 + 点击后执行的动作
    font = pygame.font.Font(None, 64)
    cx = Game.c.WINDOW_WIDTH // 2
    cy = Game.c.WINDOW_HEIGHT // 2
    buttons = [
        ui.Button((cx, cy - 70), "Start Game", font, Game.c.WHITE,
                  Game.c.BTN_BG, Game.c.BTN_HOVER, Game.c.BTN_PRESS,
                  on_click=lambda: Game.Game().run()),
        ui.Button((cx, cy + 40), "Choose Game Mode", font, Game.c.WHITE,
                  Game.c.BTN_BG, Game.c.BTN_HOVER, Game.c.BTN_PRESS,
                  on_click=Game_mode.run),
        ui.Button((cx, cy + 150), "Play Music", font, Game.c.WHITE,
                  Game.c.BTN_BG, Game.c.BTN_HOVER, Game.c.BTN_PRESS,
                  on_click=Music_play.run),
    ]
   
    #事件处理
    while True:
        handle_events(buttons)
        draw(option_page, GameTopic_text,background,buttons)
        clock.tick(60)  # 控制帧率为60FPS
   