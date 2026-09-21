import pygame
import sys
import Game

#初始化pygame
pygame.init()

music_playing = False  # 音乐播放状态,默认状态,暂未用到

def draw(music_page,Music_dict,Music_playing_text,play_rect):
    # 绘制音乐播放页面
    music_page.fill(Game.c.BLACK)  # 设置背景颜色为黑色
    
    #UI界面绘制
    
    #背景
    img_path = "D:\\Github\\Sources\\img_collections\\Sakura_love(1).jpeg"
    background_img = pygame.image.load(img_path)
    music_page.blit(background_img,(0,0))
    
    for render,rect in Music_dict:
        music_page.blit(render,rect)
    music_page.blit(Music_playing_text,play_rect)
    
    pygame.display.flip()


def handle_music_events(music_files,play_rect,Music_rect_list):
    global music_playing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
             
            if event.button == 1:  # 左键点击
                mouse_pos = pygame.mouse.get_pos()
                if play_rect.collidepoint(mouse_pos):
                    music_playing = not music_playing
                    if not music_playing:
                        pygame.mixer.music.stop() #停止播放
                for (music_name, music_path),music_rect in zip(music_files.items(),Music_rect_list):
                    if music_playing:
                        if music_rect.collidepoint(mouse_pos):
                            print(f"Playing {music_name}...")
                            pygame.mixer.music.load(music_path)
                            pygame.mixer.music.play(-1)  # 循环播放
        
    return True



def run():
    running = True
    #创建子页面--音乐播放页面
    music_page = pygame.display.set_mode((Game.c.WINDOW_WIDTH, Game.c.WINDOW_HEIGHT))
    pygame.display.set_caption("Music Play Page")
    clock = pygame.time.Clock()
    
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
    
    Music_rect_list = []
    render_list = []
    origin = - 30
    for music in music_files.keys():
        music_text = pygame.font.Font(None,48).render(music,True,Game.c.PURPLE)
        render_list.append(music_text)
        music_rect = music_text.get_rect(center=(Game.c.WINDOW_WIDTH // 2, Game.c.WINDOW_HEIGHT // 2 + origin - 200))
        Music_rect_list.append(music_rect)
        origin += 50
    
    Music_playing_text = pygame.font.Font(None,56).render("Play or Stop",True,Game.c.RED)
    render_list.append(Music_playing_text)
    play_rect = Music_playing_text.get_rect(center=(Game.c.WINDOW_WIDTH // 2, Game.c.WINDOW_HEIGHT // 2 + 100))
    #Music_dict = zip(render_list,Music_rect_list) 这是个一次性迭代器，一帧内遍历完就为空，所以革命全没了
    Music_dict = list(zip(render_list,Music_rect_list)) 
 
    
    #进行事件处理和绘制
    while running:
        running = handle_music_events(music_files,play_rect,Music_rect_list)
        draw(music_page, Music_dict, Music_playing_text, play_rect)
        clock.tick(60)  # 控制帧率为60FPS
    
