import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """对飞船发射的子弹进行管理"""

    def __init__(self,ai_settings,screen,ship):
        """在飞船位置创建一个子弹对象"""
        super(Bullet, self).__init__()
        self.screen =screen

        # 在（0，0）处创建一个表示子弹的矩形，再设置正确的位置
        self.rect=pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)
        # 将子弹初始化位置到飞船矩形的中间和顶部
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # 存储用于表示子弹的位置
        self.y=float(self.rect.y)
        # 子弹颜色，移动速度
        self.color=ai_settings.bullet_color
        self.speed_factor=ai_settings.bullet_speed_factor

    def update(self):
        """向上移动子弹"""
        self.y-=self.speed_factor
        self.rect.y=self.y

    def draw_bullet(self):
        """屏幕绘制子弹"""
        pygame.draw.rect(self.screen,self.color,self.rect)