
import sys
import pygame
from setting import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien

def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()

    ai_settings = Settings()

    # 设置窗口大小，返回游戏窗口对象
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height))

    # 窗口名称
    pygame.display.set_caption("Alien Invasion")

    # 创建飞船
    ship =Ship(ai_settings,screen)
    # 创建一个用于存储子弹的编组，
    bullets = Group()
    # 外星人编组
    aliens = Group()
    # 创建外星人群
    gf.creat_fleet(ai_settings,screen,ship,aliens)
    # 开始游戏的主循环
    while(True):
        gf.check_events(ai_settings,screen,ship,bullets)
        ship.update()
        gf.update_bullets(aliens,bullets)

        gf.update_aliens(ai_settings,aliens)
        gf.update_screen(ai_settings,screen,ship,aliens,bullets)


run_game()