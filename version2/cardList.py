import pygame
from gameSprites import *

class CardList(object):
    '''牌组类'''
    def __init__(self, pos , partition):
        self.index_l = []
        self.group = pygame.sprite.Group() #牌类精灵组
        self.partition = partition #间隔占比
        self.pos = pos #起始位置元组

    def update_list(self, li):
        #清空精灵组和列表
        if(self.index_l):
            for temp in self.group:
                temp.kill()
            self.index_l.clear()
        if(li):
            li.sort() #排序，sort不用赋值
            for i in range(len(li)): 
                self.index_l.append(li[i])
                current_pos = (self.pos[0]+self.partition*CARD_SIZE[0]*i,self.pos[1])
                sprite = CardSprite(li[i],current_pos)
                self.group.add(sprite)

class HandCardList(CardList):
    '''手牌类'''
    def __init__(self):
        super().__init__(HAND_CARDS_POS,1)

    #下面还要写出牌的函数
    def give_cards(self):
        pass

class GivenCardList(CardList):
    '''出牌的类'''
    def __init__(self,pos):
        super().__init__(pos,0.3)  

    #下面还要定义比较牌组大小的函数  

