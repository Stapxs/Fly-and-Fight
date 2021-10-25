# controller.py 管理
# 林槐出品，必属稽品 - By Stapx Steve 2021/10/25
import tkinter
import random
import pygame

import tkinter.messagebox

import articleobj
import globalvar


class Bg:
    # 用于控制背景图片相关的控制类
    bgImg = './images/bg.jpg'

    def loadBg(self):
        bg = pygame.image.load(self.bgImg).convert()
        globalvar.screen.blit(bg, (0, 0))
        # 加载额外的 UI 文字
        if (globalvar.ui == 'main' and globalvar.body_max == 0) or globalvar.ui == 'died':
            fontObj = pygame.font.Font('freesansbold.ttf', 17)  # 初始化字体
            textSurfaceObj = fontObj.render(u'Q - Exit', True, (255, 255, 255))  # 开始介绍文字
            globalvar.screen.blit(textSurfaceObj, (15, globalvar.height - 30))
            textSurfaceObj = fontObj.render(u'R - Start & Restart', True, (255, 255, 255))
            globalvar.screen.blit(textSurfaceObj, (15, globalvar.height - 60))
            textSurfaceObj = fontObj.render(u'W,A,S,D - Control', True, (255, 255, 255))
            globalvar.screen.blit(textSurfaceObj, (15, globalvar.height - 90))

            fontObj = pygame.font.Font('freesansbold.ttf', 10)  # 初始化字体
            textSurfaceObj = fontObj.render('v' + globalvar.version, True, (255, 255, 255))
            globalvar.screen.blit(textSurfaceObj, (105, globalvar.height - 145))

            fontObj = pygame.font.Font('freesansbold.ttf', 13)  # 初始化字体
            textSurfaceObj = fontObj.render('By Stapx Steve', True, (255, 255, 255))
            globalvar.screen.blit(textSurfaceObj, (15, globalvar.height - 130))

            fontObj = pygame.font.Font('freesansbold.ttf', 17)  # 初始化字体
            textSurfaceObj = fontObj.render(u'Fly&Fight ', True, (255, 255, 255))
            globalvar.screen.blit(textSurfaceObj, (15, globalvar.height - 150))
        if globalvar.ui == 'died':
            fontObj = pygame.font.Font('freesansbold.ttf', 35)  # 初始化字体
            textSurfaceObj = fontObj.render('You Are Died', True, (0, 0, 0))
            globalvar.screen.blit(textSurfaceObj, (globalvar.width / 2 - textSurfaceObj.get_rect().width / 2 + 5, globalvar.height / 2 - 55))
            textSurfaceObj = fontObj.render('You Are Died', True, (255, 255, 255))
            globalvar.screen.blit(textSurfaceObj, (globalvar.width / 2 - textSurfaceObj.get_rect().width / 2, globalvar.height / 2 - 60))
        if globalvar.ui == 'game' or globalvar.ui == 'died':
            fontObj = pygame.font.Font('freesansbold.ttf', 35)  # 初始化字体
            textSurfaceObj = fontObj.render(str(globalvar.source), True, (255, 255, 255))
            globalvar.screen.blit(textSurfaceObj, (globalvar.width - textSurfaceObj.get_rect().width - 15, 15))


class EnemyCreator:
    # 创建敌人的相关逻辑
    enemy_list = []

    # 创建敌人
    def create(self):
        if len(self.enemy_list) < globalvar.body_max:
            do_create = random.randint(0, 5)
            if do_create == 1:
                enemy = articleobj.Flight(globalvar.FlightType.ENEMY, random.randint(0, globalvar.width), 0)
                # 添加列表
                self.enemy_list.append(enemy)

    # 死亡判定
    def collision(self):
        remove = None
        remove_bullet = None
        for enemy in self.enemy_list:
            half_x = enemy.width / 2
            half_y = enemy.height / 2
            # 敌人死亡判定
            for bullet in globalvar.master.bullet_list:
                if enemy.x - half_x <= bullet.x <= enemy.x + half_x and \
                        enemy.y - half_y <= bullet.y <= enemy.y + half_y and \
                        bullet.type == globalvar.FlightType.MASTER:
                    print("击中", enemy)
                    remove = enemy
                    remove_bullet = bullet
                    break
            half_x = globalvar.master.width / 2
            half_y = globalvar.master.height / 2
            # 主机死亡判定
            for bullet in enemy.bullet_list:
                if globalvar.master.x - half_x <= bullet.x <= globalvar.master.x + half_x and \
                        globalvar.master.y - half_y <= bullet.y <= globalvar.master.y + half_y and \
                        bullet.type == globalvar.FlightType.ENEMY:
                    print("被击中", bullet)
                    # 清空画面
                    self.enemy_list.clear()
                    globalvar.master.bullet_list.clear()
                    # 停止生成
                    globalvar.body_max_bak = globalvar.body_max
                    globalvar.body_max = 0
                    # 切换 UI
                    globalvar.ui = 'died'
                    # 归中主机
                    globalvar.master.x = globalvar.width / 2 - globalvar.master.width / 2
                    globalvar.master.y = globalvar.height / 2
                    return
        if remove is not None:  # 移除敌人
            self.enemy_list.remove(remove)
            # TODO 加分计算
            globalvar.source += 1
        if remove_bullet is not None:  # 移除子弹
            globalvar.master.bullet_list.remove(remove_bullet)