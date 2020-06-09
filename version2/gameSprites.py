import pygame
from card import *

#屏幕大小常量
SCREEN_RECT = pygame.Rect(0,0,997,604)
#刷新帧率
FRAME_PER_SEC = 60
#背景图片地址
BGC_IMAGE_NAME = './images/table.png'

            


class GameSprite(pygame.sprite.Sprite):
    '''游戏精灵父类'''
    def __init__(self,image_name):
        #调用父类的init方法
        super().__init__()

        #定义对象属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()

    def update(self):
        pass




class Background(GameSprite):
    '''背景精灵'''
    def __init__(self):
        super().__init__(BGC_IMAGE_NAME)

    def update(self):#是否可以不写直接调用父类方法
        super().update()



class CardSprite(GameSprite):
    '''牌类精灵'''
    def __init__(self,index,x,y):#x,y是牌的位置
        #调用父类方法根据index创建精灵
        self.card = Card(index)
        super().__init__(self.card.pic)
        #设置牌的初始位置
        self.rect.x = x
        self.rect.y = y
    
    def update(self): #所有方法都不要忘记加self参数
        pass