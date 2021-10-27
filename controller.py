# controller.py 管理
# 林槐出品，必属稽品 - By Stapx Steve 2021/10/25

import random
import pygame

import articleobj
import globalvar


class Display:
    # 用于控制背景图片相关的控制类
    bgImg = './images/bg.jpg'

    def loadBg(self):
        bg = pygame.image.load(self.bgImg).convert()
        globalvar.screen.blit(bg, (0, 0))
        # 加载额外的 UI 文字
        if globalvar.ui == 'home':
            fontObj = pygame.font.Font('freesansbold.ttf', 35)  # 初始化字体
            textSurfaceObj = fontObj.render('Fly & Fight', True, (0, 0, 0))
            globalvar.screen.blit(textSurfaceObj, (
                globalvar.width / 2 - textSurfaceObj.get_rect().width / 2 + 5, globalvar.height / 3 - 55))
            textSurfaceObj = fontObj.render('Fly & Fight', True, (255, 255, 255))
            globalvar.screen.blit(textSurfaceObj, (
                globalvar.width / 2 - textSurfaceObj.get_rect().width / 2, globalvar.height / 3 - 60))
        if (globalvar.ui == 'main' and globalvar.body_max == 0) or globalvar.ui == 'died' or globalvar.ui == 'home':
            self.text(u'Q - Exit', 17, (255, 255, 255), (15, globalvar.height - 30))
            self.text(u'R - Start & Restart', 17, (255, 255, 255), (15, globalvar.height - 60))
            self.text(u'SPACE - Fire', 17, (255, 255, 255), (15, globalvar.height - 90))
            self.text(u'W,A,S,D - Control', 17, (255, 255, 255), (15, globalvar.height - 120))
        if (globalvar.ui == 'main' and globalvar.body_max == 0) or globalvar.ui == 'died':
            self.text('v' + globalvar.version, 10, (255, 255, 255), (105, globalvar.height - 175))
            self.text(u'By Stapx Steve', 13, (255, 255, 255), (15, globalvar.height - 160))
            self.text(u'Fly&Fight', 17, (255, 255, 255), (15, globalvar.height - 180))
        if globalvar.ui == 'died':
            fontObj = pygame.font.Font('freesansbold.ttf', 35)  # 初始化字体
            textSurfaceObj = fontObj.render('You Are Died', True, (0, 0, 0))
            globalvar.screen.blit(textSurfaceObj, (
                globalvar.width / 2 - textSurfaceObj.get_rect().width / 2 + 5, globalvar.height / 2 - 55))
            textSurfaceObj = fontObj.render('You Are Died', True, (255, 255, 255))
            globalvar.screen.blit(textSurfaceObj, (
                globalvar.width / 2 - textSurfaceObj.get_rect().width / 2, globalvar.height / 2 - 60))
        if globalvar.ui == 'game' or globalvar.ui == 'died':
            fontObj = pygame.font.Font('freesansbold.ttf', 35)  # 初始化字体
            textSurfaceObj = fontObj.render(str(globalvar.source), True, (255, 255, 255))
            globalvar.screen.blit(textSurfaceObj, (globalvar.width - textSurfaceObj.get_rect().width - 15, 15))

    # 在屏幕上输出文字（简易）
    def text(self, msg, size, color, point):
        fontObj = pygame.font.Font('freesansbold.ttf', size)  # 初始化字体
        textSurfaceObj = fontObj.render(msg, True, color)
        globalvar.screen.blit(textSurfaceObj, point)


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
        for enemy in self.enemy_list:
            half_x = enemy.width / 2
            half_y = enemy.height / 2
            # 敌人死亡判定
            for bullet in globalvar.master.bullet_list:
                if enemy.x - half_x <= bullet.x <= enemy.x + half_x and \
                        enemy.y - half_y <= bullet.y <= enemy.y + half_y and \
                        bullet.type == globalvar.FlightType.MASTER:
                    # 血量判定
                    enemy.hp -= bullet.hit * (int(bullet.type) - 5)  # 计算伤害
                    print("击中", enemy, "血量：" + str(enemy.hp) + "(" + str(bullet.hit * (int(bullet.type) - 5)) + ")")
                    enemy.hp_times = 0  # 显示血量
                    if enemy.hp <= 0:  # 判定死亡
                        self.enemy_list.remove(enemy)
                        # TODO 加分计算
                        globalvar.source += 1
                    globalvar.master.bullet_list.remove(bullet)  # 移除子弹（防止穿透）
                    break
                # 移除出屏子弹
                if bullet.y < 0 or bullet.y > globalvar.height:
                    print("出屏子弹 >", bullet)
                    globalvar.master.bullet_list.remove(bullet)
            half_x = globalvar.master.width / 2
            half_y = globalvar.master.height / 2
            # 主机死亡判定
            for bullet in enemy.bullet_list:
                if globalvar.master.x - half_x <= bullet.x <= globalvar.master.x + half_x and \
                        globalvar.master.y - half_y <= bullet.y <= globalvar.master.y + half_y and \
                        bullet.type == globalvar.FlightType.ENEMY:
                    print("被击中", bullet, "血量：" + str(globalvar.master.hp) + "(" + str(bullet.hit * (int(bullet.type) - 5)) + ")")
                    globalvar.master.hp -= bullet.hit * (int(bullet.type) - 5)  # 计算伤害
                    globalvar.master.hp_times = 0  # 显示血量
                    if globalvar.master.hp <= 0:  # 判定死亡
                        # 清除血量显示
                        globalvar.hp_times = -1
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
                # 移除出屏子弹
                if bullet.y < 0 or bullet.y > globalvar.height:
                    print("出屏子弹 >", bullet)
                    globalvar.master.bullet_list.remove(bullet)