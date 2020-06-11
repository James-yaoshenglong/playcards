import socket
import pickle
import threading
from queue import Queue
from card import *

q = Queue(5)

class Network(threading.Thread):
    def __init__(self):
        super().__init__()
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client_socket.connect(("127.0.0.1",8888))
        #这个服务器IP地址目前为本机IP以供调试，实际使用时connect学校服务器的IP可以供广域网使用
        self.palyers_cards = []
        self.current_cards = []



    def give_cards(self,my_give_cards):
        self.client_socket.send(pickle.dumps(my_give_cards))




    def run(self):
        #这一段改为start中的第一段，返回一个
        recv_data = pickle.loads(self.client_socket.recv(1024))
        # index_to_string(recv_data,palyers_cards)
        # print("您的手牌为：")
        # display(palyers_cards)
        #这一段改为主体运行部分
        q.put(['hand_card',recv_data])
        while True:
                indexs = pickle.loads(self.client_socket.recv(1024))
                q.put(['giver_index',indexs])
                # if indexs[0] == indexs[1]:
                #         print("你的序号为{}，当前出牌者为{}".format(str(indexs[0]),str(indexs[1])))
                #         q.put([,])
                #         self.given_success = False
                #         #这里在主线程中等待出牌并调用出牌函数
                # else:
                #         print("你的序号为{}，当前出牌者为{}".format(str(indexs[0]),str(indexs[1])))
                #         print("请等待{}出牌".format(str(indexs[1])))
                #         self.your_give = False
                user_give_cards = pickle.loads(self.client_socket.recv(1024))
                q.put(['current_card',user_give_cards])
                # if user_give_cards[0] == -1:
                #         print("{}获胜，游戏结束".format(str((indexs[1]+2)%3))
                #         break
                # #因为在index_to_string函数中采用了append方法，所以此处要先clear
                # #也可以通过这种方法是实现计牌器和牌池
                # if user_give_cards:
                #         #这里改为在主线程中显示对应的current_card
                #         current_cards = user_give_cards
                #         # index_to_string(user_give_cards,current_cards)
                #         # print("{}的出牌为：".format(str(indexs[1])))
                #         # display(current_cards)
                # else:
                #         #这里为不出的情况，不显示牌
                #         give_none_time+=1
                #         print("{}的出牌为：不出".format(str(indexs[1])))
                #         if give_none_time ==2:
                #                 give_none_time = 0
                #                 current_cards.clear()
                # if not(palyers_cards):
                #         print("您获胜，游戏结束")
                #         client_socket.send(pickle.dumps([-1]))
                #         break