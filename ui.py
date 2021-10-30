# controller.py 管理
# 林槐出品，必属稽品 - By Stapx Steve 2021/10/26

import pygame

import globalvar


# 输出 UI 相关逻辑

def title():
    fontObj = pygame.font.Font('freesansbold.ttf', 35)  # 初始化字体
    textSurfaceObj = fontObj.render('Fly & Fight', True, (0, 0, 0))
    globalvar.screen.blit(textSurfaceObj, (
        globalvar.width / 2 - textSurfaceObj.get_rect().width / 2 + 5, globalvar.height / 3 - 55))
    textSurfaceObj = fontObj.render('Fly & Fight', True, (255, 255, 255))
    globalvar.screen.blit(textSurfaceObj, (
        globalvar.width / 2 - textSurfaceObj.get_rect().width / 2, globalvar.height / 3 - 60))


def control_note():
    text(u'Q - Exit', 17, (255, 255, 255), (15, globalvar.height - 30))
    text(u'R - Start & Restart', 17, (255, 255, 255), (15, globalvar.height - 60))
    text(u'SPACE - Fire', 17, (255, 255, 255), (15, globalvar.height - 90))
    text(u'W,A,S,D - Control', 17, (255, 255, 255), (15, globalvar.height - 120))


def small_title():
    text('v' + globalvar.version, 10, (255, 255, 255), (105, globalvar.height - 175))
    text(u'By Stapx Steve', 13, (255, 255, 255), (15, globalvar.height - 160))
    text(u'Fly&Fight', 17, (255, 255, 255), (15, globalvar.height - 180))


def die_title():
    fontObj = pygame.font.Font('freesansbold.ttf', 35)  # 初始化字体
    textSurfaceObj = fontObj.render('You Are Died', True, (0, 0, 0))
    globalvar.screen.blit(textSurfaceObj, (
        globalvar.width / 2 - textSurfaceObj.get_rect().width / 2 + 5, globalvar.height / 2 - 55))
    textSurfaceObj = fontObj.render('You Are Died', True, (255, 255, 255))
    globalvar.screen.blit(textSurfaceObj, (
        globalvar.width / 2 - textSurfaceObj.get_rect().width / 2, globalvar.height / 2 - 60))


def master_hp_line():
    pygame.draw.rect(globalvar.screen, (255, 255, 255),
                     (20, globalvar.height - 40, globalvar.width - 40, 20), 2)  # 血条外框
    color = (255, 255, 255)
    if globalvar.master.hp < globalvar.max_m_hp / 3:
        color = (184, 89, 74)
    pygame.draw.rect(globalvar.screen, color,
                     (24, globalvar.height - 35,
                      (globalvar.width - 40) * globalvar.master.hp / globalvar.max_m_hp - 8, 11), 0)  # 血条


def score():
    fontObj = pygame.font.Font('freesansbold.ttf', 35)  # 初始化字体
    textSurfaceObj = fontObj.render(str(globalvar.source), True, (255, 255, 255))
    globalvar.screen.blit(textSurfaceObj, (globalvar.width - textSurfaceObj.get_rect().width - 15, 15))


# 在屏幕上输出文字（简易）
def text(msg, size, color, point):
    fontObj = pygame.font.Font('freesansbold.ttf', size)  # 初始化字体
    textSurfaceObj = fontObj.render(msg, True, color)
    globalvar.screen.blit(textSurfaceObj, point)
