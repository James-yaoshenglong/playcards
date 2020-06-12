import pygame
from gameSprites import *
from cardList import *
from networkClient import *

test_list = [17,1,2,3,11,16]

class Game(object):
    '''主游戏'''
    def __init__(self):
        #1.创建游戏主窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        #2.创建游戏时钟
        self.clock = pygame.time.Clock()
        #3.创建背景精灵及精灵组
        bg = Background()
        self.back_group = pygame.sprite.Group(bg)
        #4.创建四个牌组,以空链表初始化
        self.hand_card= HandCardList(HAND_CARDS_POS)
        self.current_card = GivenCardList((-100,-100))
        self.given_card = GivenCardList(GIVEN_CARDS_POS)
        self.last_card = GivenCardList(LAST_CARDS_POS)
        self.next_card = GivenCardList(NEXT_CARDS_POS)
        #5.设置事件标记
        self.can_give = False
        self.current_giver = 0
        self.your_giver = 0
        self.give_none_time = 0
        #6.创建network类
        self.network = Network()


    def __create_card_sprites(self,card_list,card_group,pos):
    #根据数组更新一个牌类精灵组
        #删除group中所有精灵，这种办法效率比较低，但是排序有保证
        for temp in card_group:
            temp.kill()
        for i in range(len(card_list)):
            card_sprite = CardSprite(card_list[i],pos[0]+i*CARD_SIZE[0],pos[1])
            card_group.add(card_sprite)
         

    #下面还要写出牌的函数
    def __give_cards(self):
        temp_index_list = []
        for sprite in self.hand_card.group:
            if sprite.given:
                temp_index_list.append(sprite.card.index)
        temp_card = GivenCardList(GIVEN_CARDS_POS)
        temp_card.update_list(temp_index_list)
        if temp_card.compare(self.current_card):
            #这里调用network类的方法进行发送
            if not temp_index_list:
                if not self.current_card.index_l: #这里要用current card来判断而不能用give_none_times
                    print("请您任意出至少一张牌：")
                    print("请重新出牌：")
                else:
                    self.network.give_cards(temp_index_list)
                    self.can_give = False
            else:
                self.can_give = False
                self.network.give_cards(temp_index_list)
                for index in temp_index_list:
                    self.hand_card.index_l.remove(index)
                self.hand_card.change_list()
        else :
            self.can_give = True
            print("请重新出牌：")
        if not self.hand_card.index_l:#判断是否获胜
            self.network.give_cards([-1])
            self.__game_over()
            
        

    def __event_handler(self):
        #事件处理函数，负责处理动画和接受发送消息
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #不写这个打右上角的x关不掉
                self.__game_over()
            #判断是否被鼠标点击出牌
            elif (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]):
                for card_sprite in self.hand_card.group:
                    card_sprite.mouse_click(pygame.mouse.get_pos())
            #出牌
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.can_give):
                self.__give_cards()
            

    def __update_status(self):
        #更新背景
        self.back_group.draw(self.screen)
        #更新牌组
        self.hand_card.group.draw(self.screen)
        self.given_card.group.draw(self.screen)
        self.last_card.group.draw(self.screen)
        self.next_card.group.draw(self.screen)
        #更新来自网络模块的信息
        if not q.empty():
            info = q.get()
            if info[0] == 'hand_card':
                self.hand_card.update_list(info[1])
            elif info[0] == 'giver_index':
                self.your_giver = info[1][0]
                self.current_giver = info[1][1]
                if self.your_giver == self.current_giver:
                    self.can_give = True
            elif info[0] == 'current_card':
                if info[1]:
                    if info[1][0] == -1:# 判断游戏结束
                        self.__game_over()
                    else:
                        self.current_card.update_list(info[1])
                else:
                    self.give_none_time+=1
                    if self.give_none_time == 2:
                        self.give_none_time = 0
                        self.current_card.update_list([])
                #更新显示
                if(self.current_giver == (self.your_giver+1)%3):
                    self.next_card.update_list(info[1])
                elif (self.current_giver == self.your_giver):
                    self.given_card.update_list(info[1])
                else:
                    self.last_card.update_list(info[1])

    


    @staticmethod
    def __game_over():#为什么要用静态方法,不用self的时候
        print("游戏结束")
        pygame.quit()
        exit()

    def start_game(self):
        print("游戏开始")
        self.network.start() #这里要用多线程设计，让发牌和主循环分开
        while True:
            #1.设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            #2.监听事件，可将通信加入这个
            self.__event_handler()
            #3.更新各个参数
            self.__update_status()
            #4.更新显示
            pygame.display.update()

