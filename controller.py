# controller.py 工具
# 林槐出品，必属稽品 - By Stapx Steve 2021/10/25

import pygame

import globalvar


class Bg:
    # 用于控制背景图片相关的控制类
    bgImg = './images/bg.jpg'

    def loadBg(self):
        bg = pygame.image.load(self.bgImg).convert()
        globalvar.screen.blit(bg, (0, 0))
