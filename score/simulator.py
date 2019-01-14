from score.IoV_state import IoVMessage


# 读取位置信息，生成广播消息
def file_location(files):
    gen = []
    with open(files, 'r') as f:
        locations = f.readlines()
    for i in range(0, len(locations)):
        locations[i] = locations[i].rstrip('\n')
        a = locations[i].split(',')
        gen.append((a[0][1:], a[1][:-2]))
    return gen

