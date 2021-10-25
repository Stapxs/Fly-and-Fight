# main.py 主函数
# 林槐出品，必属稽品 - By Stapx Steve 2021/10/25

import pygame

import articleobj
import controller
import globalvar

bgImg = './images/bg.jpg'

enemies = controller.EnemyCreator()


def run():
    # TODO 多倍数循环
    # clock 参数为 循环计数
    # 这玩意是打算用来处理一些需要 N 个循环执行一次的操作
    # * 不一定会写
    # globalvar.clock += 1
    # 主运行流程
    # 每个循环都需要执行的部分
    controller.Bg().loadBg()  # 刷新背景
    globalvar.master.display()  # 刷新主飞船（同时也会刷新此飞船所属的子弹）

    enemies.create()  # 创建敌人
    for enemy in enemies.enemy_list:  # 刷新敌人（同时也会刷新此飞船所属的子弹）
        enemy.display()

    pygame.display.update()  # 刷新窗口

    enemies.collision()  # 死亡判定


if __name__ == "__main__":

    # 初始化窗口
    pygame.init()
    globalvar.screen = pygame.display.set_mode((globalvar.width, globalvar.height), 0, 32)
    pygame.display.set_caption('Fly&Fight!')

    # 初始化基础
    controller.Bg().loadBg()  # 初始化背景
    globalvar.master = articleobj.Flight(globalvar.FlightType.MASTER)  # 创建主飞船
    globalvar.body_max_bak = globalvar.body_max  # 开始暂停
    globalvar.body_max = 0

    # 等待循环结束
    while not globalvar.done:
        for event in pygame.event.get():
            # pygame 退出标记判断
            if event.type == pygame.QUIT:
                globalvar.done = True
        # 主流程
        run()

    pygame.quit()
