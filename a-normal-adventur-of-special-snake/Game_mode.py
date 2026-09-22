import pygame
import sys
import os
import Game
import ui             # 新增:通用按钮控件
import Sound_effects  # 新增:UI音效

#图片目录:项目根下的 img_collections,基于脚本位置定位,不依赖运行目录
IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "img_collections")


def draw(mode_page, background, Mode_text, hint_text, buttons):
    mode_page.blit(background, (0, 0))

    #标题
    mode_page.blit(Mode_text, (
        Game.c.WINDOW_WIDTH // 2 - Mode_text.get_width() // 2,
        Game.c.WINDOW_HEIGHT // 2 - 190 - Mode_text.get_height() // 2))

    #底部提示(原来只能靠猜:ESC能返回,但界面上没有任何提示)
    mode_page.blit(hint_text, hint_text.get_rect(
        center=(Game.c.WINDOW_WIDTH // 2, Game.c.WINDOW_HEIGHT - 30)))

    #按钮(光标处理同主页)
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    for button in buttons:
        button.draw(mode_page)

    pygame.display.flip()


def apply_mode(mode):
    #根据所选模式,修改Constant.py中的障碍物数量范围
    Game.c.OBSTACLE_COUNT_LOW = mode['OBSTACLE_COUNT_LOW']
    Game.c.OBSTACLE_COUNT_HIGH = mode['OBSTACLE_COUNT_HIGH']
    print(f"OBSTACLE_COUNT: {Game.c.OBSTACLE_COUNT_LOW} ~ {Game.c.OBSTACLE_COUNT_HIGH}")


def handle_events(buttons):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Sound_effects.play("back")  # 返回主页面时给一个声音反馈
                return False
        for button in buttons:
            button.handle_event(event)
    return True


def run():
    running = True
    mode_page = pygame.display.set_mode((Game.c.WINDOW_WIDTH, Game.c.WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game For Choosing Specific Mode")
    clock = pygame.time.Clock()
    Sound_effects.load()  # 已加载过的话会自动跳过

    #背景图只加载一次
    background = pygame.image.load(os.path.join(IMG_DIR, "Cute_girls(1).jpg"))

    path = r"D:\Github\Sources\font_collections\MYuppy\myuppygb-medium.ttf"
    Mode_text = pygame.font.Font(path, 72).render("Mode Choose", True, Game.c.RED)
    hint_text = pygame.font.Font(None, 24).render(
        "Press ESC to go back to the main page", True, Game.c.WHITE)

    font = pygame.font.Font(None, 64)
    cx = Game.c.WINDOW_WIDTH // 2
    cy = Game.c.WINDOW_HEIGHT // 2
    buttons = [
        ui.Button((cx, cy - 70), "Easy Mode", font, Game.c.WHITE,
                  Game.c.BTN_BG, Game.c.BTN_HOVER, Game.c.BTN_PRESS,
                  on_click=lambda: apply_mode(Game.c.Easy_mode)),
        ui.Button((cx, cy + 40), "Normal Mode", font, Game.c.WHITE,
                  Game.c.BTN_BG, Game.c.BTN_HOVER, Game.c.BTN_PRESS,
                  on_click=lambda: apply_mode(Game.c.Normal_mode)),
        ui.Button((cx, cy + 150), "Hard Mode", font, Game.c.WHITE,
                  Game.c.BTN_BG, Game.c.BTN_HOVER, Game.c.BTN_PRESS,
                  on_click=lambda: apply_mode(Game.c.Hard_mode)),
    ]

    while running:
        running = handle_events(buttons)
        draw(mode_page, background, Mode_text, hint_text, buttons)
        clock.tick(60)
