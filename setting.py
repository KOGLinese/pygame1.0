class Settings():
    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        # 屏幕背景颜色
        self.bg_color = (253, 253, 254)

        # 各种移动速度
        self.ship_speed_factor = 2
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        # fleet_direction 1右移 -1 左移
        self.fleet_direction = 1

        # 子弹设置
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 5
