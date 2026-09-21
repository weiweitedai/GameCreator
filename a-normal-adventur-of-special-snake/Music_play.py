import pygame
import sys
import Game

#初始化pygame
pygame.init()

def draw(music_page, music_files, font):
    # 绘制音乐播放页面
    music_page.fill((0, 0, 0))  # 设置背景颜色为黑色

    y_offset = 50
    for music_name in music_files.keys():
        text_surface = font.render(music_name, True, (255, 255, 255))  # 白色文字
        music_page.blit(text_surface, (50, y_offset))
        y_offset += 50

    pygame.display.flip()


def handle_music_events(music_files):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键点击
                mouse_pos = pygame.mouse.get_pos()
                y_offset = 50
                for music_name, music_path in music_files.items():
                    text_rect = pygame.Rect(50, y_offset, 200, 40)  # 假设每个音乐名称的区域为200x40
                    if text_rect.collidepoint(mouse_pos):
                        print(f"Playing {music_name}...")
                        pygame.mixer.music.load(music_path)
                        pygame.mixer.music.play(-1)  # 循环播放
                    y_offset += 50



music_playing = False  # 音乐播放状态,默认状态,暂未用到

#提供音乐文件播放路径
One_last_kiss_path = r"D:\Github\Sources\snd_collections\One_last_kiss.mp3"  
Forest_path = r"D:\Github\Sources\snd_collections\forest.ogg"
Cave_path = r"D:\Github\Sources\snd_collections\cave themeb4.ogg"
B423b42_path = r"D:\Github\Sources\snd_collections\b423b42.wav"

music_files = {
    "One Last Kiss": One_last_kiss_path,
    "Forest": Forest_path,
    "Cave": Cave_path,
    "B423b42": B423b42_path
}
def run():
    #创建子页面--音乐播放页面
    music_page = pygame.display.set_mode((Game.c.WINDOW_WIDTH, Game.c.WINDOW_HEIGHT))
    pygame.display.set_caption("Music Play Page")
    clock = pygame.time.Clock()
 

    #进行事件处理和绘制
    while True:
        handle_music_events(music_files)
        draw(music_page, music_files, pygame.font.Font(None, 36))
        clock.tick(60)  # 控制帧率为60FPS
    
