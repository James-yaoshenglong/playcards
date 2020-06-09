#花色列表
SUIT_LIST = ("黑桃", "草花", "红桃", "方片", "王牌")
#点数大小排序表
POINT_LIST = ("3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A", "2", "小", "大")

class Card(object):
    '''牌类'''
    def __init__(self,index):
        if index == 52:
            self.index = index
            self.suit = 4 #花色代表在点数排序表中的位置
            self.point = 13 #点数表示在大小排序表中的位置，并不是直接的位置
            self.name = 'LittleJoker'
        elif index == 53:
            self.index = index
            self.color = 4
            self.point = 14
            self.name = 'BigJoker'
        else:
            self.index = index
            self.color = self.index % 4
            self.point = self.index % 13
            self.name = POINT_LIST[self.point]
        self.pic = './images/'+self.name+'.png' #图片的地址