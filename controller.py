# controller.py 管理
# 林槐出品，必属稽品 - By Stapx Steve 2021/10/25
import random

import pygame

import articleobj
import globalvar


class Bg:
    # 用于控制背景图片相关的控制类
    bgImg = './images/bg.jpg'

    def loadBg(self):
        bg = pygame.image.load(self.bgImg).convert()
        globalvar.screen.blit(bg, (0, 0))


class EnemyCreator:
    # 创建敌人的相关逻辑
    enemy_list = []

    # 创建敌人
    def create(self):
        if len(self.enemy_list) < globalvar.body_max:
            enemy = articleobj.Flight(globalvar.FlightType.ENEMY, random.randint(0, globalvar.width), 0)
            # 添加列表
            self.enemy_list.append(enemy)

    # 敌人死亡判定
    def collision(self):
        remove = None
        for enemy in self.enemy_list:
            harf_x = enemy.width / 2
            harf_y = enemy.height / 2
            for bullet in globalvar.master.bullet_list:
                if enemy.x - harf_x <= bullet.x <= enemy.x + harf_x and \
                   enemy.y - harf_y <= bullet.y <= enemy.y + harf_y and \
                   bullet.type == globalvar.FlightType.MASTER:
                    print("击中", enemy)
                    remove = enemy
                    break
        if remove is not None:
            self.enemy_list.remove(remove)
        # TODO 加分计算
