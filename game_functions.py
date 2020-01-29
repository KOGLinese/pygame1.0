import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien

# 返回一行屏幕可以放多少个外星人
def get_number_aliens_x(ai_settings,alien_width):
    available_space_x = ai_settings.screen_width - alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x

# 放置外星人添加到群组中
def creat_alien(ai_settings,screen,aliens,alien_number,row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)

# 计算得到外星人出现的适合行数
def get_number_rows(ai_settings,ship_height,alien_height):
    available_space_y = (ai_settings.screen_height-(2*alien_height)-ship_height)
    number_rows=int(available_space_y/(2*alien_height))
    return number_rows

# 循环创建外星人
def creat_fleet(ai_settings,screen,ship,aliens):
    alien = Alien(ai_settings,screen)
    number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            creat_alien(ai_settings,screen,aliens,alien_number,row_number)

# 键盘监听事件 键盘按下
def check_keydown_events(event,ai_settings,screen,ship,bullets):
    # 键盘 q 退出系统
    if event.key == pygame.K_q:
        sys.exit()
    # 键盘 右
    if event.key == pygame.K_RIGHT:
        # 向右移动
        ship.moving_right = True

    if event.key == pygame.K_LEFT:
        # 向左移动
        ship.moving_left = True
    # 空格发射子弹
    elif event.key == pygame.K_SPACE :
        fire_bullet(ai_settings,screen,ship,bullets)

def fire_bullet(ai_settings,screen,ship,bullets):
    # 创建一颗子弹,并加入编组bullets中
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

# 键盘松开
def check_keyup_events(event,ship):
    # 松开 右
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    # 松开左
    if event.key == pygame.K_LEFT:
        ship.moving_left = False

# 监听事件
def check_events(ai_settings,screen,ship,bullets):
    """响应按键和鼠标事件"""
    # 监视键盘和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)



def update_screen(ai_settings,screen,ship,aliens,bullets):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时重绘屏幕
    # 填充背景色
    screen.fill(ai_settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # 描绘飞船
    ship.blitme()

    # 将外星人群组放入屏幕
    aliens.draw(screen)

    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings,screen,ship, aliens,bullets):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹位置
    bullets.update()

    # 删除消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # 检查是否有子弹击中了外星人
    # 如果是这样，就删除相应的子弹和外星人
    check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets)


def check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets):
    """响应子弹和外星人的碰撞"""
    # 删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        # 删除现有子弹并更新一群外星人
        bullets.empty()
        creat_fleet(ai_settings, screen, ship, aliens)


# 边界检测
def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break
# 改变舰队方向
def change_fleet_direction(ai_settings,aliens):
    # 所有外星人向下移动
    for alien in aliens.sprites():
        alien.rect.y+=ai_settings.fleet_drop_speed

    ai_settings.fleet_direction *=-1

def update_aliens(ai_settings,stats,screen,ship,aliens,bullets):
    """
    检查是否有外星人位于屏幕边缘，并更新整群外星人的位置
    :param ai_settings:
    :param aliens:
    :return:
    """
    check_fleet_edges(ai_settings,aliens)

    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets)


    aliens.update()
    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,screen,ship,aliens,bullets)

def ship_hit(ai_settings,stats,screen,ship,aliens,bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        # 将飞船生命值减一
        stats.ships_left -= 1

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        creat_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False

def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets):
    """检查是否有外星人达到屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船撞击一样处理
            ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
            break



