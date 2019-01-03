from score.score_gen import Score
from score.moniter import Moniter
from score.observation import Observation
from score.transactions import Transaction


def test():

    # /////////////////////////////////////////////
    print("This is the test function")
    a = Score()
    a.c_score_test()
    # /////////////////////////////////////////////

    Moniter.starter()
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

    b = Transaction.serialize(a)
    print(b)


if __name__ == "__main__":
    test()
