import socket
import pickle
import threading
from queue import Queue
from card import *

q = Queue(5)

class Network(threading.Thread):
    def __init__(self,):
        super().__init__()
        self.setDaemon = True #设置这个线程为守护线程，使主线程结束时该线程也结束,这个问题还未解决
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client_socket.connect(("127.0.0.1",8888))
        #这个服务器IP地址目前为本机IP以供调试，实际使用时connect学校服务器的IP可以供广域网使用



    def give_cards(self,my_give_cards):
        self.client_socket.send(pickle.dumps(my_give_cards))


    def run(self):
        #接受发牌
        recv_data = pickle.loads(self.client_socket.recv(1024))
        q.put(['hand_card',recv_data])
        #主体游戏通信
        while True:
                indexs = pickle.loads(self.client_socket.recv(1024))
                q.put(['giver_index',indexs])
                user_give_cards = pickle.loads(self.client_socket.recv(1024))
                q.put(['current_card',user_give_cards])
                