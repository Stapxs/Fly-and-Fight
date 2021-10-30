# controller.py 管理
# 林槐出品，必属稽品 - By Stapx Steve 2021/10/25

import random
import pygame

import articleobj
import globalvar
import ui


def is_intersect(a, b):
    # 第一个矩形：a(x0, y0), a(x1, y1)
    # 第二个矩形：b(x0, y0), b(x1, y1)
    # 相交：max(ax0, bx0) <= min(ax1, bx1) and max(ay0, by0) <= min(ay1, by1)
    if max(a[0][0], b[0][0]) <= min(a[1][0], b[1][0]) and max(a[0][1], b[0][1]) <= min(a[1][1], b[1][1]):
        return True
    return False


class Display:
    # 用于控制显示相关的控制类
    bgImg = './images/bg.jpg'

    bg_height = 1211
    y = -(bg_height - globalvar.height)  # 初始位置

    move_speed = 1

    def displayUI(self):
        self.y += self.move_speed
        if globalvar.body_max > 0:
            self.move_speed = 5
        else:
            self.move_speed = 1
        if self.y >= 0:
            self.y = -(self.bg_height - globalvar.height)

        bg = pygame.image.load(self.bgImg).convert()
        globalvar.screen.blit(bg, (0, self.y))
        # 加载 UI
        # main 主标题页面，只在第一次打开显示          home 主页面
        # died 死亡页面                            game 游戏中页面
        if globalvar.ui == 'home':
            ui.title()  # 主标题
        if globalvar.ui == 'died':
            ui.die_title()  # 死亡标题
        if globalvar.ui == 'game':
            ui.master_hp_line()  # 主机血条
        if globalvar.ui == 'game' or globalvar.ui == 'died':
            ui.score()  # 分数指示
        if (globalvar.ui == 'main' and globalvar.body_max == 0) or globalvar.ui == 'died':
            ui.small_title()  # 控制说明上面的小标题
        if (globalvar.ui == 'main' and globalvar.body_max == 0) or globalvar.ui == 'died' or globalvar.ui == 'home':
            ui.control_note()  # 控制说明


class EnemyCreator:
    # 敌人的相关逻辑
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
                    globalvar.master.bullet_list.remove(bullet)
            half_x = globalvar.master.width / 2
            half_y = globalvar.master.height / 2
            # 主机死亡判定
            for bullet in enemy.bullet_list:
                if globalvar.master.x - half_x <= bullet.x <= globalvar.master.x + half_x and \
                        globalvar.master.y - half_y <= bullet.y <= globalvar.master.y + half_y and \
                        bullet.type == globalvar.FlightType.ENEMY:
                    print("被击中", bullet,
                          "血量：" + str(globalvar.master.hp) + "(" + str(bullet.hit * (int(bullet.type) - 5)) + ")")
                    enemy.bullet_list.remove(bullet)  # 移除子弹
                    globalvar.master.hp -= bullet.hit * (int(bullet.type) - 5)  # 计算伤害
                    globalvar.master.hp_times = 0  # 显示血量
                    if globalvar.master.hp <= 0:  # 判定死亡
                        self.__master_die()
                    return
                # 移除出屏子弹
                if bullet.y < 0 or bullet.y > globalvar.height:
                    globalvar.master.bullet_list.remove(bullet)
            # 撞击死亡判定
            if is_intersect([(enemy.x, enemy.y), (enemy.x + enemy.width, enemy.y + enemy.height)],
                            [(globalvar.master.x, globalvar.master.y),
                             (globalvar.master.x + globalvar.master.width,
                              globalvar.master.y + globalvar.master.height)]):
                self.__master_die()

    # 私有方法 --------------------------------------------------------------------

    def __master_die(self):
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


class ItemCreator:
    # TODO TODO TODO 其他漂浮物件相关逻辑

    # [0] 道具
    tool_item = []

    hp_num = 0

    def create_tools(self):
        if globalvar.body_max > 0:
            if self.hp_num < 1 and globalvar.master.hp < globalvar.max_m_hp / 3:
                do_create = random.randint(0, 25)
                if do_create == 1:
                    self.hp_num += 1
                    enemy = articleobj.Item(globalvar.ItemType.HEALTH, 40, 40)
                    # 添加列表
                    self.tool_item.append(enemy)
        # 清空列表
        if globalvar.body_max <= 0:
            self.tool_item.clear()

    def collision(self):
        # 道具碰撞判定
        for tool in self.tool_item:
            if is_intersect([(tool.x, tool.y), (tool.x + tool.width, tool.y + tool.height)],
                            [(globalvar.master.x, globalvar.master.y), (globalvar.master.x + globalvar.master.width,
                                                                        globalvar.master.y + globalvar.master.height)]):
                self.tool_item.remove(tool)
                tool.operate()
                self.hp_num -= 1
