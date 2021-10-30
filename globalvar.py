# globalvar.py 全局变量
# 林槐出品，必属稽品 - By Stapx Steve 2021/10/25

from enum import Enum

# 全局设置
width = 600  # 窗口尺寸
height = 700
body_max = 5  # 同屏最大数
debug = True  # 输出调试信息

# 飞机参数
max_n_hp = 20  # 敌人血量
n_hit = 2  # 敌人基础伤害

max_m_hp = 60  # 主机血量
m_hit = 5  # 主机基础伤害

# 全局工作变量
version = "1.4"  # 版本号
body_max_bak = 0  # 同屏最大数备份
screen = None  # 窗口主体
done = False  # 退出标记
master = None  # 主舰船
ui = 'home'  # UI 状态
source = 0  # 分数


# 移动方向枚举常量
class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
    NONE = 5


# 飞机类型枚举常量（数值代表伤害倍数 + 5）
class FlightType(Enum):
    MASTER = 6
    ENEMY = 7
    BOSS = 9  # BOSS 不一定会写

    def __int__(self):
        return self.value


# 物品类型枚举常量
class ItemType(Enum):
    HEALTH = 10
    FIGHT = 11
