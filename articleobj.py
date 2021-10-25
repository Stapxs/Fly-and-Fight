# articleobj.py 对象
# 林槐出品，必属稽品 - By Stapx Steve 2021/10/25

import random
import pygame
from pygame import *

import globalvar


class Flight:
    x = 0  # 飞船位置
    y = 0
    width = 76  # 飞船大小
    height = 61
    type = None  # 飞船类型

    speed = 20  # 移送速度
    move_state = globalvar.Direction.RIGHT  # 移动状态（仅非 Master 有效）

    bullet_list = []  # 子弹列表

    # 构造函数
    def __init__(self, flight_type, x=0, y=0):
        self.type = flight_type
        if flight_type == globalvar.FlightType.MASTER:  # 主舰船
            # 创建主飞船图片（包含透明通道）
            self.mst_img = pygame.image.load('./images/master.png').convert_alpha()
            # 居中底部
            self.x = globalvar.width / 2 - self.width / 2
            self.y = globalvar.height - self.height * 2
        elif flight_type == globalvar.FlightType.ENEMY:  # 敌人
            # 创建敌人飞船图片 1-3 随机（包含透明通道）
            self.mst_img = pygame.image.load('./images/enemy_' + str(random.randint(1, 3)) + '.png').convert_alpha()
            # 设置位置
            self.x = x
            self.y = y
        elif flight_type == globalvar.FlightType.BOSS:  # TODO BOSS
            pass
        elif globalvar.debug:
            print("Flight > __init__ > 飞船类型无效！")

    # 显示
    def display(self):
        # 显示本飞船的子弹（子弹要叠在飞船下面）
        for bullet in self.bullet_list:
            bullet.move()
            bullet.display()
        # 显示飞船
        self.move()
        globalvar.screen.blit(self.mst_img, (self.x, self.y))

    # 处理移动
    def move(self):
        # 主舰船，处理键盘操作
        if self.type == globalvar.FlightType.MASTER:
            # 键盘事件
            for event in pygame.event.get():
                # pygame 退出标记判断
                if event.type == pygame.QUIT:
                    globalvar.done = True
                elif event.type == KEYDOWN:
                    # 移动
                    if event.key == K_UP or event.key == K_w:
                        self.__mvpic(globalvar.Direction.UP, self.speed)
                    if event.key == K_DOWN or event.key == K_s:
                        self.__mvpic(globalvar.Direction.DOWN, self.speed)
                    if event.key == K_LEFT or event.key == K_a:
                        self.__mvpic(globalvar.Direction.LEFT, self.speed)
                    if event.key == K_RIGHT or event.key == K_d:
                        self.__mvpic(globalvar.Direction.RIGHT, self.speed)
                    # 发射子弹
                    if event.key == K_SPACE:
                        self.__fire()
                    # 重开
                    if event.key == K_r:
                        # 重置主机位置
                        self.x = globalvar.width / 2 - self.width / 2
                        self.y = globalvar.height - self.height * 2
                        # 开始生成
                        globalvar.body_max = globalvar.body_max_bak
                        # 切换 UI
                        globalvar.ui = 'game'
                    # 退出
                    if event.key == K_q or event.key == K_ESCAPE:
                        globalvar.done = True
        elif self.type == globalvar.FlightType.ENEMY:
            info = self.__enemy()
            self.__mvpic(info[0], info[1])

    # 私有方法 --------------------------------------------------------------------

    # 移动主飞船图片
    def __mvpic(self, where, speed):
        # 处理方向
        if where == globalvar.Direction.UP and self.y > 0:
            self.y -= speed
        if where == globalvar.Direction.DOWN and self.y < globalvar.height - self.height:
            self.y += speed
        if where == globalvar.Direction.LEFT and self.x > 0:
            self.x -= speed
        if where == globalvar.Direction.RIGHT and self.x < globalvar.width - self.width:
            self.x += speed

        if globalvar.debug and where != globalvar.Direction.NONE and self.type == globalvar.FlightType.MASTER:
            print("移动", where, " -> [", self.x, ",", self.y, "]")

    # 发射子弹
    def __fire(self):
        bullet = None
        if self.type == globalvar.FlightType.MASTER:
            bullet = Bullet(self.type, self.x + 20, self.y - self.height / 2)
        elif self.type == globalvar.FlightType.ENEMY:
            bullet = Bullet(self.type, self.x + 20, self.y + self.height / 2)
        # 将子弹添加到列表内用于 self.display() 处理显示和移动
        if bullet is not None:
            self.bullet_list.append(bullet)

        if globalvar.debug and self.type == globalvar.FlightType.MASTER:
            print("发射子弹", bullet)

    # 敌人移动/发送逻辑
    def __enemy(self):
        # 敌人发射子弹逻辑
        do_fire = random.randint(0, 90)
        if do_fire == 1:
            self.__fire()
        # return [globalvar.Direction.NONE, 0]  # 禁用移动逻辑
        # TODO 敌人移动逻辑
        do_move = random.randint(0, 3)  # 1/3 的几率决定此次循环是否移动
        if do_move == 1:
            do_what = random.randint(0, 1)  # 选择 x 还是 y 移动
            leg = random.randint(5, 10)  # 随机步长（最大 10）
            if do_what == 0:
                do_what = random.randint(0, 1)
                # 如果是 x， 向着 master 方向移动
                if do_what == 0:
                    if self.x > globalvar.master.x:
                        return [globalvar.Direction.LEFT, leg]
                    else:
                        return [globalvar.Direction.RIGHT, leg]
                else:
                    do_what = random.randint(0, 1)
                    if do_what == 1:
                        return [globalvar.Direction.LEFT, leg]
                    else:
                        return [globalvar.Direction.RIGHT, leg]
            else:
                # 如果是 y， 在 0 - globalvar.height * 2 / 3 （上方 2/3 ） 区域内移动
                # 如果靠近下面就往上，靠近上面就往下
                topheight = globalvar.height * 2 / 3
                if self.y <= topheight / 3:
                    return [globalvar.Direction.DOWN, leg]
                elif self.y >= topheight - topheight / 3:
                    return [globalvar.Direction.UP, leg]
                else:
                    do_what = random.randint(0, 1)
                    if do_what == 0:
                        return [globalvar.Direction.DOWN, leg]
                    else:
                        return [globalvar.Direction.UP, leg]
        # 其他情况，不移动
        return [globalvar.Direction.NONE, 0]


class Bullet:
    x = 0  # 子弹位置
    y = 0
    width = 40  # 子弹大小
    height = 68
    speed = 15 / globalvar.body_max  # 移动速度（慢点，慢点好躲 XD）
    type = None  # 对应的飞船类型

    # 构造方法
    def __init__(self, f_type, x, y):
        self.type = f_type
        # 创建图片（包含透明通道）
        if f_type == globalvar.FlightType.MASTER:
            self.bul_img = pygame.image.load('./images/bm.png').convert_alpha()
        elif f_type == globalvar.FlightType.ENEMY:
            self.bul_img = pygame.image.load('./images/be.png').convert_alpha()
        elif f_type == globalvar.FlightType.BOSS:
            pass
        elif globalvar.debug:
            print("Bullet > __init__ > 飞船类型无效！")
        # 初始化位置
        self.x = x
        self.y = y

    # 显示
    def display(self):
        globalvar.screen.blit(self.bul_img, (self.x, self.y))

    # 移动
    def move(self):
        if self.type == globalvar.FlightType.MASTER:  # 向上飞行
            self.__mvpic(globalvar.Direction.UP)
        elif self.type == globalvar.FlightType.ENEMY or self.type == globalvar.FlightType.BOSS:  # 向下飞行
            self.__mvpic(globalvar.Direction.DOWN)

    # 私有方法 --------------------------------------------------------------------

    def __mvpic(self, to):
        if to == globalvar.Direction.UP:
            self.y -= self.speed
        elif to == globalvar.Direction.DOWN:
            self.y += self.speed
        elif globalvar.debug:
            print("Bullet > __mvpic > 移动方向无效。")
