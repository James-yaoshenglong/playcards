import socket
import pickle

colors = ("黑桃", "草花", "红桃", "方片", "王牌")
#为实现单个字符，10用0 替代，大代替大王，小代替小王,不出为1
points = ("3", "4", "5", "6", "7", "8", "9", "0", "J", "Q", "K", "A", "2", "小", "大")
typeList = ("非法","单张","对子","三张","三带一","顺子","炸弹")


class CARD():
    def __init__(self,index):
        if index == 52:
            self.index = index
            self.color = 4
            self.point = 13
        elif index == 53:
            self.index = index
            self.color = 4
            self.point = 14
        else:
            self.index = index
            self.color = self.index % 4
            self.point = self.index % 13




def sort(palyers_cards):
    #牌组排序
        for i in range(len(palyers_cards)):
                for j in range (len(palyers_cards)-i-1):
                        if palyers_cards[j].point<palyers_cards[j+1].point:
                                palyers_cards[j],palyers_cards[j+1] = palyers_cards[j+1],palyers_cards[j]


def index_to_string(client_cards,palyers_cards):
        for index in client_cards:
                palyers_cards.append(CARD(index))
        sort(palyers_cards)

def display(palyers_cards):
    #显示牌组
        # s1 = ""
        s2 = ""
        for card in palyers_cards:
            #打印花色和牌面
                # s1 += colors[card[0]]
                # s2 += "{:<4s}".format(points[card[1]])
                s2 += points[card.point]+" "
        # print(s1)
        print(s2)


def judgeType(current_list):
    if len(current_list) == 1:
        return 1
    elif len(current_list) == 2:
        if current_list[0] == current_list[1]:
            return 2
        else:
            return 0
    elif len(current_list) == 3:
        if current_list[0] == current_list[1] and current_list[1] == current_list[2]:
            return 3
        else:
            return 0
    elif len(current_list) == 4:
        if current_list[0] == current_list[1] and current_list[1] == current_list[2]:
            if current_list[3] == current_list[2]:
                return 6
            else:
                return 4
        else:
            return 0
    elif len(current_list) >= 5:
        for i in range(len(current_list)-1):
            if current_list[i+1] != current_list[i]:
                return 0
        return 5



def judge(current_cards,last_cards):
        if not(current_cards):
                return True 
        else:
            current_type = judgeType(current_cards)
            last_type = judgeType(last_cards)
            if current_type:
                if current_type != 6 and current_type != last_type:
                    print("你给的牌与上家类型不同")
                    return False
                else:
                    if current_type == 1:
                        if current_cards[0] > last_cards[0]:
                            return True
                        else:         
                            print("您所出的牌没有大过上家")                       
                            return False
                    elif current_type == 2:
                        if current_cards[0] > last_cards[0]:
                            return True
                        else:
                            print("您所出的牌没有大过上家") 
                            return False
                    elif current_type == 3:
                        if current_cards[0] > last_cards[0]:
                            return True
                        else:
                            print("您所出的牌没有大过上家") 
                            return False
                    elif current_type == 4:
                        if current_cards[0] > last_cards[0]:
                            return True
                        else:
                            print("您所出的牌没有大过上家") 
                            return False
                    elif current_type == 5:
                        if current_cards[0] > last_cards[0]:
                            return True
                        else:
                            print("您所出的牌没有大过上家") 
                            return False
                    elif current_type == 6:
                        if current_type == last_type:
                            if current_cards[0] > last_cards[0]:
                                return True
                            else:
                                print("您所出的牌没有大过上家") 
                                return False
                        else:
                            return True 
            else:
                print("您给的牌为非法类型")
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
        for point in give_list:
                before_len = len(give_index_list)
                for i in range(len(palyers_cards)):
                        if point == palyers_cards[i].point:
                                if not(palyers_cards[i].index in give_index_list):
                                        give_index_list.append(palyers_cards[i].index)
                                        break
                current_len = len(give_index_list)
                if before_len == current_len:
                    print("输入的{}不是您所持有的牌".format(char))
                    return   False  
        if judge(give_list,current_cards):
                return give_index_list
        else:
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
                                                if palyers_cards[i].index == index:
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