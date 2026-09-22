'''
用于合成并预加载音效
'''
# Sound_effects.py —— UI音效
# 不依赖任何外部音频文件:用正弦波在内存里合成短促的"滴"声。
# 下载到真实音效时,只需把 _synth(...) 换成 pygame.mixer.Sound("文件路径")
import array
import math
import pygame

_sounds = {}


def _synth(freq, ms, volume=0.3):
    """合成一段正弦波短音效。
    freq: 频率(赫兹),越高声音越尖; ms: 时长(毫秒); volume: 音量 0~1
    末尾做线性淡出,避免波形突然截断产生"啪"的爆音
    """
    if pygame.mixer.get_init() is None:
        pygame.mixer.init()
    rate, fmt, channels = pygame.mixer.get_init()

    n = int(rate * ms / 1000)            # 采样点总数
    buf = array.array('h')               # 16位有符号样本
    for i in range(n):
        t = i / rate
        env = 1.0 - i / n                # 淡出包络
        sample = int(32767 * volume * env * math.sin(2 * math.pi * freq * t))
        if channels == 2:                # 立体声时左右声道各写一份
            buf.append(sample)
            buf.append(sample)
        else:
            buf.append(sample)
    return pygame.mixer.Sound(buffer=buf.tobytes())


def load():
    """页面启动时调用一次,预加载所有音效(避免第一次点击时卡顿)"""
    global _sounds
    if _sounds:      # 已经加载过就不用重复加载
        return
    try:
        _sounds = {
            'click': _synth(880, 60, 0.35),   # 点击:短促高音
            'hover': _synth(440, 30, 0.12),   # 悬停:很轻的提示音
            'back':  _synth(330, 120, 0.30),  # 返回:低沉下滑音
        }
    except pygame.error:
        _sounds = {}  # 没有音频设备时静默降级:游戏照常运行,只是没声音


def play(name):
    if name in _sounds:
        _sounds[name].play()
