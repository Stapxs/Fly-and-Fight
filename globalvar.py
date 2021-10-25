# globalvar.py 全局变量
# 林槐出品，必属稽品 - By Stapx Steve 2021/10/25

from enum import Enum

# 全局工作变量

width = 600  # 窗口尺寸
height = 800
screen = None  # 窗口主体
done = False  # 退出标记
debug = True  # 输出调试信息
clock = 0  # 循环计数


# 枚举常量

# 移动方向
class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


# 飞机类型（数值代表伤害倍数）
class FlightType(Enum):
    MASTER = 5
    ENEMY = 6
    BOSS = 9  # BOSS 不一定会写
