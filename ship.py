import  pygame

class Ship():
    def __init__(self,ai_settings,screen):
        #初始化飞船以及位置
        self.screen=screen
        self.ai_settings = ai_settings
        #加载飞机图像兵截取其外接矩形
        self.image = pygame.image.load('image/PaperPlane.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #将每艘飞机放在屏幕中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)
        #移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标志调整飞船位置"""
        # 更新飞船center值
        if self.moving_right and self.rect.centerx < self.screen_rect.right:
            self.rect.centerx += self.ai_settings.ship_speed_factor
            #self.rect.centerx += 1
        if self.moving_left and self.rect.centerx > 0:
            self.rect.centerx -= self.ai_settings.ship_speed_factor
            #self.rect.centerx -= 1
        #print(self.center)
        #根据self.center更新rect对象
        #self.rect.centerx = self.center
        self.center = self.rect.centerx

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image,self.rect)