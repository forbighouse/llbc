from test_script.veh_trust.config import *


def probability_count_fuc2(msg, bl_op):
    probability_true_resp_dict = defaultdict(list)

    for items in msg:
        if items[5] == 1:
            expand_ratio = round(((random.choice(range(25, 50))) / 50), 2)
            r1 = 1 - math.pow(0.07 * (items[7] - items[4]), 3)
            # r1 = 0.5 + math.exp(-0.7*(items[7]-items[4]))
            if 0.5 + math.exp(-0.014 * ((items[6] + 50) * expand_ratio)) > 1:
                r2 = 0.99
            else:
                r2 = 0.5 + math.exp(-0.014 * ((items[6] + 50) * expand_ratio))
        else:
            expand_ratio = round(((random.choice(range(10, 25))) / 50), 2)
            r1 = 1 - math.pow(0.07 * (items[7] - items[4]), 3)
            # r1 = 0.5 + math.exp(-0.7*(items[7]-items[4]))
            r2 = 0.5 + math.exp(-0.014 * ((items[6] + 50) * (1+expand_ratio)))

        pby_answer = ((r1 + r2) / 2)
        probability_true_resp_dict[items[5]].append(pby_answer)
        # print("{} {} {}".format("[mean_occur_probability = ", pby_answer, " ]"))

    return probability_true_resp_dict


def probability_count_fuc3(msg, bl_op):
    probability_true_resp_dict = defaultdict(list)
    tmp_weight_recent_dict = defaultdict(list)
    tmp_weight_past_dict = defaultdict(list)

    for items in msg:
        r2 = 0.5 + math.exp(-0.014*(items[6]+50))
        probability_true_resp_dict[items[5]].append(r2)

        # 历史消费信誉，2天或2周时间间隔，例如 近2天/总4天，算出总的活跃度
        # tmp_weight_recent_dict[items[5]].append(bl_op[items[0]][0][1])
        # tmp_weight_past_dict[items[5]].append(bl_op[items[0]][0][0])

    return probability_true_resp_dict


def probability_count_fuc4(msg, bl_op):
    probability_true_resp_dict = defaultdict(list)
    for items in msg:
        if items[5] == 1:
            expand_ratio = round(((random.choice(range(25, 50))) / 50), 2)
            r1 = 0.5 + math.exp(-0.014 * ((items[6]+50) * expand_ratio))
            if r1 > 1:
                r1 = 0.99
        else:
            expand_ratio = round(((random.choice(range(10, 25))) / 50), 2)
            r1 = 0.5 + math.exp(-0.014 * ((items[6] + 50) * (1+expand_ratio)))
        probability_true_resp_dict[items[5]].append(r1)
    return probability_true_resp_dict
