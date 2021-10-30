# main.py 主函数
# 林槐出品，必属稽品 - By Stapx Steve 2021/10/25

import pygame

import articleobj
import controller
import globalvar

enemies = controller.EnemyCreator()
items = controller.ItemCreator()
uic = controller.Display()


def run():
    # 主运行流程
    uic.displayUI()  # 刷新界面
    globalvar.master.display()  # 刷新主飞船（同时也会刷新此飞船所属的子弹）

    enemies.create()  # 创建敌人
    for enemy in enemies.enemy_list:  # 刷新敌人（同时也会刷新此飞船所属的子弹）
        enemy.display()

    items.collision()  # 物品碰撞判定
    items.create_tools()  # 创建道具物品
    for item in items.tool_item:  # 刷新道具物品（包含移动）
        item.display()

    pygame.time.wait(10)  # 循环延时
    pygame.display.update()  # 刷新窗口

    enemies.collision()  # 死亡判定


if __name__ == "__main__":

    # 初始化窗口
    pygame.init()
    globalvar.screen = pygame.display.set_mode((globalvar.width, globalvar.height), 0, 32)
    pygame.display.set_caption('Fly&Fight!')

    # 初始化基础
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
