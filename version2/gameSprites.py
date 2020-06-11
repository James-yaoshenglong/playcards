import pygame
from card import *

#屏幕大小常量
SCREEN_RECT = pygame.Rect(0,0,997,604)
#刷新帧率
FRAME_PER_SEC = 60
#背景图片地址
BGC_IMAGE_NAME = './images/table.png'
#牌图片的大小
CARD_SIZE = (56,98)
#这些位置目前还没有实现居中对齐
#手牌位置
HAND_CARDS_POS = (10,SCREEN_RECT.bottom-CARD_SIZE[1]-10)
#出牌位置 
GIVEN_CARDS_POS = (200,SCREEN_RECT.bottom-2*CARD_SIZE[1]-20)
#上家位置
LAST_CARDS_POS = (10,SCREEN_RECT.centery-CARD_SIZE[1])
#下家位置   
NEXT_CARDS_POS = (SCREEN_RECT.right-10-CARD_SIZE[0],SCREEN_RECT.centery-CARD_SIZE[1])

class GameSprite(pygame.sprite.Sprite):
    '''游戏精灵父类'''
    def __init__(self,image_name):
        #调用父类的init方法
        super().__init__()
        #定义对象属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()



class Background(GameSprite):
    '''背景精灵'''
    def __init__(self):
        super().__init__(BGC_IMAGE_NAME)



class CardSprite(GameSprite):
    '''牌类精灵'''
    def __init__(self,index,pos):#x,y是牌的位置
        #调用父类方法根据index创建精灵
        self.card = Card(index)
        super().__init__(self.card.pic)
        #设置牌的初始位置
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.given = False #判断是否被选中要出
    

    def mouse_click(self,mouse_pos):#目前无法实现堆叠状况的正确点击
        if(mouse_pos[0]>self.rect.left and  mouse_pos[0]<self.rect.right and mouse_pos[1]<self.rect.bottom and mouse_pos[1]>self.rect.top):#判断点击的位置是否在牌的中间
            self.given = not self.given
            if(self.given):
                self.rect.y -= 20
            else:
                self.rect.y += 20
        