import pygame
from gameSprites import *

class Game(object):
    '''主游戏'''
    def __init__(self):
        #1.创建游戏主窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)

        #2.创建游戏时钟
        self.clock = pygame.time.Clock()

        #3.#创建背景精灵及精灵组
        #目前还是先创建所有精灵
        bg = Background()
        #创建四个牌组
        self.back_group = pygame.sprite.Group(bg)
        self.hand_card_group = pygame.sprite.Group()
        self.given_card_group = pygame.sprite.Group()
        self.last_card_group = pygame.sprite.Group()
        self.next_card_group = pygame.sprite.Group()
        #牌的其他特性
        self.hand_card_list = [11,2,1,10,11,13,11,12,3,4,5,6,7,8,2,9,8]#调试用，利用循环创建


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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#不写这个打右上角的x关不掉
                self.__game_over()
            #判断是否被鼠标点击出牌
            elif (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]):
                for card_sprite in self.hand_card_group:
                    card_sprite.mouse_click(pygame.mouse.get_pos())
            #出牌
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                self.__give_cards()
            #接受发牌
            


    def __update_sprites(self):
        #self.back_group.update()
        self.back_group.draw(self.screen)
        #self.card_group.update()
        self.hand_card_group.draw(self.screen)
        self.given_card_group.draw(self.screen)

    @staticmethod
    def __game_over():#为什么要用静态方法
        print("游戏结束")
        pygame.quit()
        exit()

    def start_game(self):
        print("游戏开始")
        self.__create_card_sprites(self.hand_card_list,self.hand_card_group,HAND_CARDS_POS)
        while True:#这里可以要用多线程设计，让发牌和主循环分开
            #1.设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            #2.监听事件，可将通信加入这个
            self.__event_handler()
            #4.更新/绘制精灵组
            self.__update_sprites()
            #5.更新显示
            pygame.display.update()


def test():
    game = Game()
    game.start_game()

test()