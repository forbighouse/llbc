
# ================== base_veh_location ===================
# 仿真车辆的数量
VEH_NUM = 50
# veh位置的文件名称
VEH_LOCATION_FILE = 'veh_list.txt'
# accident的文件名称
ACCIDENT_LOCATION_FILE = 'accident_list.txt'
# 区块链钱包地址的文件名称
BLOCKCHAIN_ADDRESS_FILE = 'bl_address_ids.txt'
# veh的初始化速度文件名称
VEH_SPEED_FILE = 'veh_speed_list.txt'
# 区块链网络的地址数量
BLOCKCHAIN_ADDRESS_TOTAL_NUM = round((1+2)*VEH_NUM)
# 事件的类型，例如车祸、红绿灯、限行、拥堵等
ACCIDENT_TYPE = 0
# 仿真的事件数量
ACCIDENT_NUM = 50
# 道路长度，目前只有一条直路
ROAD_LEN = 5000

# =================== trust_management_simulator ================
# 仿真轮数
SIMULATION_ROUND = 50
# RSU的设定数量
RSU_NUM = 35
# 通信距离设定
THRESHOLD_COMMUNICATION = 300
# RSU的间距
RSU_DISTANCE = 250
# 仿真车辆的数量
VEH_NUM = 50
# 仿真时间
time_len = 200000
# 车辆感知范围，设定车辆在多近的距离才可以汇报事件
VEHICLE_PERCEPTION_DISTANCE = 150
# 一个消息的时效性
TIME_TOLERANCE = 1
# 事件发生的阈值
THRESHOLD = 0.5
# 事件发生的概率
PE = 0.1  # 应该用动态的每个事件用一个，这里先用相同的测试
# 测试模式
DEBUG = 0
# 更新所有的txt文件
UPDATE_TXT = 0
# veh和accident的距离值修正，根据accident的可能性判定公式，太近了超出1
RATE_CORRECT = 50

# =================== trust_v4 ================
TRICKER = 50
