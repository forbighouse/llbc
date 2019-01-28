from xmlrpc.client import ServerProxy


server = ServerProxy('http://127.0.0.1:6666')  # 连接服务器，创建服务器代理对象
print(server.twice(6))  # 调用服务器提供的函数