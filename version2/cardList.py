import pygame
from gameSprites import *
TYPE_LIST = ("不出","单张","对子","三张","三带一","顺子","炸弹") #-1为非法

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
    def __init__(self,pos):
        super().__init__(HAND_CARDS_POS,1)

    def change_list(self):
        for temp in self.group:
                temp.kill()
        if(self.index_l):
            self.index_l.sort() 
            for i in range(len(self.index_l)): 
                current_pos = (self.pos[0]+self.partition*CARD_SIZE[0]*i,self.pos[1])
                sprite = CardSprite(self.index_l[i],current_pos)
                self.group.add(sprite)
        else:
            #牌出完了，获胜
            print('huosheng')

class GivenCardList(CardList):
    '''出牌的类'''
    def __init__(self,pos):
        super().__init__(pos,0.3)
        self.type = 0 #牌组的类型  
    
    @staticmethod
    def __index_to_point(index):#这一点还可以改进，怎么样可以不用这个方法而直接调类中的内容
        if index == 52: #用这个方法修改大王压小王出问题
            return 13
        elif index == 53:
            return 14
        else:
            return index // 4

    def __judge_type(self):
        if self.index_l:
            if len(self.index_l) == 1:
                return 1
            elif len(self.index_l) == 2:
                if self.__index_to_point(self.index_l[0]) == self.__index_to_point(self.index_l[1]):
                    return 2
                else:
                    return -1
            elif len(self.index_l) == 3:
                if self.__index_to_point(self.index_l[0]) == self.__index_to_point(self.index_l[1]) and self.__index_to_point(self.index_l[1]) == self.__index_to_point(self.index_l[2]):
                    return 3
                else:
                    return -1
            elif len(self.index_l) == 4:
                if self.__index_to_point(self.index_l[0]) == self.__index_to_point(self.index_l[1]) and self.__index_to_point(self.index_l[1]) == self.__index_to_point(self.index_l[2]):
                    if self.__index_to_point(self.index_l[3]) == self.__index_to_point(self.index_l[2]):
                        return 6
                    else:
                        return 4
                else:
                    return -1
            elif len(self.index_l) >= 5:
                for i in range(len(self.index_l)-1):
                    if self.__index_to_point(self.index_l[i+1]) != self.__index_to_point(self.index_l[i]):
                        return -1
                return 5
        else:
            return 0

    def update_list(self, li):
        super().update_list(li)
        self.type = self.__judge_type()

    def compare(self,another):#下面还要定义比较牌组大小的函数
        if self.type < 0: #要先判断是否为非法
                print("您给的牌为非法类型")
                return False
        elif another.type == 0:
                return True 
        elif self.type > 0:
            if self.type != 6 and self.type != another.type:
                print("你给的牌与上家类型不同")
                return False
            else:
                if self.type == 1:
                    if self.__index_to_point(self.index_l[0]) > self.__index_to_point(another.index_l[0]):
                        return True
                    else:         
                        print("您所出的牌没有大过上家")                       
                        return False
                elif self.type == 2:
                    if self.__index_to_point(self.index_l[0]) > self.__index_to_point(another.index_l[0]):
                        return True
                    else:
                        print("您所出的牌没有大过上家") 
                        return False
                elif self.type == 3:
                    if self.__index_to_point(self.index_l[0]) > self.__index_to_point(another.index_l[0]):
                        return True
                    else:
                        print("您所出的牌没有大过上家") 
                        return False
                elif self.type == 4:
                    if self.__index_to_point(self.index_l[0]) > self.__index_to_point(another.index_l[0]):
                        return True
                    else:
                        print("您所出的牌没有大过上家") 
                        return False
                elif self.type == 5:
                    if len(self.index_l) != len(another.index_l):#顺子类型一样也要判断长度
                        print("你给的牌与上家类型不同")
                        return False
                    elif self.__index_to_point(self.index_l[0]) > self.__index_to_point(another.index_l[0]):
                        return True
                    else:
                        print("您所出的牌没有大过上家") 
                        return False
                elif self.type == 6:
                    if self.type == another.type:
                        if self.__index_to_point(self.index_l[0]) > self.__index_to_point(another.index_l[0]):
                            return True
                        else:
                            print("您所出的牌没有大过上家") 
                            return False
                    else:
                        return True 
        elif self.type == 0:
            return True
  

