import pygame
from gameSprites import *

class Game(object):
    '''主游戏'''
    def __init__(self):
        #1.创建游戏主窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)

        #2.创建游戏时钟
        self.clock = pygame.time.Clock()

        #3.调用私有方法，创建精灵和精灵组
        self.__create_sprites()

    def __create_sprites(self):
    #创建背景精灵及精灵组
        bg = Background()
        self.back_group = pygame.sprite.Group(bg)
    #创建牌类精灵及精灵组
        self.card_group = pygame.sprite.Group()
        l = [11,11,11,11,11,11,11,11]#调试用，利用循环创建
        for i in range(len(l)):
            card_sprite = CardSprite(l[i],10+54*i,SCREEN_RECT.bottom-100)
            self.card_group.add(card_sprite)
         


    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#不写这个打右上角的x关不掉
                self.__game_over()


    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)
        self.card_group.update()
        self.card_group.draw(self.screen)

    @staticmethod
    def __game_over():#为什么要用静态方法
        print("游戏结束")
        pygame.quit()
        exit()

    def start_game(self):
        print("游戏开始")
        while True:
            #1.设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            #2.监听事件
            self.__event_handler()
            #4.更新/绘制精灵组
            self.__update_sprites()
            #5.更新显示
            pygame.display.update()


def test():
    game = Game()
    game.start_game()

test()