import socket
import pickle

colors = ("黑桃", "草花", "红桃", "方片", "王牌")
#为实现单个字符，10用0 替代，大代替大王，小代替小王,不出为1
points = ("3", "4", "5", "6", "7", "8", "9", "0", "J", "Q", "K", "A", "2", "小", "大")


def sort(palyers_cards):
    #牌组排序
        for i in range(len(palyers_cards)):
                for j in range (len(palyers_cards)-i-1):
                        if palyers_cards[j][1]<palyers_cards[j+1][1]:
                                palyers_cards[j],palyers_cards[j+1] = palyers_cards[j+1],palyers_cards[j]


def index_to_string(client_cards,palyers_cards):
        for index in client_cards:
                if index == 52:
                        palyers_cards.append([4, 13,index])
                elif index == 53:
                        palyers_cards.append([4, 14,index])
                else: 
                        palyers_cards.append([index%4,index%13,index])
        sort(palyers_cards)

def display(palyers_cards):
    #显示牌组
        s1 = ""
        s2 = ""
        for card in palyers_cards:
            #打印花色和牌面
                # s1 += colors[card[0]]
                # s2 += "{:<4s}".format(points[card[1]])
                s2 += points[card[1]]+" "
        # print(s1)
        print(s2)


def judge(give_list,current_cards):
        if not(current_cards):
                return True 
        elif  current_cards[0][1]<give_list[0]:
                return True
        else:
                return False


def string_to_index(my_give_cards,palyers_cards,current_cards):
        give_list = []
        for char in my_give_cards:
                before_len = len(give_list)
                for i in range(len(points)):
                        if char == points[i]:
                                give_list.append(i)
                current_len = len(give_list)
                if before_len == current_len:
                    print("输入的{}为非法字符".format(char))
                    return False                    
        give_index_list = []
        for temp in give_list:
                before_len = len(give_index_list)
                for i in range(len(palyers_cards)):
                        if temp == palyers_cards[i][1]:
                                if not(palyers_cards[i][2] in give_index_list):
                                        give_index_list.append(palyers_cards[i][2])
                                        break
                current_len = len(give_index_list)
                if before_len == current_len:
                    print("输入的{}不是您所持有的牌".format(char))
                    return   False  
        if judge(give_list,current_cards):
                return give_index_list
        else:
                print("您所出的牌没有大过上家")
                return False


def give_cards(palyers_cards,client_socket,current_cards):
        my_give_cards = input("请出牌：")
        while True:
                if my_give_cards == "1": 
                        if current_cards:
                                client_socket.send(pickle.dumps([]))
                                break
                        else:
                                print("请您任意出至少一张牌：")
                                my_give_cards = input("请重新出牌：")
                else:
                        give_index_list = string_to_index(my_give_cards,palyers_cards,current_cards)
                        if give_index_list:
                                for index in give_index_list:
                                        for i in range(len(palyers_cards)):
                                                if palyers_cards[i][2] == index:
                                                        del palyers_cards[i]
                                                        break
                                client_socket.send(pickle.dumps(give_index_list))
                                print("您出牌后的手牌为：")
                                display(palyers_cards)        
                                break
                        else:
                                my_give_cards = input("请重新出牌：")

def recieve(client_socket,palyers_cards,current_cards):
        give_none_time = 0
        while True:
                indexs = pickle.loads(client_socket.recv(1024))
                if indexs[0] == indexs[1]:
                        print("你的序号为{}，当前出牌者为{}".format(str(indexs[0]),str(indexs[1])))
                        give_cards(palyers_cards,client_socket,current_cards)
                else:
                        print("你的序号为{}，当前出牌者为{}".format(str(indexs[0]),str(indexs[1])))
                        print("请等待{}出牌".format(str(indexs[1])))
                user_give_cards = pickle.loads(client_socket.recv(1024))
                #因为在index_to_string函数中采用了append方法，所以此处要先clear
                #也可以通过这种方法是实现计牌器和牌池
                if user_give_cards:
                        current_cards.clear()
                        index_to_string(user_give_cards,current_cards)
                        print("{}的出牌为：".format(str(indexs[1])))
                        display(current_cards)
                else:
                        give_none_time+=1
                        print("{}的出牌为：不出".format(str(indexs[1])))
                        if give_none_time ==2:
                                give_none_time = 0
                                current_cards.clear()

def main():
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client_socket.connect(("127.0.0.1",8888))
        palyers_cards = []
        recv_data = pickle.loads(client_socket.recv(1024))
        index_to_string(recv_data,palyers_cards)
        print("您的手牌为：")
        display(palyers_cards)
        current_cards = []
        recieve(client_socket,palyers_cards,current_cards)


if __name__ == "__main__":
    main()





# 剩余judge函数和异常退出程序未写