import Game
import pygame
import sys
import Music_play
import Game_mode


'''
def draw_button(surface, text, font, color, rect,path=None):
    Text_text = pygame.font.Font(path, font).render(text, True, color)
    surface.blit(Text_text, (Game.c.WINDOW_WIDTH //2 - Text_text.get_width() // 2, Game.c.WINDOW_HEIGHT // 2 - Text_text.get_height() // 2))
'''



def draw(option_page,GameTopic_text, GameStart_button_text, GameMode_button_text, MusicPlay_button_text):
    #界面绘制
        option_page.fill(Game.c.PURPLE)
        
        #UI界面绘制
        
        #背景图片添加
        img_source = "D:\\Github\\Sources\\img_collections\\Steedy_snake(1).jpg"
        background = pygame.image.load(img_source)
        option_page.blit(background,(0,0))        
        
        #文字渲染
        option_page.blit(GameTopic_text, (Game.c.WINDOW_WIDTH // 2 - GameTopic_text.get_width() // 2, Game.c.WINDOW_HEIGHT // 2 - 150 - GameTopic_text.get_height() // 2))
    
        option_page.blit(GameStart_button_text, (Game.c.WINDOW_WIDTH // 2 - GameStart_button_text.get_width() // 2, Game.c.WINDOW_HEIGHT // 2 - 50 - GameStart_button_text.get_height() // 2))
                
        option_page.blit(GameMode_button_text, (Game.c.WINDOW_WIDTH // 2 - GameMode_button_text.get_width() // 2, Game.c.WINDOW_HEIGHT // 2 + 50 - GameMode_button_text.get_height() // 2))

        option_page.blit(MusicPlay_button_text, (Game.c.WINDOW_WIDTH // 2 - MusicPlay_button_text.get_width() // 2, Game.c.WINDOW_HEIGHT // 2 + 150 - MusicPlay_button_text.get_height() // 2))
        
        pygame.display.flip()

def handle_events(rect_GameStart, rect_GameMode, rect_MusicPlay):
    #事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
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
if __name__ == "__main__":
    #制作贪吃蛇游戏首页

    #创建窗口
    pygame.init()
    option_page = pygame.display.set_mode((Game.c.WINDOW_WIDTH, Game.c.WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game For Choosing Specific Mode")
    clock = pygame.time.Clock()

    #引入字体
    path = r"D:\Github\Sources\font_collections\MYuppy\myuppygb-medium.ttf"
    GameTopic_text = pygame.font.Font(path, 72).render("Snake Game", True, Game.c.GREEN)
    
    GameStart_button_text = pygame.font.Font(None, 64).render("Start Game", True, Game.c.DARK_GREEN)
    rect_GameStart = pygame.Rect(Game.c.WINDOW_WIDTH // 2 - GameStart_button_text.get_width() // 2, Game.c.WINDOW_HEIGHT // 2 - 50 - GameStart_button_text.get_height() // 2, GameStart_button_text.get_width(), GameStart_button_text.get_height())
    GameMode_button_text = pygame.font.Font(None, 64).render("Choose Game Mode", True, Game.c.DARK_GREEN)
    rect_GameMode = pygame.Rect(Game.c.WINDOW_WIDTH // 2 - GameMode_button_text.get_width() // 2, Game.c.WINDOW_HEIGHT // 2 + 50 - GameMode_button_text.get_height() // 2, GameMode_button_text.get_width(), GameMode_button_text.get_height())
    MusicPlay_button_text = pygame.font.Font(None, 64).render("Play Music", True, Game.c.DARK_GREEN)
    rect_MusicPlay = pygame.Rect(Game.c.WINDOW_WIDTH // 2 - MusicPlay_button_text.get_width() // 2, Game.c.WINDOW_HEIGHT // 2 + 150 - MusicPlay_button_text.get_height() // 2, MusicPlay_button_text.get_width(), MusicPlay_button_text.get_height())


    #事件处理
    while True:
        handle_events(rect_GameStart, rect_GameMode, rect_MusicPlay)
        draw(option_page, GameTopic_text, GameStart_button_text, GameMode_button_text, MusicPlay_button_text)
        clock.tick(60)  # 控制帧率为60FPS
   