# articleobj.py 对象
# 林槐出品，必属稽品 - By Stapx Steve 2021/10/25

import pygame

from pygame import *

import globalvar


class Master:
    img = './images/master.png'
    mst_img = None

    x = 0  # 飞船位置
    y = 0
    width = 76  # 飞船大小
    height = 61

    speed = 20  # 移送速度

    bullet_list = []  # 子弹列表

    # 构造函数
    def __init__(self):
        # 创建主飞船图片（包含透明通道）
        self.mst_img = pygame.image.load(self.img).convert_alpha()
        # 居中底部
        # globalvar.screen.blit(mst_img, (0, random.randint(0, globalvar.width)))
        self.x = globalvar.width / 2 - self.width / 2
        self.y = globalvar.height - self.height * 2

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
                # 退出
                if event.key == K_q or event.key == K_ESCAPE:
                    globalvar.done = True

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

        if globalvar.debug:
            print("移动", where, " -> [", self.x, ",", self.y, "]")

    # 发射子弹
    def __fire(self):
        bullet = Bullet(self.x + 20, self.y - self.height / 2)
        # 将子弹添加到列表内用于 self.display() 处理显示和移动
        self.bullet_list.append(bullet)

        if globalvar.debug:
            print("发射子弹", bullet)


class Bullet:
    img = './images/bm.png'
    bul_img = None

    x = 0  # 子弹位置
    y = 0
    width = 40  # 子弹大小
    height = 68
    speed = 20  # 移动速度（保持和飞船移动速度相同的话应该比较好躲 XD）

    # 子弹对应飞机类型（这会影响到使用的贴图和飞行方向）
    type = globalvar.FlightType.MASTER

    # 构造方法
    def __init__(self, x, y):
        # 创建图片（包含透明通道）
        self.bul_img = pygame.image.load(self.img).convert_alpha()
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
