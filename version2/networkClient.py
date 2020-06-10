import socket
import pickle
from card import *

class Network(object):
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client_socket.connect(("127.0.0.1",8888))
        #这个服务器IP地址目前为本机IP以供调试，实际使用时connect学校服务器的IP可以供广域网使用
        self.palyers_cards = []
        self.current_cards = []
        self.your_give = False
        self.given_success = False

    def start(self):
        #这一段改为start中的第一段，返回一个
        recv_data = pickle.loads(client_socket.recv(1024))
        index_to_string(recv_data,palyers_cards)
        print("您的手牌为：")
        display(palyers_cards)




    def give_cards(self,my_give_cards):
            if not my_give_cards: 
                    if current_cards:
                            self.client_socket.send(pickle.dumps(my_give_cards))
                            self.given_success = True
                            self.your_give = False
                    else:
                            print("请您任意出至少一张牌：")
                            print("请重新出牌：")
                            self.given_success = False
            else:
                        #目前这里还缺将之前的juge那一块搞过来
                            self.client_socket.send(pickle.dumps(my_give_cards))
                            print("您出牌后的手牌为：")
                            display(palyers_cards)        
                            self.given_success = True
                            self.your_give = False









    def run(self):
        #这一段改为主体运行部分
        give_none_time = 0
        while True:
                indexs = pickle.loads(self.client_socket.recv(1024))
                if indexs[0] == indexs[1]:
                        print("你的序号为{}，当前出牌者为{}".format(str(indexs[0]),str(indexs[1])))
                        self.your_give = True
                        self.given_success = False
                        #这里在主线程中等待出牌并调用出牌函数
                else:
                        print("你的序号为{}，当前出牌者为{}".format(str(indexs[0]),str(indexs[1])))
                        print("请等待{}出牌".format(str(indexs[1])))
                        self.your_give = False
                user_give_cards = pickle.loads(client_socket.recv(1024))
                if user_give_cards[0] == -1:
                        print("{}获胜，游戏结束".format(str((indexs[1]+2)%3))
                        break
                #因为在index_to_string函数中采用了append方法，所以此处要先clear
                #也可以通过这种方法是实现计牌器和牌池
                if user_give_cards:
                        #这里改为在主线程中显示对应的current_card
                        current_cards = user_give_cards
                        # index_to_string(user_give_cards,current_cards)
                        # print("{}的出牌为：".format(str(indexs[1])))
                        # display(current_cards)
                else:
                        #这里为不出的情况，不显示牌
                        give_none_time+=1
                        print("{}的出牌为：不出".format(str(indexs[1])))
                        if give_none_time ==2:
                                give_none_time = 0
                                current_cards.clear()
                if not(palyers_cards):
                        print("您获胜，游戏结束")
                        client_socket.send(pickle.dumps([-1]))
                        break