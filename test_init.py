from score.score_gen import Score
from score.node_manager import Monitor
from score.observation import Observation
from score.transactions import Transaction


def test():

    # /////////////////////////////////////////////
    print("This is the test function")
    a = Score()
    a.c_score_test()
    # /////////////////////////////////////////////



    Monitor.starter()
    a = Observation()
    a.observe_time = 1111
    a.observe_zone = "#21"
    a.observe_event = "12"

    a.node_list.append("x01")
    a.node_list.append("x02")
    a.node_list.append("x03")
    a.node_list.append("x04")
    a.node_list.append("x05")
    a.node_list.append("x06")

    # 产生一个事件
    obs = {}  # 观察到的现象
    '''
    timestamp: 观察到的时间
    location_zone: 事件所在的区域，为了找到可以帮忙的车
    location_section: 事件所在的路段，确定具体的位置
    event_class: 事件的分类
    。。。。。。
    '''

    # 选择一个终端节点作为事件的观测和发布者
    x1 = Monitor(obs)

    # 观测者调用通信协议将结果发出去


    # 一个终端集合内的所有节点得到这个结果，参考集列表
    #     定义一个参考集合，填满终端节点


    #




    b = Transaction()


if __name__ == "__main__":

    test()
