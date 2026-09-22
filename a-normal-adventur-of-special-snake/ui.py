'''
通用button类,服务于三个交互界面

作用:给主页面/子页面提供统一的按钮外观与交互反馈
   1. 三种视觉状态:普通 / 悬停 / 按下
   2. 悬停时提亮并显示手型光标,按下时文字下沉2像素
   3. 点击、悬停自动播放音效(音效在 Sound_effects.py 中预加载
'''
import pygame
import Sound_effects


class Button:
    def __init__(self, center, text, font, text_color,
                 bg_color, hover_color, press_color,
                 padding=(30, 14), radius=14, on_click=None):
        # center: 按钮中心坐标(x, y)
        # on_click: 被点击时要执行的函数
        self.font = font
        self.text_color = text_color
        self.padding = padding
        self.radius = radius
        self.on_click = on_click
        self.text = text  # 记录文字内容,便于以后用 set_text 更换

        self._build_surface(text)
        self.rect = self.text_surf.get_rect(center=center)
        self.rect.inflate_ip(padding[0] * 2, padding[1] * 2)

        self.colors = {"normal": bg_color, "hover": hover_color, "press": press_color}
        self.state = "normal"      # 当前视觉状态
        self.hovered = False       # 鼠标是否悬停
        self.press_until = 0       # 按压高亮持续到的时刻(毫秒),松开后仍保留一小段

    def _build_surface(self, text):
        # 文字只需渲染一次,之后每帧直接贴图(每帧渲染文字很耗性能)
        self.text_surf = self.font.render(text, True, self.text_color)

    def set_text(self, text):
        # 更换按钮文字(如音乐页的 Play / Stop 切换),并保持中心位置不变
        self.text = text
        self._build_surface(text)
        center = self.rect.center
        self.rect = self.text_surf.get_rect(center=center)
        self.rect.inflate_ip(self.padding[0] * 2, self.padding[1] * 2)

    def handle_event(self, event):
        # 被左键点中时:播放点击音效并执行 on_click,返回 True
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                and self.rect.collidepoint(event.pos)):
            self.press_until = pygame.time.get_ticks() + 120
            Sound_effects.play("click")
            if self.on_click:
                self.on_click()
            return True
        return False

    def draw(self, surface):
        # 先判断悬停,并只在"刚悬停上来"的那一帧播放提示音(不会每帧重复)
        was_hovered = self.hovered
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        if self.hovered and not was_hovered:
            Sound_effects.play("hover")

        # 决定视觉状态:正在按压 > 按压余晖 > 悬停 > 普通
        if self.hovered and pygame.mouse.get_pressed()[0]:
            self.state = "press"
        elif pygame.time.get_ticks() < self.press_until:
            self.state = "press"
        elif self.hovered:
            self.state = "hover"
        else:
            self.state = "normal"

        # 半透明圆角面板:带Alpha的颜色不能直接画在主画布上,
        # 必须画在一张 SRCALPHA 透明图层上再贴到主画布
        panel = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.rect(panel, self.colors[self.state], panel.get_rect(),
                         border_radius=self.radius)
        surface.blit(panel, self.rect.topleft)

        # 文字:按下时整体下沉2像素,模拟物理按压
        offset = 2 if self.state == "press" else 0
        surface.blit(self.text_surf, self.text_surf.get_rect(
            center=(self.rect.centerx, self.rect.centery + offset)))

        # 悬停时把系统光标换成手型
        if self.hovered:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

