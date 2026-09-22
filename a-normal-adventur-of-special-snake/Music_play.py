import pygame
import sys
import os
import Game
import ui             # 新增:通用按钮控件
import Sound_effects  # 新增:UI音效

#图片目录:项目根下的 img_collections,基于脚本位置定位,不依赖运行目录
IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "img_collections")
#音乐目录:同上
SND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "snd_collections")

#初始化pygame
pygame.init()

music_playing = False  # 音乐播放状态


def toggle_play():
    #播放/停止切换(点击 Play/Stop 按钮时执行)
    global music_playing
    music_playing = not music_playing
    if not music_playing:
        pygame.mixer.music.stop()


def play_song(music_name, music_path):
    #点中歌名时执行:只有处于"播放"状态才会加载并循环播放
    if music_playing:
        print(f"Playing {music_name}...")
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)


def draw(music_page, background, title_text, play_button, song_buttons):
    music_page.blit(background, (0, 0))

    #标题
    music_page.blit(title_text, title_text.get_rect(
        center=(Game.c.WINDOW_WIDTH // 2, Game.c.WINDOW_HEIGHT // 2 - 260)))

    #播放按钮的文字随状态变化:播放中显示 Stop,停止时显示 Play
    label = "Stop Music" if music_playing else "Play Music"
    if play_button.text != label:
        play_button.set_text(label)

    #按钮(光标处理同主页)
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    play_button.draw(music_page)
    for button in song_buttons:
        button.draw(music_page)

    pygame.display.flip()


def handle_music_events(play_button, song_buttons):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Sound_effects.play("back")
                return False
        play_button.handle_event(event)
        for button in song_buttons:
            button.handle_event(event)
    return True


def run():
    running = True
    music_page = pygame.display.set_mode((Game.c.WINDOW_WIDTH, Game.c.WINDOW_HEIGHT))
    pygame.display.set_caption("Music Play Page")
    clock = pygame.time.Clock()
    Sound_effects.load()

    #背景图只加载一次
    background = pygame.image.load(os.path.join(IMG_DIR, "Sakura_love(1).jpeg"))

    music_files = {
        "One Last Kiss": os.path.join(SND_DIR, 'One_last_kiss.mp3'),
        "Forest": os.path.join(SND_DIR, 'forest.ogg'),
        "Cave": os.path.join(SND_DIR, 'cave themeb4.ogg'),
        "B423b42": os.path.join(SND_DIR, 'b423b42.wav'),
    }

    title_text = pygame.font.Font(None, 56).render("Music Player", True, Game.c.WHITE)

    #四个歌名按钮,从上到下排列
    #注意 lambda 要写 n=name, p=path:闭包延迟求值,
    #不写默认参数的话,所有按钮点击时都会拿到循环最后的那个 path
    font = pygame.font.Font(None, 48)
    cx = Game.c.WINDOW_WIDTH // 2
    cy = Game.c.WINDOW_HEIGHT // 2
    song_buttons = []
    for i, (name, path) in enumerate(music_files.items()):
        song_buttons.append(ui.Button(
            (cx, cy - 180 + i * 90), name, font, Game.c.WHITE,
            Game.c.BTN_BG, Game.c.BTN_HOVER, Game.c.BTN_PRESS,
            on_click=lambda n=name, p=path: play_song(n, p)))

    #播放/停止按钮
    play_button = ui.Button((cx, cy + 180), "Play Music", pygame.font.Font(None, 56),
                            Game.c.WHITE,
                            Game.c.BTN_BG, Game.c.BTN_HOVER, Game.c.BTN_PRESS,
                            on_click=toggle_play)

    while running:
        running = handle_music_events(play_button, song_buttons)
        draw(music_page, background, title_text, play_button, song_buttons)
        clock.tick(60)
