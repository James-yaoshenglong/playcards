import socket
import threading
import math
import random
import pickle
import time
#注意引用的问题
# palyers_cards = [[],[],[]]

# def login():





def deal(palyers_cards):
        colors = ("黑桃", "草花", "红桃", "方片", "王牌")
        points = ("3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A", "2", "小王", "大王")
        #洗牌函数，可以用取一次random，将其从序列里删去，再重新去取
        card_indexs = [x for x in range(54)]
        random.shuffle(card_indexs)  #是直接作用，不是返回
        deal_index = random.randint(0,2)
        for index in card_indexs:
                palyers_cards[deal_index].append(index)
                deal_index+=1
                deal_index = deal_index%3

# pickle.dumps()将数据序列化为二进制
# pickle.loads()将数据复原


def broadcast(players,give_index):
        #由于服务器端在客户端连接之后执行速度比客户端快，所以两次发送被一次接受了
        #所以使用time.sleep
        while True:
                time.sleep(0.1)
                give_index[0] +=1 
                give_index[0] = give_index[0]%3
                for i in range(len(players)):
                        players[i].send(pickle.dumps([i,give_index[0]]))
                user_give_cards = pickle.loads(players[give_index[0]].recv(1024))
                for i in range(len(players)):
                        players[i].send(pickle.dumps(user_give_cards))



def dunch_offical(players):
        palyers_cards = [[],[],[]]
        deal(palyers_cards)
        for i in range(len(players)):
                players[i].send(pickle.dumps(palyers_cards[i]))
        give_index = [random.randint(0,2)]
        broadcast(players,give_index)
        data = pickle.loads(players[0].recv(1024))
        print(data)





def main():
        #接受用户登陆，注意记录用户的登陆信息（积分系统）
        tables = []
        server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_socket.bind(('',8888))
        server_socket.listen(128)
        print("服务器开始工作")
        population_on_a_table = 0
        table_number = 0
        while True:
                client_socket, client_addr = server_socket.accept()
                print("接受到一个用户登陆")
                population_on_a_table += 1
                population_on_a_table = population_on_a_table%3
                if population_on_a_table==1:
                        table_number +=1
                        tables.append([client_socket])
                elif population_on_a_table==0:
                        tables[table_number-1].append(client_socket)
                        t = threading.Thread(target=dunch_offical,args=(tables[table_number-1],))
                        t.start()
                        print("{}号桌已经开桌".format(str(table_number)))
                else:
                        tables[table_number-1].append(client_socket)
        #发牌，留三张
        deal()
        client_socket.send(pickle.dumps(palyers_cards[1]))
        #随机指定叫地主的人并且叫一轮地主
        #从地主开始出牌，判断出牌是否合理，并且广播出牌（可以添加计时器）
        #下家出牌，比较大小
        #到再次轮到出牌者的时候，注意是按大小轮到，还是上两家都没有轮到
        #判断游戏是否结束，并进行积分


if __name__ == "__main__":
        main()
