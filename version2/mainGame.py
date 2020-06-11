import pygame
from gameSprites import *
from cardList import *

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
        self.hand_card= HandCardList()
        self.given_card = GivenCardList(GIVEN_CARDS_POS)
        self.last_card = GivenCardList(LAST_CARDS_POS)
        self.next_card = GivenCardList(NEXT_CARDS_POS)
        #5.设置事件标记
        self.can_give = False
        self.receive_hand = True
        self.receive_given = False
        self.current_giver = 0
        self.your_giver = 0



    def __create_card_sprites(self,card_list,card_group,pos):
    #根据数组更新一个牌类精灵组
        #删除group中所有精灵，这种办法效率比较低，但是排序有保证
        for temp in card_group:
            temp.kill()
        for i in range(len(card_list)):
            card_sprite = CardSprite(card_list[i],pos[0]+i*CARD_SIZE[0],pos[1])
            card_group.add(card_sprite)
         

    def __give_cards(self):
        give_list = []
        for temp in self.hand_card_group: #group不能用index
            if(temp.given):
                give_list.append(temp.card.index)
                self.hand_card_list.remove(temp.card.index)
        self.__create_card_sprites(give_list,self.given_card_group,GIVEN_CARDS_POS)
        self.__create_card_sprites(self.hand_card_list,self.hand_card_group,HAND_CARDS_POS)
                
            
        


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
                self.hand_card.give_cards()
        #接受发牌
        if(self.receive_given):
            if(self.current_giver == (self.your_giver+1)%2):
                self.next_card.update_list(test_list)
            elif (self.current_giver == self.your_giver):
                self.given_card.update_list(test_list)
            else:
                self.last_card.update_list(test_list)
        elif(self.receive_hand):
            print("jieshoufapai")
            self.hand_card.update_list(test_list)#目前先测试
            self.receive_hand = False
            


    def __update_status(self):
        #更新背景
        self.back_group.draw(self.screen)
        #更新牌组
        self.hand_card.group.draw(self.screen)
        self.given_card.group.draw(self.screen)
        self.last_card.group.draw(self.screen)
        self.next_card.group.draw(self.screen)
        #更新来自网络模块的信息
    


    @staticmethod
    def __game_over():#为什么要用静态方法
        print("游戏结束")
        pygame.quit()
        exit()

    def start_game(self):
        print("游戏开始")
        while True:#这里可以要用多线程设计，让发牌和主循环分开
            #1.设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            #2.监听事件，可将通信加入这个
            self.__event_handler()
            #3.更新/绘制精灵组
            self.__update_status()
            #4.更新显示
            pygame.display.update()


def test():
    game = Game()
    game.start_game()

test()